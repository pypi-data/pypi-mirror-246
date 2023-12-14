"""
    Used for context_embedding
"""
import logging as log
import threading
import time
from queue import Queue

import numpy as np

from ....utils.ComE_utils import chunkize_serial
from ....utils.ComE_utils import initComeEnv
from ....utils.ComE_utils import prepare_sentences

log.basicConfig(
    format="%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s",
    level=log.DEBUG,
)

try:
    initComeEnv()
    from ....module.pretrain.ComE.SDG_utils.training_sdg_inner import (
        train_o2,
        FAST_VERSION,
    )

    # print(f"cython version {FAST_VERSION}")
except ImportError as e:
    log.error(e)
    raise e


class Context2Vec:
    """
    Class that train the context embedding
    """

    def __init__(self, lr=0.1, window_size=5, workers=1, negative=5):
        """
        :param lr: learning rate
        :param window: windows size used to compute the context embeddings
        :param workers: number of thread
        :param negative: number of negative samples
        :return:
        """

        self.lr = float(lr)
        self.min_lr = 0.0001
        self.workers = workers
        self.negative = negative
        self.window_size = int(window_size)

    def train(self,
              model,
              paths,
              total_nodes,
              alpha=1.0,
              node_count=0,
              chunksize=150):
        """
        Update the model's neural weights from a sequence of paths
        (can be a once-only generator stream).

        :param model: model containing the shared data
        :param paths: generator of the paths
        :param total_nodes: total number of nodes in the path
        :param alpha: trade-off parameter
        :param node_count: init of the number of nodes
        :param chunksize: size of the batch
        :return:
        """
        assert model.node_embedding.dtype == np.float32
        assert model.context_embedding.dtype == np.float32
        print(
            f"O2 training model with {self.workers} workers on {len(model.vocab)} vocabulary and"
            f" {model.layer1_size} features, using \t'negative "
            f"sampling'={self.negative}\t'windows'={self.window_size}")

        if alpha <= 0.0:
            return

        if not model.vocab:
            raise RuntimeError(
                "you must first build vocabulary before training the model")

        start, next_report = time.time(), [1.0]
        if total_nodes is None:
            raise AttributeError("need the number of node")

        node_count = [0]

        jobs = Queue(
            maxsize=2 *
            self.workers)  # buffer ahead only a limited number of jobs..
        # this is the reason we can't simply use ThreadPool :(
        lock = (
            threading.Lock()
        )  # for shared state (=number of nodes trained so far, log reports...)

        def worker_train():
            """Train the model, lifting lists of paths from the jobs queue."""
            py_work = np.zeros(model.layer1_size, dtype=np.float32)

            while True:
                job = jobs.get()
                if job is None:  # data finished, exit
                    break

                lr = max(self.min_lr,
                         self.lr * (1 - 1.0 * node_count[0] / total_nodes))
                job_nodes = sum(
                    train_o2(
                        model.node_embedding,
                        model.context_embedding,
                        path,
                        lr,
                        self.negative,
                        self.window_size,
                        model.table,
                        py_alpha=alpha,
                        py_size=model.layer1_size,
                        py_work=py_work,
                    ) for path in job)  # execute the sgd

                with lock:
                    node_count[0] += job_nodes

                    elapsed = time.time() - start
                    if elapsed >= next_report[0]:
                        print(
                            f"PROGRESS: at {100.0 * node_count[0] / total_nodes:.2f}"
                            f"%% nodes, lr {lr:.5f}, "
                            f"{node_count[0] / elapsed if elapsed else 0.0:.0f} nodes/s"
                        )
                        next_report[0] = elapsed + 1.0
                        # don't flood the log, wait at least a second between progress reports

        workers = [
            threading.Thread(target=worker_train) for _ in range(self.workers)
        ]
        for thread in workers:
            thread.daemon = True  # make interrupting the process with ctrl+c easier
            thread.start()

        # convert input strings to Vocab objects (eliding OOV/downsampled nodes)
        # , and start filling the jobs queue
        for _, job in enumerate(
                chunkize_serial(prepare_sentences(model, paths), chunksize)):
            jobs.put(job)

        print(
            f"reached the end of input; waiting to finish {jobs.qsize()} outstanding jobs"
        )
        for _ in range(self.workers):
            jobs.put(
                None
            )  # give the workers heads up that they can finish -- no more work!

        for thread in workers:
            thread.join()

        elapsed = time.time() - start
        print(f"training on {node_count[0]} nodes took {elapsed:.1f}s,"
              f" {node_count[0] / elapsed if elapsed else 0.0:.0f} "
              f"nodes/s")
