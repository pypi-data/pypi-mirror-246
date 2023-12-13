"""
===========================================
Machine learning traning and testing module
===========================================

Functions to perform the training and testing of the
machine learning models and the PCA and scaler objects."""
import numpy as np
import torch
from pathlib import Path
import pickle
import time
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from torch.utils.data import DataLoader
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, QuantileTransformer, PowerTransformer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR


from . import ml_models
from. import auxiliar as aux


def save_sk_model(model, type):
    """Saves a model in sk_logs folder in working directory

    Parameters
    ----------
    model: objet
        Model object to be saved
    type: str
        Model type to select the log destination folder.
        Values: regressor, finetuned, pca or scaler
    """
    t_valid_types = ('regressor', 'finetuned', 'scaler', 'pca')
    if type not in t_valid_types:
        aux.print_error(f'Invalid type provided. Valid values are {t_valid_types}')
        exit()

    path_sk_logs = Path('sk_logs', type)
    sk_logs_num_version = len(list(path_sk_logs.glob('v_*')))
    filename = Path(path_sk_logs, f'v_{sk_logs_num_version}_{type}.sav')
    filename.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(model, open(filename, 'wb'))


def input_output_fom_select(data, var_source='mgg', fom='vth_LE [V]'):
    """ Creates the neural network input and output pytorch tensors, fom='vth_LE [V]' by default

    Parameters
    ----------
    data: dictionary
        Simulated data
    fom: str
        Choose the figure of merit for the neural network training. Accepted labels:
            - For Vth: ['vth_LE [V]'], ['vth_SD [V]], ['vth_CC [V]]
            - For ioff: ['ioff_VG [A]']
            - For SS: ['ss_VGI [mV/dec]']
            - For ion: ['ion_dd_VG [A]'], ['ion_mc_VG [A]']

    Returns
    --------
    X: torch.tensor
        Input tensor for the neural network
    Y: torch.tensor
        Output tensor for the neural network
    """
    X, Y = [], []
    for _, item in enumerate(data):
        if var_source == 'mgg':
            X.append(item['mgg_profile [eV]'])
        elif var_source == 'ler':
            X.append(item['ler_profile [nm]'])
        Y.append(item[fom])
    Y = np.array(Y, dtype=float)
    print("Total size\n","\tInput:", torch.tensor(X).shape,"\tOutput:",torch.tensor(Y).shape)
    return torch.tensor(X), torch.tensor(Y)


def input_output_iv(data):
    """Creates the neural network input (mgg_profiles) and output (logIoff) pytorch tensors

    Parameters
    ----------
    data: dict
        Simulated data

    Returns
    -------
    X: dict
        Input dict for the neural network with ids
    Y: dict
        Output dict with the log10Ioff for the neural network with ids
    """
    X, Y = [], []
    for _, item in enumerate(data):
        X.append({'id':item['id'],
                  'data':item["mgg_profile [eV]"]})
        Y.append({'id':item['id'],
                  'data':np.log10(item["iv_curve"]["i_drain [A]"])})
    print("Total size\n","\tInput:",f'[{len(X)}, {len(X[0]["data"])}]',"\tOutput:", f'[{len(Y)}, {len(Y[0]["data"])}]')
    return  X, Y


def scaler_to_data(x, scaler_selector="StandarScaler", scaler=None):
    """ Scales the input data using the selected scaler

    Parameters
    ----------
    x: list
        Input data
    scaler_selector: str
        Select the scaler to be used. Accepted labels:
            - "StandarScaler" (default) from sklearn.preprocessing library
            - "MinMaxScaler" from sklearn.preprocessing library
            - "MaxAbsScaler" from sklearn.preprocessing library
            - "RobustScaler" from sklearn.preprocessing library
            - "QuantileTransformer" from sklearn.preprocessing library
            - "PowerTransformer" from sklearn.preprocessing library
    scaler: sklearn.preprocessing object
        If scaler is not None, the scaler object is used to scale the data

    Returns
    -------
    x_scaled: list
        Scaled input data
    scaler: sklearn.preprocessing object
        Scaler object used to scale the data
    """
    p_scaler = scaler
    if scaler is None:
        if scaler_selector == "StandarScaler":
            scaler = StandardScaler()
        elif scaler_selector == "MinMaxScaler":
            scaler = MinMaxScaler()
        elif scaler_selector == "MaxAbsScaler":
            scaler = MaxAbsScaler()
        elif scaler_selector == "RobustScaler":
            scaler = RobustScaler()
        elif scaler_selector == "QuantileTransformer":
            scaler = QuantileTransformer()
        elif scaler_selector == "PowerTransformer":
            scaler = PowerTransformer()
        else:
            aux.print_warning(f'[{__name__}.scaler_to_data] Scaler not found, using StandardScaler')
            scaler = StandardScaler() # default scaler

    x_scaled = scaler.fit_transform(x)

    # Save scaler object to disk for future use
    if p_scaler is None:
        save_sk_model(scaler, 'scaler')

    return x_scaled, scaler


