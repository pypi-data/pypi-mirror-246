"""
Utils for SUBLIME model
"""
import numpy as np
import torch
import torch.nn.functional as F
from sklearn import metrics
from sklearn.neighbors import kneighbors_graph

# from munkres import Munkres

# pylint: disable=no-else-return


def nearest_neighbors_pre_elu(X, k, metric, i):
    adj = kneighbors_graph(X, k, metric=metric)
    adj = np.array(adj.todense(), dtype=np.float32)
    adj += np.eye(adj.shape[0])
    adj = adj * i - i
    return adj


def knn_fast(X, k, b):
    X = F.normalize(X, dim=1, p=2)
    index = 0
    values = torch.zeros(X.shape[0] * (k + 1)).cuda()
    rows = torch.zeros(X.shape[0] * (k + 1)).cuda()
    cols = torch.zeros(X.shape[0] * (k + 1)).cuda()
    norm_row = torch.zeros(X.shape[0]).cuda()
    norm_col = torch.zeros(X.shape[0]).cuda()
    while index < X.shape[0]:
        if (index + b) > (X.shape[0]):
            end = X.shape[0]
        else:
            end = index + b
        sub_tensor = X[index:index + b]
        similarities = torch.mm(sub_tensor, X.t())
        vals, inds = similarities.topk(k=k + 1, dim=-1)
        values[index * (k + 1):(end) * (k + 1)] = vals.view(-1)
        cols[index * (k + 1):(end) * (k + 1)] = inds.view(-1)
        rows[index * (k + 1):(end) * (k + 1)] = (torch.arange(index, end).view(
            -1, 1).repeat(1, k + 1).view(-1))
        norm_row[index:end] = torch.sum(vals, dim=1)
        norm_col.index_add_(-1, inds.view(-1), vals.view(-1))
        index += b
    norm = norm_row + norm_col
    rows = rows.long()
    cols = cols.long()
    values *= torch.pow(norm[rows], -0.5) * torch.pow(norm[cols], -0.5)
    return rows, cols, values


def apply_non_linearity(tensor, non_linearity, i):
    if non_linearity == "elu":
        return F.elu(tensor * i - i) + 1
    elif non_linearity == "relu":
        return F.relu(tensor)
    elif non_linearity == "none":
        return tensor
    else:
        raise NameError("We dont support the non-linearity yet")


def cal_similarity_graph(node_embeddings):
    similarity_graph = torch.mm(node_embeddings, node_embeddings.t())
    return similarity_graph


def top_k(raw_graph, K):
    _, indices = raw_graph.topk(k=int(K), dim=-1)
    assert torch.max(indices) < raw_graph.shape[1]
    mask = torch.zeros(raw_graph.shape).cuda()
    mask[torch.arange(raw_graph.shape[0]).view(-1, 1), indices] = 1.0

    mask.requires_grad = False
    sparse_graph = raw_graph * mask
    return sparse_graph


def get_feat_mask(features, mask_rate):
    feat_node = features.shape[1]
    mask = torch.zeros(features.shape)
    samples = np.random.choice(feat_node,
                               size=int(feat_node * mask_rate),
                               replace=False)
    mask[:, samples] = 1
    return mask.cuda(), samples


def symmetrize(adj):  # only for non-sparse
    return (adj + adj.T) / 2


def split_batch(init_list, batch_size):
    groups = zip(*(iter(init_list), ) * batch_size)
    end_list = [list(i) for i in groups]
    count = len(init_list) % batch_size
    end_list = end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


# class clustering_metrics():
#     """clustering metrics"""
#     def __init__(self, true_label, predict_label):
#         self.true_label = true_label
#         self.pred_label = predict_label

#     def clusteringAcc(self):
#         # best mapping between true_label and predict label
#         l1 = list(set(self.true_label))
#         numclass1 = len(l1)

#         l2 = list(set(self.pred_label))
#         numclass2 = len(l2)
#         if numclass1 != numclass2:
#             print('Class Not equal, Error!!!!')
#             return 0, 0, 0, 0, 0, 0, 0

#         cost = np.zeros((numclass1, numclass2), dtype=int)
#         for i, c1 in enumerate(l1):
#             mps = [i1 for i1, e1 in enumerate(self.true_label) if e1 == c1]
#             for j, c2 in enumerate(l2):
#                 mps_d = [i1 for i1 in mps if self.pred_label[i1] == c2]

#                 cost[i][j] = len(mps_d)

#         # match two clustering results by Munkres algorithm
#         m = Munkres()
#         cost = cost.__neg__().tolist()

#         indexes = m.compute(cost)

#         # get the match results
#         new_predict = np.zeros(len(self.pred_label))
#         for i, c in enumerate(l1):
#             # correponding label in l2:
#             c2 = l2[indexes[i][1]]

#             # ai is the index with label==c2 in the pred_label list
#             ai = [ind for ind, elm in enumerate(self.pred_label) if elm == c2]
#             new_predict[ai] = c

#         acc = metrics.accuracy_score(self.true_label, new_predict)
#         f1_macro = metrics.f1_score(self.true_label,
#                                     new_predict,
#                                     average='macro')
#         precision_macro = metrics.precision_score(self.true_label,
#                                                   new_predict,
#                                                   average='macro')
#         recall_macro = metrics.recall_score(self.true_label,
#                                             new_predict,
#                                             average='macro')
#         f1_micro = metrics.f1_score(self.true_label,
#                                     new_predict,
#                                     average='micro')
#         precision_micro = metrics.precision_score(self.true_label,
#                                                   new_predict,
#                                                   average='micro')
#         recall_micro = metrics.recall_score(self.true_label,
#                                             new_predict,
#                                             average='micro')
#         return acc, f1_macro, precision_macro, recall_macro, f1_micro, precision_micro, recall_micro

#     def evaluationClusterModelFromLabel(self, print_results=True):
#         nmi = metrics.normalized_mutual_info_score(self.true_label,
#                                                    self.pred_label)
#         adjscore = metrics.adjusted_rand_score(self.true_label,
#                                                self.pred_label)
#         (acc, f1_macro, precision_macro, recall_macro, f1_micro,
#          precision_micro, recall_micro) = self.clusteringAcc()

#         if print_results:
#             print(
#                 f'ACC={acc:.4f}, f1_macro={f1_macro:.4f}, precision_macro={precision_macro:.4f}, \
#                 recall_macro={recall_macro:.4f}, f1_micro={f1_micro:.4f}, ' +
#                 f'precision_micro={precision_micro:.4f}, recall_micro={recall_micro:.4f}, \
#                     NMI={nmi:.4f}, ADJ_RAND_SCORE={adjscore:.4f}')

#         return acc, nmi, f1_macro, adjscore
