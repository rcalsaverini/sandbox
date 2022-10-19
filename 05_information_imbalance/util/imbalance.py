from annoy import AnnoyIndex
import numpy as np
import tqdm.autonotebook as tqdm


def index_annoy(data, n_trees):
    """
    Index a data set using annoy.
    """
    index = AnnoyIndex(data.shape[1], "angular")
    for i, x in enumerate(data):
        index.add_item(i, x)
    index.build(n_trees)
    return index


def enumerate_kth_neighbor(data, k, n_trees=100):
    """
    Enumerate the k-th neighbor of each datum of a data set.
    """
    n_points, dim = data.shape
    index = index_annoy(data, n_trees)
    for i in range(n_points):
        (*_, idxs), (*_, ds) = index.get_nns_by_item(i, k + 1, include_distances=True)
        yield i, idxs, ds


def y_rank_given_x_rank(x, y, x_rank=1, n_trees=100):
    y_index = index_annoy(y, n_trees)
    y_ranks = []
    for i, x_idx, ds in tqdm.tqdm(
        enumerate_kth_neighbor(x, x_rank, n_trees), total=x.shape[0]
    ):
        y_idxs = y_index.get_nns_by_item(i, y.shape[0])
        y_ranks.append(y_idxs[x_idx])
    return y_ranks


def information_imbalance(x, y):
    ranks = y_rank_given_x_rank(x, y, x_rank=1)
    return 2 / y.shape[0] * np.mean(ranks)
