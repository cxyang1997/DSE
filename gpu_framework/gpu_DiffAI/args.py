import os

import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('true', 'y', 't'):
        return True
    elif v.lower() in ('false', 'n', 'f'):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")

def get_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--lr", default=0.000001, type=float, help="learning rate")
    p.add_argument("--stop_val", default=0.05, type=float, help="error for stoping")
    p.add_argument("--t_epoch", default=10, type=int, help="epoch for lambda")
    p.add_argument("--optimizer", default="direct", type=str, help="select the optimizer")
    p.add_argument("--w", default=0.5, type=float, help="the measure between two lagarangian iteration")

    p.add_argument("--benchmark_name", default="benchmark", help="represent the benchmark")
    p.add_argument("--data_size", default=10000, type=int, help="size of dataset, both for training and testing")
    p.add_argument("--test_portion", default=0.99, type=float, help="portion of test set of the entire dataset")
    p.add_argument("--num_epoch", default=10, type=int, help="number of epochs for training")
    p.add_argument("--width", default=0.1, type=float, help="width of perturbation") # for DiffAI
    
    p.add_argument("--n", default=5, type=int, help="number of theta sampled around mean")
    p.add_argument("--nn_mode", default='all', help="how many NN used in model, 'single' means only used in the first one")
    p.add_argument("--l", default=10, type=int, help="size of hidden states in NN")
    p.add_argument("--b", default=1000, type=int, help="range of lambda")
    p.add_argument("--module", default="linearrelu", help="module in model")

    # dataset
    p.add_argument("--data_attr", default="normal_52.0_59.0", help="dataset_attr")
    p.add_argument("--train_size", default=200, type=int, help="training size")
    p.add_argument("--test_size", default=20000, type=int, help="test size")

    # perturbation
    p.add_argument("--num_components", default=10, type=int, help="number of components to split")
    p.add_argument("--bs", default=10, type=int, help="batch size by number of component")
    
    # training
    p.add_argument("--use_smooth_kernel", default=False, type=str2bool, help="decide whether to use smooth kernel")
    p.add_argument("--save", default=True, help="decide whether to save the model or not")

    # evaluation
    p.add_argument("--test_mode", default=False, type=str2bool, help="decide whether check load model and then test")
    return p


def get_args():
    return get_parser().parse_args()

if __name__ == "__main__":
    a = get_args()
    print(a)