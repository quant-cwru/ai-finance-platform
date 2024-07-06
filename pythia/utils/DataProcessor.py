import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import torch
from project.data.datasets.timeseries.StockHistorical import StockHistorical


class DataProcessor:
    """
    Important distinction between a dataset and a processor: only the latter contains features and labels.
    For now assume the input object is formatted exactly like data.datasets.timeseries.StockHistorical
    If data does not have the attribute data_n, then the data is unnormed.
    """
    def __init__(self, data : StockHistorical):
        self.data = data
        self.features = None
        self.labels = None
    
    def set_features(self, features : list):
        """
        Takes in a list of columns identified by their name and creates the respective feature subset.
        """
        if hasattr(self.data, "data_n"):
            self.features = self.data.data_n[features]
        else:
            self.features = self.data.data[features]
    
    def set_labels(self, labels: list, shift=1):
        """
        Takes in a list of labels and creates the respective target subset.
        Since we are dealing with time-series data right now, the shift indicates how many timesteps ahead the labels are.
        """
        if hasattr(self.data, "data_n"):
            data = self.data.data_n
        else:
            data = self.data.data

        self.labels = data[labels].shift(-shift)
        
        # Remove NaN values
        self.features = self.features[:-shift]
        self.labels = self.labels[:-shift]
        self.labels = self.labels.dropna()
        self.features = self.features.loc[self.labels.index]

    def drop(self, col: str):
        """
        Drops a column in the dataset. Should also drop the same column in its features and labels (if present).
        """
        if hasattr(self.data, "data_n"):
            self.data.data_n.drop(columns=[col], inplace=True)
        self.data.data.drop(columns=[col], inplace=True)

        if self.features is not None and col in self.features.columns:
            self.features.drop(columns=[col], inplace=True)
        if self.labels is not None and col in self.labels.columns:
            self.labels.drop(columns=[col], inplace=True)

    def plot(self, feature_idx=None):
        """
        Plots the input dataframe if no sample index is provided. Else plots the associated feature-target on a timeseries scale.
        """
        if hasattr(self.data, "data_n"):
            # Data is normalized, denormalize it
            data = self.data.data_n.copy()
            means = self.data.data.mean()
            stds = self.data.data.std()

            for c in data.columns:
                data[c] = data[c] * stds[c] + means[c]
        else:
            # Data is unnormalized
            data = self.data.data

        fig, ax = plt.subplots(figsize=(10, 6))

        if feature_idx is None:
            # Plot the entire DataFrame
            data.plot(ax=ax)
            ax.set_title("Stock Prices")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
        else:
            if feature_idx < 0 or feature_idx >= len(self.features.columns):
                raise IndexError("Feature index out of range.")
            
            # Plot the associated feature-target on a timeseries scale.

            # Get the name of the selected feature
            feature_name = self.features.columns[feature_idx]

            # Plot the selected feature
            ax.plot(self.features.index, self.features.iloc[:, feature_idx], 
                    label=feature_name, color='blue')

            # Plot the target
            target_name = self.labels.columns[0] 
            ax.plot(self.labels.index, self.labels.iloc[:, 0], 
                    label=f'Target ({target_name})', color='red', linestyle='--')

            ax.set_title(f"Feature-Target Timeseries: {feature_name} vs {target_name}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Value")
            ax.legend()

        ax.grid(True)
        return fig

    def to_torch(self):
        """
        Returns a torch dataset (in tensors) from the corresponding features and labels.
        See https://pytorch.org/tutorials/beginner/basics/data_tutorial.html
        """

        #Custom torch class
        class CustomTorchDataset(Dataset):
            def __init__(self, features, labels):
                self.features = torch.tensor(features.values, dtype=torch.float32)
                self.labels = torch.tensor(labels.values, dtype=torch.float32)

            def __len__(self):
                return len(self.features)

            def __getitem__(self, idx):
                return self.features[idx], self.labels[idx]

        #Instantiates the torch class with the data and returns it
        return CustomTorchDataset(self.features, self.labels)

    def __getitem__(self, idx):
        if self.features is None or self.labels is None:
            raise ValueError("Features and labels must be set before indexing.")
        
        return {
            'features': self.features.iloc[idx],
            'label': self.labels.iloc[idx]
        }
    
    def __len__(self):
        if self.features is None:
            raise ValueError("Features must be set before getting length.")
        return len(self.features)
        