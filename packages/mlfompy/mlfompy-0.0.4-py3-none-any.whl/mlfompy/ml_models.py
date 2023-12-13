"""
==============================
Machine learning models module
==============================

Models for the neural networks for FoM and I-V curves prediction."""
import torch
import torch.nn as nn
from torch.nn import functional as F
import pytorch_lightning as pl
from torch.utils.data import Dataset
from torchmetrics import MeanAbsolutePercentageError
from torcheval.metrics.functional import r2_score

class CustomDataset(Dataset):
    """Dataset class"""
    def __init__(self, data_in, data_out):
        self.data_in = data_in
        self.data_out = data_out

    def __len__(self):
        return len(self.data_in)

    def __getitem__(self, i):
        if torch.is_tensor(i):
            i = i.tolist()
        return self.data_in[i], self.data_out[i]


class mlp_mgg_fom(pl.LightningModule):
    """Class for the multi-layer perceptron applied to predict the FoMs due to MGG"""
    def __init__(self, config):
        super().__init__()
        self.input_layer_size = config["input_layer_size"]
        self.layer_1 = config["layer_1"]
        self.layer_2 = config["layer_2"]
        self.lr = config["lr"]
        self.batch_size = config["batch_size"]
        self.momentum = config["momentum"]
        self.std = config["weight_std"]
        self.encoder = nn.Sequential(
            nn.Linear(self.input_layer_size,self.layer_1),
            nn.ReLU(),
            nn.Linear(self.layer_1, self.layer_2),
            nn.ReLU(),
            nn.Linear(self.layer_2, 1)
        )
        self.apply(self.init_weights_normal)
        # Save the hyperparameters to use the trained NN
        self.save_hyperparameters()


    def init_weights_normal(self, module):
        """ Initialization of the weights of neural network layers and nodes
        with a normal distribution with mean=0, with std as a hyperparameter
        """
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=self.std)
            if module.bias is not None:
                module.bias.data.zero_()


    def forward(self,x):
        """Prediction/inference actions"""
        embedding = self.encoder(x)
        return embedding


    def configure_optimizers(self):
        """Optimization algorithm"""
        optimizer = torch.optim.SGD(self.parameters(), momentum=self.momentum, lr=self.lr,nesterov=False)
        lr_scheduler = {
            'scheduler': torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min',factor=0.5, verbose=True),
            'name': 'learning_rate_scheduler',
            'monitor': 'val/loss'
        }
        return [optimizer], [lr_scheduler]


    def training_step(self, train_batch, batch_idx):
        """Training loop with MSE as loss function, R2 metric to visualize"""
        x, y = train_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            self.log('train/r2', r2, on_step=True, on_epoch=True, logger=True)
        self.log('train/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True) # sending metrics to TensorBoard, add on_epoch=True to calculate epoch-level metrics
        return loss


    def validation_step(self, val_batch, batch_idx):
        """Validation loop with MSE as loss function, R2 metric to visualize"""
        x, y = val_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            self.log('val/r2', r2, on_step=True, on_epoch=True, logger=True)
        self.log('val/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)


    def test_step(self, test_batch, batch_idx):
        """Test loop with MSE as loss function, R2 and MAPE metrics to visualize"""
        x, y = test_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        mape = MeanAbsolutePercentageError()
        mape = mape(y_hat, y)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            self.log('test/r2', r2, on_step=True, on_epoch=True, logger=True)
        self.log('test/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log('test/mape', mape, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        rscore = round(r2.item(),3)
        # print(f'This is the R2 of the test: {rscore}')


class mlp_mgg_iv(pl.LightningModule):
    """Multi-layer perceptron applied to predict the I-V curves due to MGG. Structure of the NN is defined here"""
    def __init__(self, config): # config added to ray tune
        super().__init__()
        self.input_layer_size = config["input_layer_size"]
        self.layer_1 = config["layer_1"]
        self.layer_2 = config["layer_2"]
        # self.layer_3 = config["layer_3"]
        self.lr = config["lr"]
        self.batch_size = config["batch_size"]
        self.momentum = config["momentum"]
        self.std = config["weight_std"]
        self.encoder = nn.Sequential(
            nn.Linear(self.input_layer_size,self.layer_1),
            nn.Tanh(),
            nn.Linear(self.layer_1, self.layer_2),
            nn.Tanh(),
            nn.Linear(self.layer_2, 21)
        )
        self.apply(self.init_weights_normal)
        # Save the hyperparameters to use the trained NN
        self.save_hyperparameters()


    def init_weights_normal(self, module):
        """
        Initialization of the weights of neural network layers and nodes
        with a normal distribution with mean=0, with std as a hyperparameter
        """
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=self.std)
            if module.bias is not None:
                module.bias.data.zero_()


    def init_weights_xavier(self, module):
        """
        The current standard approach for initialization of the weights of neural
        network layers and nodes that use the Sigmoid or TanH activation function
        is called “glorot” or “xavier” initialization
        """
        if isinstance(module, nn.Linear):
            torch.nn.init.xavier_uniform(module.weight)
            module.bias.data.fill_(0)


    def init_weights_he(self, module):
        """
        The current standard approach for initialization of the weights of neural
        network layers and nodes that use the rectified linear (ReLU) activation
        function is called “he” initialization.
        """
        if isinstance(module, nn.Linear):
            torch.nn.init.kaiming_uniform_(module.weight)
            module.bias.data.fill_(self.bias)

    def forward(self,x):
        """Prediction/inference actions"""
        embedding = self.encoder(x)
        return embedding


    def configure_optimizers(self):
        """Optimization algorithm"""
        optimizer = torch.optim.SGD(self.parameters(), momentum=self.momentum, lr=self.lr,nesterov=False)
        lr_scheduler = {
            'scheduler': torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min',factor=0.5, verbose=True),
            'name': 'learning_rate_scheduler',
            'monitor': 'val/loss'
        }
        return [optimizer], [lr_scheduler]


    def training_step(self, train_batch, batch_idx):
        """Training loop with MSE as loss function, R2 metric to visualize"""
        x, y = train_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            self.log('train/r2', r2, on_step=True, on_epoch=True, logger=True)
        # sending metrics to TensorBoard, add on_epoch=True to calculate epoch-level metrics
        self.log('train/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return loss


    def validation_step(self, val_batch, batch_idx):
        """Validation loop with MSE as loss function, R2 metric to visualize"""
        x, y = val_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            self.log('val/r2', r2, on_step=True, on_epoch=True, logger=True)
        self.log('val/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)


    def test_step(self, test_batch, batch_idx):
        """Test loop with MSE as loss function, R2 and MAPE metrics to visualize"""
        x, y = test_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        mape = MeanAbsolutePercentageError()
        mape = mape(10**y_hat, 10**y)
        if len(y_hat)>2:
            r2 = r2_score(10**y_hat, 10**y)
            self.log('test/r2', r2, on_step=True, on_epoch=True, logger=True)
        rscore = round(r2.item(),3)
        self.log('test/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log('test/mape', mape, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        # print(f'Iste é o R2 do test: {r2}')