def split_data(X, Y, test_size = 0.2):
    """Split the data into the train, validation and test subsets

    Parameters
    ----------
    X: dict or torch.tensor
        Input data to split
    Y: dict or torch.tensor
        Output data to split
    test_size: float
        Ratio for the test/train and validation/train split, by default is set to 0.2

    Returns
    -------
    X_train/Y_train: dict or torch.tensor
        Input/Output train subsets
    X_val/Y_val: dict or torch.tensor
        Input/Output validation subsets
    X_test/Y_test: dict or torch.tensor
        Input/Output test subsets
    """
    X, X_test, Y, Y_test = train_test_split(X, Y, test_size=test_size, random_state = 0)
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=test_size, random_state = 0)
    if torch.is_tensor(X_train):
        print("Tensor dimensions:\n\tTrain:\t\tInput:", X_train.shape," Output:", Y_train.shape,
            "\n\tValidation:\tInput:", X_val.shape," Output:", Y_val.shape,
            "\n\tTest:\t\tInput:", X_test.shape," Output:", Y_test.shape
            )
    else:
        print("Tensor dimensions:\n\tTrain:\t\tInput:",f'[{len(X_train)}, {len(X_train[0]["data"])}]',"\tOutput:", f'[{len(Y_train)}, {len(Y_train[0]["data"])}]'
            "\n\tValidation:\tInput:",f'[{len(X_val)}, {len(X_val[0]["data"])}]',"\tOutput:", f'[{len(Y_val)}, {len(Y_val[0]["data"])}]'
            "\n\tTest:\t\tInput:",f'[{len(X_test)}, {len(X_test[0]["data"])}]',"\tOutput:", f'[{len(Y_test)}, {len(Y_test[0]["data"])}]'
            )
    return X_train, X_val, X_test, Y_train, Y_val, Y_test


def pca_features_reduction(X_train, X_val, X_test, criteria=0.95):
    """Applies the PCA methodology to reduce the features. The PCA is fitted to the train dataset, by default to the 95% of the cummulative variance

    Parameters
    ----------
    X_train: torch.tensor
        Input train subsets
    X_val: torch.tensor
        Input validation subsets
    X_test: torch.tensor
        Input test subsets
    criteria: float
        If the criteria is an integer, the criteria correspond to the number of features reduction after applying PCA
        If the criteria is a float between 0 and 1, correspond to apply the criteria of a percentage of the total cummulative variance

    Returns
    --------
    X_train_pca: torch.tensor
        Input train subset afet applying the PCA reduction
    X_val_pca: torch.tensor
        Input validation subset afet applying the PCA reduction
    X_test_pca: torch.tensor
        Input test subset afet applying the PCA reduction
    pca: pca_object
        pca object with the information of the features reduction
    """
    pca = PCA(criteria)
    X_train_pca = torch.tensor(pca.fit_transform(X_train.tolist()))
    X_test_pca = torch.tensor(pca.transform(X_test).tolist())
    X_val_pca = torch.tensor(pca.transform(X_val).tolist())

    # Save pca object to disk for future use
    save_sk_model(pca, 'pca')

    print("Tensor dimensions after PCA:\n","\tTrain:", "\t\tInput:", X_train_pca.shape,
        "\n\tValidation:", "\t\tInput:", X_val_pca.shape,
        "\n\tTest:", "\t\tInput:", X_test_pca.shape
        )
    return  X_train_pca.to(torch.float32), X_val_pca.to(torch.float32), X_test_pca.to(torch.float32), pca


