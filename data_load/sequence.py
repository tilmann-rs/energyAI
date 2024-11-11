# Modify the create_sequences function to handle multiple features
import numpy as np
import torch

def sequence_target_slicing(data, seq_len, pred_len):

    sequences = []
    targets = []

    for i in range(len(data) - seq_len - pred_len):
        seq = data[i:i + seq_len]
        target = data[i + seq_len:i + seq_len + pred_len]
        sequences.append(seq)
        targets.append(target)

    # Convert lists to NumPy arrays first, then to PyTorch tensors
    return torch.tensor(np.array(sequences), dtype=torch.float32), torch.tensor(np.array(targets), dtype=torch.float32)


#
# def create_sequences_torch(data, seq_len, pred_len):
#     sequences = []
#     targets = []
#
#     for i in range(len(data) - seq_len - pred_len):
#         seq = data[i:i + seq_len]
#         target = data[i + seq_len:i + seq_len + pred_len]
#         sequences.append(seq)
#         targets.append(target)
#
#     # Convert lists to NumPy arrays first, then to PyTorch tensors
#     return torch.tensor(np.array(sequences), dtype=torch.float32), torch.tensor(np.array(targets), dtype=torch.float32)


def create_sequences_np(data, seq_length, pred_len):
    X, y = [], []
    for i in range(len(data) - seq_length - pred_len):
        X.append(data[i:(i + seq_length), :])
        y.append(data[i + seq_length:i + seq_length + pred_len, :])
    # Convert lists to tensors before returning
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)
