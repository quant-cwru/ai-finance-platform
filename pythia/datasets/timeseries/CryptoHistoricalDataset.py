from openbb import obb
from torch.utils.data import Dataset
import numpy as np
import torch
from pythia.datasets.TimeSeries import TimeSeries 

class CryptoHistoricalDataset(TimeSeries):
    def __init__(self, symbol, start_date, end_date, seq_length, interval='1d', transform=None, provider='yfinance'):
        """
        Instantiates a dataframe of the closing prices of a given ticker symbol, period, and interval
        """
        # Fetch data using OpenBB
        self.data_df = obb.crypto.price.historical(symbol=symbol, start_date=start_date, end_date=end_date, interval=interval, provider=provider).to_df()

    def norm(self):
        """
        Normalizes the data and stores it as field: data_n
        """
        self.data_n = self.data.copy()
        for c in self.data_n.columns:
            mean = self.data_n[c].mean()
            std = self.data_n[c].std()
            self.data_n[c] = (self.data_n[c] - mean) / std

#############################################
# Begin
# Prior code commented because it's DataProcessor part

    # The follow code went under __init__
        # close_prices = self.data_df['close'].values
        # self.X, self.y = [], []

        # # Create input/output pairs
        # for i in range(len(close_prices) - seq_length):
        #     self.X.append(close_prices[i:i+seq_length])
        #     self.y.append(close_prices[i+1:i+seq_length+1])

        # self.transform = transform

        # self.X_mean = np.mean(self.X)
        # self.X_std = np.std(self.X)
        # self.y_mean = np.mean(self.y)
        # self.y_std = np.std(self.y)
    # The above code went under __init__

    # def __len__(self):
    #     return len(self.X)

    # def __getitem__(self, idx):

    #     inputs = self.X[idx]
    #     targets = self.y[idx]
    #     sample = (inputs, targets)

    #     if self.transform:
    #         sample = self.transform(sample)

    #     return sample

# class Rescale(object):
#   def __call__(self, sample):
#     inputs = sample[0]
#     targets = sample[1]
#     inputs_mean = np.mean(inputs)
#     inputs_std = np.std(inputs, axis=0)
#     targets_mean = np.mean(targets)
#     targets_std = np.std(targets, axis=0)

#     inputs = (inputs - inputs_mean) / inputs_std
#     targets = (targets - targets_mean) / targets_std

#     return inputs, targets

# class ToTensor(object):
#     """Convert ndarrays in sample to Tensors."""

#     def __call__(self, sample):
#       inputs = sample[0]
#       targets = sample[1]
#       return torch.tensor(inputs), torch.tensor(targets)

# # Transformation classes remain the same as previously defined:
# # - Rescale
# # - ToTensor

# End
#############################################