def generate_dataloaders(X_train, X_val, X_test, Y_train, Y_val, Y_test, config, num_workers = 10):
    """Generation of the DataLoaders to the train, validation and test processes.
    The DataLoaders combines a dataset and a sampler, and provides an iterable over the given dataset.

    Parameters
    ----------
    X_train: torch.tensor
        Input train subsets
    X_val: torch.tensor
        Input validation subsets
    X_test: torch.tensor
        Input test subsets
    config: dictionary
        Contains the key:value pairs for the neural network hyperparameters
    num_workers: int
        How many subprocesses to use for data loading. 0 means that the data will be loaded in the main process

    Returns
    -------
    train_loader: Dataloader
        Iterable object to train
    val_loader: Dataloader
        Iterable object to validate
    test_loader: Dataloader
        Iterable obejct to test
    """
    test_dataset = ml_models.CustomDataset(data_in=X_test, data_out=Y_test)
    test_loader = DataLoader(dataset=test_dataset, batch_size=len(X_test), num_workers = num_workers)
    train_dataset = ml_models.CustomDataset(data_in=X_train, data_out=Y_train)
    train_loader = DataLoader(dataset=train_dataset, batch_size=config["batch_size"], num_workers = num_workers)
    val_dataset = ml_models.CustomDataset(data_in=X_val, data_out=Y_val)
    val_loader = DataLoader(dataset=val_dataset, batch_size=config["batch_size"],num_workers = num_workers)
    print("Dimension train dataset:", len(train_dataset))
    print("Dimension validation dataset:", len(val_dataset))
    print("Dimension test dataset:", len(test_dataset))
    return train_loader, val_loader, test_loader


def mgg_train_test_fom(X_train, X_val, X_test, Y_train, Y_val, Y_test, config = None, num_epochs = 1500):
    """ Train and test process to calibrate the neural network and predict the foms

    Parameters
    ----------
    X_train: torch.tensor
        Input train subsets
    X_val: torch.tensor
        Input validation subsets
    X_test: torch.tensor
        Input test subsets
    config: dictionary
        Contains the key:value pairs for the neural network hyperparameters
    num_epochs: int
        Number of epochs, 1500 by default as it is implemented the early stopping method

    Returns
    --------
    model: pytorch lightning object
        Calibrated neural network model
    """
    if config is None:
        config = {
            "input_layer_size": len(X_train[0]),
            "layer_1": int(len(X_train[0])/3),
            "layer_2": int(len(X_train)/16),
            "lr": 1e-1,
            "momentum": 0.9,
            "weight_std": 0.01,
            "batch_size": 64
            }
    train_loader, val_loader, test_loader = generate_dataloaders(X_train, X_val, X_test, Y_train, Y_val, Y_test, config)
    early_stopping = EarlyStopping('val/r2',mode = 'max', min_delta = 5e-4, patience = 50,verbose = True)
    model = ml_models.mlp_mgg_fom(config)
    trainer = pl.Trainer(accelerator="cpu",max_epochs=num_epochs,check_val_every_n_epoch=1,log_every_n_steps=1,callbacks=[early_stopping])
    trainer.fit(model, train_loader, val_loader)
    trainer.test(model, dataloaders = test_loader)
    return model


def mgg_train_test_iv(X_train, X_val, X_test, Y_train, Y_val, Y_test, config = None, num_epochs = 1500):
    """Train and test process to calibrate the neural network and predict the I-V curves

    Parameters
    ----------
    X_train: torch.tensor
        Input train subsets
    X_val: torch.tensor
        Input validation subsets
    X_test: torch.tensor
        Input test subsets
    config: dictionary
        Contains the key:value pairs for the neural network hyperparameters
    num_epochs: int
        Number of epochs, 1500 by default as it is implemented the early stopping method

    Returns
    --------
    - model: pytorch lightning object
        Calibrated neural network model
    """
    if config is None:
        config = {
            "input_layer_size": len(X_train[0]),
            "layer_1": int(len(X_train[0])/3),
            "layer_2": int(len(X_train[0])/16),
            "lr": 1e-1,
            "momentum": 0.9,
            "weight_std": 0.01,
            "batch_size": 32
        }
    train_loader, val_loader, test_loader = generate_dataloaders(X_train, X_val, X_test, Y_train, Y_val, Y_test, config)
    early_stopping = EarlyStopping('val/r2', mode = 'max', min_delta = 1e-3, patience = 50,verbose = True)
    model = ml_models.mlp_mgg_iv(config)
    trainer = pl.Trainer(accelerator="cpu",max_epochs=num_epochs,check_val_every_n_epoch=1,log_every_n_steps=1,callbacks=[early_stopping])
    trainer.fit(model, train_loader, val_loader)
    trainer.test(model, dataloaders = test_loader)
    return model


