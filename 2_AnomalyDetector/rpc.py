import xmlrpc.server
from collections import deque
from params import log_offsets
from visualize import animate
from threading import Thread

# LSTM imports  
import torch as T
import pandas as pd
from model import Model
from log_dataset_2 import LogDataset
from helper import evaluate
from torch.utils.data import DataLoader 


class MyServer:

    def __init__(self) -> None:
        self.type = 'euler'
        self.cols = log_offsets[self.type]['cols']

        self.base_file = './dataset/dji/baseline.csv'
        self.anomaly_file = './dataset/dji/anomaly.csv'
        self.runtime_file = './dataset/dji/runtime.csv'
        self.predict_file = f'./dataset/dji/predict_{self.type}.csv'

        self.model_name = 'dji_' +  self.type
        self.batch_size = 1
        self.steps = 10  # data collection rate is set at 10Hz, hence 10 steps means prediction at every 1 second
        self.window_sz = 30 # window size for runtime data analysis
        self.threshold = 3 # deviation threshold 
        self.epochs = 50 # for training
        self.input_sz = len(self.cols)

        self.djibaseDataset = LogDataset(self.base_file, self.cols, steps=self.steps)
        self.djiwindyDataset = LogDataset(self.anomaly_file, self.cols, steps=self.steps)
        self.baseline = self.djibaseDataset

        self.model = Model(batch_size=self.batch_size, input_size=3, hidden_size=64, num_layers=5, linear_size=128,device= 'cuda' if T.cuda.is_available() else 'cpu')
        self.model.load_state_dict(T.load('models/' + self.model_name + '_s' + str(self.steps) + '_b' + str(self.batch_size)))
        self.model.eval()  # set model in evaluation mode

        self.buffer = deque()

        self.pCols = []
        for col in self.cols:
            c = "predicted_" + col
            self.pCols.append(c)
        self.pdf = pd.DataFrame(columns=self.cols + self.pCols + ['label'])

        self.x_display_queue = deque()
        self.y_display_queue = deque()
        self.z_display_queue = deque()
        self.queues = [self.x_display_queue, self.y_display_queue, self.z_display_queue]
        # thread = Thread(target=animate, args=(self.queues, self.threshold*T.tensor(self.djibaseDataset.df.describe().T['std']), ))
        thread = Thread(target=animate, args=(self.queues, ))
        thread.start()
    
    def test(self, *msg):
        # print("Received: ", msg)
        l1 = None

        size = len(self.buffer)
        if size == self.steps+1:
            # inference
            seq = list(self.buffer)[0:self.steps]
            y = T.tensor(self.buffer[-1], dtype=T.float32)[log_offsets[self.type]['start']:log_offsets[self.type]['end']].unsqueeze_(0)
            tseq = T.tensor(seq, dtype=T.float32)[:, log_offsets[self.type]['start']:log_offsets[self.type]['end']].unsqueeze_(0)
            l1 = evaluate(tseq, y, self.model, self.cols, self.pCols, self.baseline, testfile=None, threshold_sigma=self.threshold, epochs = 1)

            for i in range(len(self.queues)):
                dev = l1[i].item()
                self.queues[i].append(dev / (self.threshold*T.tensor(self.baseline.df.describe().T['std']).tolist()[i]))

            # print('Detection Deviations:', true_positives, ', Total:', total)
            self.buffer.popleft()

        if len(self.queues[0]) >= 60:
            for i in range(len(self.queues)):
                self.queues[i].popleft()

        
        self.buffer.append(msg)        

        return "Hello back from server!"

server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000))
server.register_instance(MyServer())
server.serve_forever()