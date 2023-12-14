import argparse
import pickle as pkl
import os
import cupy as cp
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--feature_file')
parser.add_argument('--ver')
parser.add_argument('--db_folder')
parser.add_argument('--ind1')
parser.add_argument('--ind2')
parser.add_argument('--device')
parser.add_argument('--out_folder')
args = parser.parse_args()

db_folder, part, ind1, ind2, device, out_folder,feature_path = args.db_folder, args.ver, int(args.ind1), int(args.ind2), int(
    args.device), args.out_folder, args.feature_file

print(db_folder, part, ind1, ind2, device, out_folder,feature_path)
def match(feature, path):
    try:
        with open(path, 'rb') as f:
            data = pkl.load(f)
        name = data[0]
        dt = data[1]
        dt = cp.array(dt)
        feature = cp.array(feature)
        res = cp.max(cp.dot(dt, feature.T) - 0.95, axis=0)
        ind = res > 0
        score = float(cp.sum(res * ind))
        match = int(cp.sum(ind))
        return name, match, score
    except:
        return 0, 0, 0


path = [os.path.join(db_folder, n) for n in os.listdir(db_folder)]
with open(feature_path, 'rb') as f:
    feature = pkl.load(f)
with cp.cuda.Device(device):
    feature = cp.array(feature)
    mempool = cp.get_default_memory_pool()
    res = []
    for j in path[ind1:ind2]:
        res.append(match(feature, j))
    mempool.free_all_blocks()
    with open(out_folder + '/{}.pkl'.format(j.split('/')[-1].split('.')[0]), 'wb') as f:
        pkl.dump(res, f)