def ler_train_model(x, y, config = {}):
    """Training process to calibrate predictor the foms for LER variabitlity
    This function is based on different regressors from sklearn library

    The regressor to be fitted or trained are the following from sklearn and
    it can be selected using the config parameter with the regressor key and
    posible values are: MLP (default), LinearRegression, DecisionTree, RandomForest or SVM

    These regressors have been already tested with LER varaibility data and
    the results can be checked in https://doi.org/10.1371/journal.pone.0288964

    Parameters
    ----------
    x: list of values
        Input subsets
    y: list of values
        Output subsets
    config: dictionary
        Contains the key:value pairs for the hyperparameters configuration. Options are:
        - regressor: MLP (default), LinearRegression, DecisionTree, RandomForest or SVM
        - seed: random seed
        - iterations: max. number of iterations
        - activation: activation function for MLP. Default is tanh.

    Returns
    --------
    regressor: Sklearn regressor object
        Fitted sklearn regressor object
    """
    regresor_type = config.get('regresor_type','MLP')
    seed = int(config.get('seed', 905))
    activation = config.get('activation', 'tanh')
    iters = int(config.get('iterations', 2000))
    if regresor_type == 'LinearRegression':
        regressor = LinearRegression()
    elif regresor_type == 'DecisionTree':
        regressor = DecisionTreeRegressor(random_state = seed)
    elif regresor_type == 'RandomForest':
        reg = RandomForestRegressor(n_estimators = 100 ,  random_state = seed)
    elif regresor_type == 'SVM':
        regressor = SVR(kernel="rbf", epsilon=0.05)
    else: # MLP default option
        print('Max. number of iterations: ', iters)
        regressor = MLPRegressor(
            hidden_layer_sizes = (80, 80, 80),
            solver = 'lbfgs',
            random_state = seed,
            alpha = 0.1,
            tol = 1e-10,
            activation = activation,
            max_iter = iters,
            verbose = False
        )
    start = time.time()
    regressor.fit(x, y)
    t = time.time() - start
    if hasattr(regressor, 'n_iter_'):
        print('Iterations executed:', regressor.n_iter_, end='. ')
    print('Training time (seconds):', t)

    # Save regressor object to disk for future reference
    save_sk_model(regressor, 'regressor')

    return regressor


def ler_finetune_model(X_train, Y_train, regressor, config={}):
    """ Fine-tunning existing predictor model

    Parameters
    ----------
    X_train: list of values
        Input train subsets
    Y_train: list of values
        Input test subsets
    config: dictionary
        Contains the key:value pairs for the hyperparameters configuration. Options are:
        - iterations: max. number of iterations
        - activation: activation function for MLP. Default is tanh.

    Returns
    --------
    regressor: Sklearn regressor object
        Fitted sklearn regressor object
    """
    activation = config.get('activation', 'tanh')
    iters = int(config.get('iterations', 3000))
    print ('Number of finetuning train examples:', len(X_train))
    sc_X = StandardScaler()
    X_train_fit = sc_X.fit(X_train)
    X_trainscaled = X_train_fit.transform(X_train)
    regressor.max_iter = iters
    regressor.activations = activation
    regressor.warm_start = True
    print('Warm start: ', regressor.warm_start, end='. ')
    start = time.time()
    regressor.fit(X_trainscaled, Y_train)
    t = time.time() - start
    print('Training time (seconds):', t)

    # Save regressor object to disk for future reference
    save_sk_model(regressor, 'finetuned')

    return regressor