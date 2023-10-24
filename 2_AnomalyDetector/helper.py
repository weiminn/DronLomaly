
import torch as T
import pandas as pd
from torch.utils.data import Dataset 

def evaluate(seq, y, model, cols, pCols, dataset: Dataset, testfile=None, threshold_sigma=3, epochs = 10):
    mean = T.tensor(dataset.df.describe().T['mean'])
    std = T.tensor(dataset.df.describe().T['std'])
    std = T.round(std,decimals=10)
    std[std==0] = 0.0000000001 # must have a minimum std

    true_positives = 0.
    total = 0.
    # res = pd.DataFrame(columns=cols + pCols + ['label'])
            
    y_hat = model(seq)
    l1_distances = T.abs(y_hat-y)
    # label = 0
    # for i,l1 in enumerate(l1_distances):
    #     total += 1
    #     threshold = threshold_sigma * std
    #     deviations = l1 > threshold
    #     deviation = T.any(deviations)
        
        # if deviation.item() > 0: 
        #     label = 1
        #     true_positives += 1

    # d = []
    # l = y.detach().tolist()[0]
    # for item in enumerate(l):
    #     d.append(item[1])
    # l = y_hat.detach().tolist()[0]
    # for item in enumerate(l):
    #     d.append(item[1])
    # d.append(label)
    # temp = pd.DataFrame([d], columns=cols + pCols + ['label'])
    # res = pd.concat([res, temp], axis=0)
                
    # print(f"Detected deviations: {true_positives}")
    # return true_positives/total
    # return true_positives, total, l1_distances.squeeze_(0)
    return l1_distances.squeeze_(0)
  