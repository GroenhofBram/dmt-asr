import torch

DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"