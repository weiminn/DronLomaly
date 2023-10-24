import torch as T
import pandas as pd
from torch.utils.data import Dataset 

class LogDataset(Dataset):

    def __init__(self, data_path, type='dji', steps=3):

        self.steps = steps
        self.df = pd.read_csv(data_path, header=0, index_col=None)

        if type == 'dji':
            self.df = self.df[['acceleration_x', 'acceleration_y', 'acceleration_z']]
        else:

            self.df['airspeedchange'] = self.df['airspeed']- self.df['airspeed'].shift(1)
            self.df['airspeedchange'].fillna(0, inplace=True)

            self.df = self.df[['roll', 'pitch', 'yaw', 'rollspeed', 'pitchspeed', 'yawspeed',  'airspeedchange']]

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        if idx + self.steps >= len(self)-1:
            idx -= self.steps

        return T.tensor(self.df.iloc[idx:idx+self.steps].values, dtype=T.float), T.tensor(self.df.iloc[idx+self.steps].values, dtype=T.float)