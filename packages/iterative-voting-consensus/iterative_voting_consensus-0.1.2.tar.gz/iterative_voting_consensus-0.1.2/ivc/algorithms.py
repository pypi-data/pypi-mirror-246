import numpy as np
from tqdm import trange

from ivc.utils import (
    compute_majority_disagreement,
    compute_probabilistic_disagreement,
    random_initialization,
)


def iterative_probabilistic_voting_consensus(
    clusters: np.ndarray,
    max_value: int,
    n_iter: int = 5,
    tol: float = 0.1,
    verbose: bool = True,
    pi_init: np.ndarray | None = None,
    weights: np.ndarray | None = None,
) -> np.ndarray:
    """Iterative Probabilistic Voting Consensus Algorithm.

    Parameters
    ----------
    clusters : np.ndarray of shape (n, m)
        Various clustering used to compute the disagreement matrix
        There is m clustering of n points
    max_value : int
        Maximal number of clusters
    n_iter : int, optional
        Maximal number of iterations, by default 5
    tol : float, optional
        Tolerance for the convergence criterion.
        Maximum number of not fixed point to stop the algorithm, by default 0.1
    verbose : bool, optional
        Show the TQDM progress bar, by default True
    pi_init : np.ndarray | None, optional
        Initialization of the partition, by default None
    weights : np.ndarray | None, optional
        Weights of each clustering, by default None
        If None, the weigths of each clusterings are equals.

    Returns
    -------
    np.ndarray
        _description_
    """
    if verbose:
        pbar = trange(n_iter)
    else:
        pbar = range(n_iter)

    if pi_init is None:
        pi_star = random_initialization(n_value=clusters.shape[0], max_value=max_value)
    else:
        pi_star = pi_init.copy()

    if weights is None:
        weights = np.ones(clusters.shape[1])

    for _ in pbar:
        disagreement = compute_probabilistic_disagreement(
            clusters, max_value, pi_star, weights
        )
        fixed_points = np.mean(pi_star == np.argmin(disagreement, axis=-1))
        pi_star = np.argmin(disagreement, axis=-1)

        if verbose:
            pbar.set_description(f"Percentage of fixed points {fixed_points}")  # type: ignore

        if 1 - fixed_points < tol:
            break

    return pi_star


def iterative_voting_consensus(
    clusters: np.ndarray,
    max_value: int,
    n_iter: int = 5,
    tol: float = 0.1,
    verbose: bool = True,
    pi_init: np.ndarray | None = None,
    weights: np.ndarray | None = None,
) -> np.ndarray:
    """Iterative Probabilistic Voting Consensus Algorithm.

    Parameters
    ----------
    clusters : np.ndarray of shape (n, m)
        Various clustering used to compute the disagreement matrix
        There is m clustering of n points
    max_value : int
        Maximal number of clusters
    n_iter : int, optional
        Maximal number of iterations, by default 5
    tol : float, optional
        Tolerance for the convergence criterion.
        Maximum number of not fixed point to stop the algorithm, by default 0.1
    verbose : bool, optional
        Show the TQDM progress bar, by default True
    pi_init : np.ndarray | None, optional
        Initialization of the partition, by default None
    weights : np.ndarray of shape (m)| None, optional
        Weights of each clustering, by default None
        If None, the weigths of each clusterings are equals.

    Returns
    -------
    np.ndarray of shape (n)
        Optimal partition found
    """
    if verbose:
        pbar = trange(n_iter)
    else:
        pbar = range(n_iter)

    if pi_init is None:
        pi_star = random_initialization(n_value=clusters.shape[0], max_value=max_value)
    else:
        pi_star = pi_init.copy()

    if weights is None:
        weights = np.ones(clusters.shape[1])

    for _ in pbar:
        disagreement = compute_majority_disagreement(
            clusters, max_value, pi_star, weights
        )
        fixed_points = np.mean(pi_star == np.argmin(disagreement, axis=-1))
        pi_star = np.argmin(disagreement, axis=-1)

        if verbose:
            pbar.set_description(f"Percentage of fixed points {fixed_points}")  # type: ignore

        if 1 - fixed_points < tol:
            break

    return pi_star
