import os
import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, RandomSampler

from .wandb import Wandb
from .stats import Statistics
from .utils import to_device, get_date, Callbacks
from .logger import Logger


class Trainer(Callbacks):
    def __init__(self, model, config):
        self.config = config
        self.logger = Logger("Trainer", config)
        self.date = get_date()

        if self.config.device == "auto":
            self.config.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.logger.log(f"Set on device {self.config.device}", force=True)

        self.model = model.to(device=self.config.device)
        if self.config.compile:
            self.logger.log(f"Compiling model...", force=True)
            self.model = torch.compile(self.model)
            self.logger.log(f"Model compiled!", force=True)

        self.epoch = 0
        self.iteration = 0
        self.optimizer = self.config.optimizer(
            self.model.parameters(), lr=self.config.lr, **self.config.optimizer_params
        )
        self.criterion = self.config.criterion()
        self.scheduler = None
        if self.config.scheduler:
            self.scheduler = self.config.scheduler(
                self.optimizer, **self.config.scheduler_params
            )

        if config.wandb:
            self.wandb = Wandb(config)

        Callbacks.__init__(self)

    @staticmethod
    def get_file_path(date, epoch, iteration):
        return f"{date}_epoch={epoch:03d}_iter={iteration:06d}.pt"

    @staticmethod
    def get_checkpoint_path(config, date, epoch, iteration):
        folder = os.path.join(config.checkpoint_folder, config.name)
        file = Trainer.get_file_path(date, epoch, iteration)
        return folder, os.path.join(folder, file)

    def save_model(self):
        state = {
            "epoch": self.epoch,
            "iter": self.iteration,
            "config": self.config,
            "model": self.model.to(device="cpu").state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "scheduler": self.scheduler.state_dict()
            if self.scheduler != None
            else None,
        }

        folder, cp_path = Trainer.get_checkpoint_path(
            self.config, self.date, self.epoch, self.iteration
        )
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.logger.log(
            f"Saving model {self.config.name} at epoch {self.epoch}, iter {self.iteration} to {cp_path}",
            force=True,
        )
        torch.save(state, cp_path)
        return cp_path

    def _load_state_dict(self, checkpoint, keep_states):
        # self.epoch = checkpoint["epoch"]
        # self.iteration = checkpoint["iter"]
        self.model.load_state_dict(checkpoint["model"])
        if keep_states:
            self.optimizer.load_state_dict(checkpoint["optimizer"])
            if self.config.scheduler != None:
                self.scheduler.load_state_dict(checkpoint["scheduler"])

    @staticmethod
    def from_pretrained(model, config, cp_path, keep_states=True):
        Logger("Trainer", config).log("Loading checkpoint from", cp_path, force=True)
        checkpoint = torch.load(cp_path)
        # Don't use the checkpoint config as it contains erroneous data such as optimizer, scheduler represented as strings
        # Moreover, this allows to change the config between runs, even tho this is already possible from one training to another
        trainer = Trainer(model, config)
        trainer._load_state_dict(checkpoint, keep_states)
        return trainer

    def on_batch_end(self, statistics, output, target, loss):
        self.trigger_callbacks("on_batch_end")

        if self.config.stats_every == None or (
            self.iteration != 0 and self.iteration % self.config.stats_every != 0
        ):
            return

        stats = statistics.register(output, target, loss, self.epoch, self.iteration)

        if self.config.wandb:
            self.wandb.log(stats)

        self.trigger_callbacks("on_stats", **stats)

    def fit(self, train_dataset, eval_dataset=None):
        device = self.config.device
        self.model.train()
        self.date = get_date()

        statistics = Statistics(
            self.model,
            self.criterion,
            self.scheduler,
            self.config,
            eval_dataset,
        )

        train_loader = DataLoader(
            train_dataset,
            sampler=RandomSampler(train_dataset, replacement=True),
            shuffle=False,
            pin_memory=device != "cpu",
            batch_size=self.config.batch_size,
            num_workers=self.config.num_workers,
        )
        data_iter = iter(train_loader)

        if self.config.wandb:
            self.logger.log("Initializing wandb")
            self.wandb.init(self.model, self.optimizer, self.criterion, self.scheduler)

        self.logger.log("Starting training")
        while self.iteration < self.config.max_iterations and (
            self.config.epochs == None or self.epoch < self.config.epochs
        ):
            try:
                batch = next(data_iter)
            except StopIteration:
                data_iter = iter(train_loader)
                self.epoch += 1
                self.trigger_callbacks("on_epoch_end")
                batch = next(data_iter)

            self.trigger_callbacks("on_batch_start")
            data, target = batch
            data, target = to_device(data, device), to_device(target, device)

            output = self.model(data)
            loss = self.criterion(output, target)

            loss.backward()
            if self.config.grad_norm_clip != None and self.config.grad_norm_clip != 0.0:
                nn.utils.clip_grad_norm_(
                    self.model.parameters(), self.config.grad_norm_clip
                )
            self.optimizer.step()
            if self.scheduler:
                self.scheduler.step()
            self.optimizer.zero_grad(set_to_none=True)

            self.on_batch_end(statistics, output, target, loss)

            self.iteration += 1

        cp_path = self.save_model()
        return statistics, cp_path
