import numpy as np


def random_initialization(n_value: int, max_value: int) -> np.ndarray:
    """Random initialization of the pi_star partition.

    Parameters
    ----------
    n_value : int
        Number of data points
    max_value : int
        Maximal number of clusters

    Returns
    -------
    np.ndarray of shape (n_value)
        Random partition
    """
    return np.random.randint(low=0, high=max_value, size=n_value)


def compute_majority_disagreement(
    clusters: np.ndarray, max_value: int, pi_star: np.ndarray, weights: np.ndarray
) -> np.ndarray:
    """Compute the disagreement matrix.

    Parameters
    ----------
    clusters : np.ndarray of shape (n, m)
        Various clustering used to compute the disagreement matrix
    max_value : int
        Maximal number of clusters
    pi_star : np.ndarray of shape (n)
        Current partition
    weights : np.ndarray of shape (m)
        Weights of each clustering

    Returns
    -------
    np.ndarray of shape (n, max_value)
        Disagreement matrix
    """
    disagreement = np.full(shape=(clusters.shape[0], max_value), fill_value=np.inf)
    for i in range(max_value):
        p_i = pi_star == i

        if p_i.any():
            repr_p_i = get_majority(clusters[p_i].T)

            disagreement[:, i] = np.sum(
                weights[None] * np.sum(clusters[:, None] != repr_p_i[None], axis=1),
                axis=-1,
            )

    return disagreement


def get_majority(matrix: np.ndarray) -> np.ndarray:
    """Return the most present cluster for each clustering

    Parameters
    ----------
    matrix : np.ndarray of shape (n, m)
        Matrix of n points clustered m times

    Returns
    -------
    np.ndarray of shape (m)
        Most present cluster in each clustering
    """
    return np.array([np.bincount(vector).argmax() for vector in matrix])


def compute_probabilistic_disagreement(
    clusters: np.ndarray, max_value: int, pi_star: np.ndarray, weights: np.ndarray
) -> np.ndarray:
    """Compute the disagreement matrix of the IPVC algorithm.

    Parameters
    ----------
    clusters : np.ndarray of shape (n, m)
       Various clustering used to compute the disagreement matrix
       There is m clustering of n points
    max_value : int
        Maximal number of clusters
    pi_star : np.ndarray of shape (n)
        Current partition
    weights : np.ndarray of shape (m)
        Weights of each clustering

    Returns
    -------
    np.ndarray of shape (n, max_value)
        Disagreement matrix
    """
    disagreement = np.full(shape=(clusters.shape[0], max_value), fill_value=np.inf)
    for i in range(max_value):
        p_i = pi_star == i

        if p_i.any():
            disagreement[:, i] = np.sum(
                weights[None]
                * np.mean(clusters[:, None] != clusters[None, p_i], axis=1),
                axis=-1,
            )
    return disagreement
