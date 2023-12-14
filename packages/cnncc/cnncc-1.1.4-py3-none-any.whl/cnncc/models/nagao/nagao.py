import torch
import torch.nn as nn
from functools import partial
from torchvision import transforms
from PIL import Image
import os
import pandas as pd
import random
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
from torchvision.transforms import v2
import numpy as np


def load_pretrained_model():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    model = torch.load(
        current_dir + "/nagao_71acc.pt", map_location=torch.device("cpu")
    )
    model.eval()
    return model


def prepare_img_for_inference(image):
    image = Image.open(image)

    transform = transforms.Compose(
        [
            transforms.Resize((300, 300)),
            transforms.ToTensor(),
        ]
    )

    image = transform(image)
    image = image.unsqueeze(0)
    return image


def inference(model, image):
    with torch.no_grad():
        output = model(image)
        output = torch.nn.functional.softmax(output, dim=1)
        p, classe = torch.max(output, dim=1)
        p = p.item() * 100
        classe = classe.item()
        return output, p, classe
