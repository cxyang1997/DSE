import torch
import random
from torch.autograd import Variable
import copy
# import domain

def var(i, requires_grad=False):
    # print(i)
    if requires_grad:
        exit(0)
    if torch.cuda.is_available():
        return Variable(torch.tensor(i, dtype=torch.float).cuda(), requires_grad=requires_grad)
    else:
        return Variable(torch.tensor(i, dtype=torch.float), requires_grad=requires_grad)


def var_list(i_list, requires_grad=False):
    # print(i)
    if requires_grad:
        exit(0)
    if torch.cuda.is_available():
        # res = Variable(torch.tensor(i_list, dtype=torch.double).cuda(), requires_grad=requires_grad)
        res = torch.tensor(i_list, dtype=torch.float, requires_grad=requires_grad).cuda()
    else:
        # res = Variable(torch.tensor(i_list, dtype=torch.double), requires_grad=requires_grad)
        res = torch.tensor(i_list, dtype=torch.float, requires_grad=requires_grad)
    # print(f"before squeeze, {res.shape}")
    # print(f"var list --before unsequeeze-- res: {res}")
    # res.unsqueeze_(0)
    # print(f"var list --after unsequeeze-- res: {res}")
    # print(f"after squeeze, {res.shape}")
    return res


PI = var((3373259426.0 + 273688.0 / (1 << 21)) / (1 << 30))
PI_TWICE = PI.mul(var(2.0))
PI_HALF = PI.div(var(2.0))

# print(PI)
# print(torch.sin(PI))
# print(torch.sin(PI_TWICE))
# print(torch.sin(PI_HALF))

def split_symbol_table(symbol_table, argument_list, partition=10):
    symbol_table_list = list()
    # TODO: for now, assume the partition is along one dimension
    if len(argument_list) == 1:
        target = argument_list[0]
        original_length = symbol_table[target].getVolumn()
        domain_list = symbol_table[target].split(partition) # interval/zonotope split
        for domain in domain_list:
            # print('domain', domain.left, domain.right)
            new_symbol_table = dict()
            for key in symbol_table:
                # print('OUT key, target', key, target)
                if key == target:
                    # print('key, target', key, target)
                    new_symbol_table[key] = domain
                elif 'probability' in key:
                    new_symbol_table[key] = symbol_table[key].mul(var(1.0/partition))
                # TODO: 
                elif key == 'point_cloud' or key == 'counter':
                    point_cloud = list()
                    counter = 0
                    for point_symbol_table in symbol_table['point_cloud']:
                        point_value = point_symbol_table[target].left.data.item()
                        if point_value <= domain.right.data.item() and point_value >= domain.left.data.item():
                            counter += 1
                            point_cloud.append(point_symbol_table)
                    new_symbol_table['point_cloud'] = point_cloud
                    new_symbol_table['counter'] = var(counter)
                else:
                    new_symbol_table[key] = copy.deepcopy(symbol_table[key])
            symbol_table_list.append(new_symbol_table)
    elif len(argument_list) == 0:
        return [symbol_table]
    else:
        return [symbol_table]

    return symbol_table_list


def build_point_cloud(symbol_table, X_train, y_train, f):
    symbol_table['point_cloud'] = list()

    for idx, x in enumerate(X_train):
        x, y = x, y_train[idx]
        smooth_point_symbol_table = f(x, y)
        symbol_table['point_cloud'].append(smooth_point_symbol_table)
    symbol_table['counter'] = var(len(symbol_table['point_cloud']))
    
    return symbol_table


def create_point_cloud(symbol_table, point_set, f):
    symbol_table['point_cloud'] = list()

    for x in point_set:
        point_symbol_table = f(x)
        symbol_table['point_cloud'].append(point_symbol_table)
    symbol_table['counter'] = var(len(symbol_table['point_cloud']))

    return symbol_table


def product(it):
    if isinstance(it, int):
        return it
    product = 1
    for x in it:
        if x >= 0:
            product *= x
    return product


def get_size(t):
    return (t.element_size(), t.nelement())