import math

import numpy as np
from scipy.linalg import expm, logm


def _SUn_generator(n: int, i: int) -> tuple[np.ndarray, int | float | complex]:
    assert n > 1 and 0 <= i < n**2

    if i == 0:
        return np.eye(n, dtype=np.int8), 1
    mat = np.zeros((n, n), dtype=np.int8)

    k = math.isqrt(i)
    l = (i - k**2) // 2
    A = -1 if (i - k**2) % 2 else 1

    if k != l:
        mat[k, l] = 1
        if A == 1:
            mat[l, k] = 1
        else:
            mat[l, k] = -1
    else:
        for j in range(k):
            mat[j, j] = 1
        mat[k, k] = -k
        A = k * (k + 1) // 2

    return mat, A


class SU():
    """
    Special unitary group
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("n must be positive")
        self.n = n

    def __getitem__(self, i: int):
        if not 0 <= i < self.n**2:
            raise IndexError(f"i must be in [0, {self.n**2-1}]")
        mat, A = _SUn_generator(self.n, i)
        if A == -1:
            return 1j * mat
        else:
            return mat / np.sqrt(A)

    def __repr__(self):
        return f"SU({self.n})"

    def __contains__(self, mat):
        if not isinstance(mat, np.ndarray):
            return False
        if mat.shape != (self.n, self.n):
            return False
        if not np.allclose(mat @ mat.conj().T, np.eye(self.n)):
            return False
        if not np.allclose(np.linalg.det(mat), 1):
            return False
        return True

    def angles(self, mat):
        """
        mat = expm(1j*sum(angles[i]*self[i]))
        """
        if not self.__contains__(mat):
            raise ValueError(f"mat is not in SU({self.n})")
        A = logm(mat) / 1j
        angles = []
        for i in range(1, self.n**2):
            angles.append(np.trace(A @ self[i]).real / 2)
        return np.array(angles)

    def __call__(self, angles):
        """
        mat = expm(1j*sum(angles[i]*self[i]))
        """
        if len(angles) != self.n**2 - 1:
            raise ValueError(f"angles must be of length {self.n**2-1}")
        return expm(1j * sum(angles[i - 1] * self[i]
                             for i in range(1, self.n**2)))

    def random(self):
        n = self.n**2 - 1
        vec = np.random.randn(n)
        vec = vec / np.linalg.norm(vec)
        radius = np.random.rand()**(1.0 / n)
        angles = 2 * np.pi * radius * vec
        return self(angles)
