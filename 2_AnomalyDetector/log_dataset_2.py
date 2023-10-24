
import torch as T
from torch.utils.data import Dataset
import pandas as pd

class LogDataset(Dataset):

    def __init__(self, data_path, cols=[], steps=3):

        self.steps = steps
        self.df = pd.read_csv(data_path, header=0, index_col=None)

        if not cols == []:
            self.df = self.df[cols]
      
    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        if idx + self.steps >= len(self)-1:
            idx -= self.steps

        return T.tensor(self.df.iloc[idx:idx+self.steps].values, dtype=T.float), T.tensor(self.df.iloc[idx+self.steps].values, dtype=T.float)

class TestDataset(Dataset):

    def __init__(self, data_path, cols=[], steps=3):

        self.steps = steps
        self.df = pd.read_csv(data_path, header=0, index_col=None)

        if not cols == []:
            self.df = self.df[cols + ['wind1', 'wind2']]
      
    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        if idx + self.steps >= len(self)-1:
            idx -= self.steps

        seq = self.df.iloc[idx:idx+self.steps].values
        seq_tensor = T.tensor(seq, dtype=T.float)
        anomaly = seq_tensor[:, 3:]
        anomaly_ = anomaly.any(0).any(0)
        anomaly_int = anomaly_.int()

        return T.tensor([T.tensor(self.df.iloc[idx:idx+self.steps, :3].values, dtype=T.float), T.tensor(self.df.iloc[idx+self.steps, :3].values, dtype=T.float), anomaly_int])