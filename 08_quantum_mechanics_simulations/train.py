import pickle

import numpy as np
from numpy import random as rnd
from matplotlib import pyplot as plt
from tqdm import autonotebook as tqdm

from sklearn.model_selection import train_test_split


import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor

with open("data/dataset.bin", mode="rb") as fh:
    data = pickle.load(fh)


num_examples = len(data)
num_points = len(data[0]["space"])

potentials = np.zeros((num_examples, num_points))
wave_functions = np.zeros((num_examples, num_points))
energies = np.zeros(num_examples)

for k, item in enumerate(data):
    potentials[k] = item["potential"]
    wave_functions[k] = item["states"][0]["wave_function"]
    energies[k] = item["states"][0]["energy"]


train_pot, test_pot, train_wf, test_wf, train_en, test_en = train_test_split(
    potentials, wave_functions, energies
)


class QMDataset(Dataset):
    def __init__(self, potential, wave_function, energy):
        self.potential = potential.astype(np.float32)
        self.wave_function = wave_function.astype(np.float32)
        self.energy = energy.astype(np.float32)

    def __len__(self):
        return self.potential.shape[0]

    def __getitem__(self, idx):
        return self.potential[idx], self.wave_function[idx], self.energy[idx]


trainset = QMDataset(train_pot, train_wf, train_en)
testset = QMDataset(test_pot, test_wf, test_en)


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(300, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 16),
            nn.ReLU(),
        )
        self.energy_stack = nn.Sequential(
            nn.Linear(16, 32), nn.ReLU(), nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 1)
        )
        self.wf_stack = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, 300),
        )

    def forward(self, x):
        x = self.flatten(x)
        rep = self.linear_relu_stack(x)
        energy = self.energy_stack(rep)
        psi = self.wf_stack(rep)
        return psi, torch.squeeze(energy)


model = NeuralNetwork().to("cpu")
print(model)


loss_psi = nn.MSELoss()
loss_eng = nn.MSELoss()
optm = torch.optim.SGD(model.parameters(), lr=1e-3)


loader = DataLoader(trainset, batch_size=32)
size = len(loader)

for batch, (v, psi, e) in enumerate(loader):
    psi_pred, e_pred = model(v.to("cpu"))
    loss = loss_psi(psi_pred, psi.to("cpu")) + loss_eng(e_pred, e.to("cpu"))
    optm.zero_grad()
    loss.backward()
    optm.step()

    #     if batch % 100 == 0:
    loss, current = loss.item(), batch * len(v)
    print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


#     print(v.shape)
#     print(psi.shape)
#     print(e.shape)
#     psi_pred, e_pred = model(v)
#     print(psi_pred.shape)
#     print(e_pred.shape)
#     break
