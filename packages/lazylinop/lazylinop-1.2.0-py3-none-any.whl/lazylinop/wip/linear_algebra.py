"""
Module for linear algebra related LazyLinearOps.
"""
try:
    import dask
    from dask.distributed import Client, LocalCluster, wait
except ImportError:
    print("Dask ImportError")
from lazylinop import *
try:
    import numba as nb
    from numba import njit, prange, set_num_threads, threading_layer
    nb.config.THREADING_LAYER = 'omp'
    _T = nb.config.NUMBA_NUM_THREADS
except ImportError:
    print('Did not find Numba.')
import numpy as np
import scipy as sp
import warnings
warnings.simplefilter(action='always')


@njit(parallel=False, cache=True)
def mm(A: np.ndarray, B: np.ndarray, M: int, K: int, N: int, swap_kn: bool=False):
    C = np.full(M * N, 0 * (A[0] * B[0]))
    if swap_kn:
        for m in range(M):
            for k in range(K):
                for n in range(N):
                    C[m * N + n] += A[m * K + k] * B[k * N + n]
    else:
        for m in range(M):
            for n in range(N):
                tmp = 0.0
                for k in range(K):
                    tmp += A[m * K + k] * B[k * N + n]
                C[m * N + n] = tmp
    return C


def khatri_rao(A, B, column: bool=True, method: str='lazylinop'):
    """Constructs a Khatri-Rao product lazy linear operator K.
    Khatri-Rao product is a column-wize Kronecker product we denotes c*
    while the row-wize product is r*.
    If A and B are two matrices then (A c* B)^T = A^T r* B^T.
    Therefore, we easily get the adjoint of the row-wize Kronecker product.
    If matrix A in R^{m x n} and B in R^{p x n}, the Khatri-Rao product
    matrix is in R^{(m * p) x n}. The function does not explicitly compute
    the matrix. It uses the trick (A c* B) @ x = vec(B @ diag(x) @ A.T)
    where x is a vector of length n and diag(x) a diagonal matrix of size n * n.
    Therefore, we save m * p * n - n * n of memory if m * p > n.

    Args:
        A:
        First matrix, it can be LazyLinearOp or NumPy array
        B:
        Second matrix, it can be LazyLinearOp or NumPy array
        column: bool, optional
        Compute Khatri-Rao product column-wize (True is default)
        If False, compute row-wize product
        method: str, optional
        If 'scipy' uses SciPy Khatri-Rao product

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            number of rows differs.
        ValueError
            number of columns differs.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.wip.linear_algebra import khatri_rao
        >>> M1 = np.full((2, 2), 1)
        >>> M2 = np.eye(3, M=2, k=0)
        >>> x = np.random.rand(2)
        >>> K = khatri_rao(M1, M2)
        >>> S = sp.linalg.khatri_rao(M1, M2)
        >>> np.allclose(K @ x, S @ x)
        True

    References:
        See also `scipy.linalg.khatri_rao <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.khatri_rao.html>`_.
    """

    Ma, Na = A.shape[0], A.shape[1]
    Mb, Nb = B.shape[0], B.shape[1]

    if not column and Ma != Mb:
        raise ValueError("number of rows differs.")

    if column and Na != Nb:
        raise ValueError("number of columns differs.")

    shape = (Ma * Mb, Na) if column else (Ma, Na * Nb)

    # Compute number of operations for lazylinop (B @ diag(x) @ A.T)
    # and for SciPy and return the best method
    def _nops(A, B, x):
        m, k = B.shape
        k, n = x.shape[0], x.shape[0]
        n, p = A.T.shape
        batch_size = 1 if x.ndim == 1 else x.shape[1]
        # # Left to right or right to left multiplication ?
        # ltor = (m * k * n + m * n * p + k + m * p) * batch_size + k ** 2
        # rtol = (m * k * p + k * n * p + k + m * p) * batch_size + k ** 2
        # # SciPy computes the Khatri-Rao matrix K and then computes K @ X
        # nops = A.shape[0] * B.shape[0] * A.shape[1] * (1 + batch_size)
        # print(nops / max(ltor, rtol), 'lazylinop' if nops >  max(ltor, rtol) else 'scipy')
        # return 'lazylinop' if nops > min(ltor, rtol) else 'scipy'
        # Memory: lazylinop creates batch size diagonal matrix (k, k)
        # while SciPy creates Khatri-Rao product matrix (A.shape[0] * B.shape[0], A.shape[1])
        # print('batch size={0:d} {1:s}'.format(batch_size, 'lazylinop' if (A.shape[0] * B.shape[0] * A.shape[1]) > ((k ** 2 + m * p) * batch_size) else 'scipy'))
        return 'lazylinop' if (A.shape[0] * B.shape[0] * A.shape[1]) > ((k ** 2 + m * p) * batch_size) else 'scipy'

    def _2d(A, B, x, column):
        Ma, Na = A.shape[0], A.shape[1]
        Mb, Nb = B.shape[0], B.shape[1]
        if isLazyLinearOp(x):
            x = np.eye(x.shape[0], M=x.shape[0], k=0) @ x
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        Y = np.full((Ma * Mb if column else Ma, batch_size), 0.0 * (A[0, 0] * B[0, 0] * x[0, 0]))
        if column:
            # We use (A c* B) @ x = vec(B @ diag(x) @ A^T)
            # and a ravel with order='F' (does not work with Numba)
            for i in range(batch_size):
                m, k = B.shape
                k, n = x.shape[0], x.shape[0]
                n, p = A.T.shape
                ltor = m * k * n + m * n * p
                rtol = m * k * p + k * n * p
                # Save diagonal matrix creation
                if i == 0:
                    D = np.diag(x[:, i])
                else:
                    np.fill_diagonal(D, val=x[:, i])
                # Minimize the number of operations
                if ltor < rtol:
                    Y[:, i] = ((B @ D) @ A.T).ravel(order='F')
                else:
                    Y[:, i] = (B @ (D @ A.T)).ravel(order='F')
        else:
            for i in range(batch_size):
                for r in range(Ma):
                    Y[r, i] = A[r, :] @ (B[r, :] @ x[:, i].reshape(A.shape[1], B.shape[1]).T).T
        return Y.ravel() if is_1d else Y
        
    # We use (A c* B)^T = A^T r* B^T to compute the adjoint.
    return LazyLinearOp(
        shape=shape,
        matmat=lambda x: sp.linalg.khatri_rao(
            np.eye(A.shape[0], M=A.shape[0], k=0) @ A if isLazyLinearOp(A) else A,
            np.eye(B.shape[0], M=B.shape[0], k=0) @ B if isLazyLinearOp(B) else B
        ) @ x if column and (_nops(A, B, x) == 'scipy' or method == 'scipy') else _2d(A, B, x, column),
        rmatmat=lambda x : _2d(A.T.conj(), B.T.conj(), x, not column)
    )


def expm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs exponentiation of linear operator L as a lazy linear operator E(L).
    Of note, it is only an approximation E(L) @ X ~= sum((scale * L)^i / factorial(i), i=0 to nmax) @ X.

    Args:
        L: 2d array
            Linear operator.
        scale: float, optional
            Scale factor expm(scale * L) (default is 1).
        nmax: int, optional
            Stop the serie expansion after nmax (default is 8).
        backend: str, optional
            It can be 'scipy' (default) to use scipy.linalg.expm function.
            nmax parameter is useless if backend is 'scipy'.
            It can be 'serie' to use a serie expansion of expm(scale * L).
        use_numba: bool, optional
            If True, use prange from Numba (default is False)
            to compute batch in parallel.
            It is useful only and only if the batch size and
            the length of a are big enough.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import expm
        >>> scale = 0.01
        >>> coefficients = np.array([1.0, scale, 0.5 * scale ** 2])
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = expm(L, scale=scale, nmax=4)
        >>> E2 = sp.linalg.expm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.expm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.expm.html>`_.
        See also :py:func:`lazylinop.wip.polynomial.polyval`.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        if use_numba:
            M = sp.linalg.expm(scale * L)
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            @njit(nopython=True, parallel=True, cache=True)
            def _matmat(M, x):
                if x.ndim == 1:
                    is_1d = True
                    batch_size = 1
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((M.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = M @ X[:, b]
                else:
                    y = M @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(M, X),
                rmatmat=lambda X: _matmat(M.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.expm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.expm(scale * L.T.conj()) @ X
            )
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: sp.linalg.expm(scale * L) @ X,
            rmatmat=lambda X: sp.linalg.expm(scale * L.T.conj()) @ X
        )
    elif backend == 'serie':
        from lazylinop.wip.polynomial import polyval
        coefficients = np.empty(nmax + 1, dtype=np.float64)
        factor = 1.0
        factorial = 1.0
        for i in range(nmax + 1):
            coefficients[i] = factor / factorial
            factor *= scale
            factorial *= (i + 1)
        return polyval(coefficients, L)
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def logm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: str=False):
    """Constructs logarithm of linear operator L as a lazy linear operator Log(L).
    Of note, it is only an approximation Log(L) @ X ~= sum((-1)^(n + 1) * (L - Id)^n / n, n=1 to nmax) @ X.

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor logm(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.logm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of logm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            nmax must be >= 1.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import logm
        >>> scale = 0.01
        >>> N = 10
        >>> E1 = logm(eye(N, n=N, k=0), scale=scale, nmax=4, backend='scipy')
        >>> E2 = sp.linalg.logm(scale * np.eye(N, M=N, k=0))
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E1 @ X, E2 @ X)

    References:
        See also `scipy.linalg.logm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.logm.html>`_.
        See also `logarithm of a matrix <https://en.wikipedia.org/wiki/Logarithm_of_a_matrix>`_.
    """
    if True or backend == 'scipy':
        # backend has to be 'scipy' because 'serie' is not precise enough
        if isLazyLinearOp(L):
            L = np.eye(L.shape[0], M=L.shape[0]) @ L
        if use_numba:
            M = sp.linalg.logm(scale * L)
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            @njit(nopython=True, parallel=True, cache=True)
            def _matmat(M, x):
                if x.ndim == 1:
                    is_1d = True
                    batch_size = 1
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((M.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = M @ X[:, b]
                else:
                    y = M @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(M, X),
                rmatmat=lambda X: _matmat(M.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.logm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.logm(scale * L.T.conj()) @ X
            )
    elif backend == 'serie':
        if nmax < 1:
            raise ValueError("nmax must be >= 1.")
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                batch_size = 1
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            Lx = np.empty(L.shape[0], dtype=x.dtype)
            # Taylor expansion
            # It uses the equation log(scale * L) ~= sum((-1)^(n + 1) * (scale * L - Id)^n / n, n=1 to nmax)
            y = np.subtract(np.multiply(scale, L @ x), x)
            if nmax > 2:
                # loop over the batch size
                for b in range(batch_size):
                    # compute (scale * L - Id) @ x
                    np.subtract(np.multiply(scale, L @ x[:, b]), x[:, b], out=Lx)
                    for n in range(2, nmax):
                        factor = (2 * (n % 2) - 1) / n
                        np.add(y[:, b], np.multiply(factor, Lx), out=y[:, b])
                        np.subtract(np.multiply(scale, L @ Lx), Lx, out=Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def cosm(L, scale: float=1.0, nmax: int=8, backend: str='scipy'):
    """Constructs a cosinus of linear operator L as a lazy linear operator C(L).
    It uses the equation expm(i * scale * L) = cos(scale * L) + i * sin(scale * L)
    where i^2 = -1 and returns real part.
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosm(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.cosm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of cosm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import cosm
        >>> scale = 0.01
        >>> coefficients = np.array([1.0, scale, 0.5 * scale ** 2])
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = cosm(L, scale=scale, nmax=4)
        >>> E2 = sp.linalg.cosm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.cosm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cosm.html>`_.
        See also :py:func:`expm`.
        See also :py:func:`lazylinop.wip.polynomial.polyval`.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: sp.linalg.cosm(scale * L) @ X,
            rmatmat=lambda X: sp.linalg.cosm(scale * L.T.conj()) @ X
        )
    elif backend == 'serie':
        from lazylinop.wip.polynomial import polyval
        coefficients = np.empty(nmax + 1, dtype=np.float64)
        factor = 1.0
        sign = 1
        for i in range(nmax + 1):
            if (i % 2) == 0:
                coefficients[i] = sign * factor
                sign *= -1
            else:
                coefficients[i] = 0.0
            factor *= scale / (i + 1)
        return polyval(coefficients, L)
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def sinm(L, scale: float=1.0, nmax: int=8, backend: str='scipy'):
    """Constructs a cosinus of linear operator L as a lazy linear operator C(L).
    It uses the equation expm(i * scale * L) = cos(scale * L) + i * sin(scale * L)
    where i^2 = -1 and returns imaginary part.
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor sinm(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.sinm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of sinm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import sinm
        >>> scale = 0.01
        >>> coefficients = np.array([1.0, scale, 0.5 * scale ** 2])
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = sinm(L, scale=scale, nmax=4)
        >>> E2 = sp.linalg.sinm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.sinm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sinm.html>`_.
        See also :py:func:`expm`.
        See also :py:func:`lazylinop.wip.polynomial.polyval`.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: sp.linalg.sinm(scale * L) @ X,
            rmatmat=lambda X: sp.linalg.sinm(scale * L.T.conj()) @ X
        )
    elif backend == 'serie':
        from lazylinop.wip.polynomial import polyval
        coefficients = np.empty(nmax + 1, dtype=np.float64)
        factor = 1.0
        sign = 1
        for i in range(nmax + 1):
            if (i % 2) == 1:
                coefficients[i] = sign * factor
                sign *= -1
            else:
                coefficients[i] = 0.0
            factor *= scale / (i + 1)
        return polyval(coefficients, L)
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def coshm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs an hyperbolic cosine of linear operator L as a lazy linear operator C(L).
    It uses the equation 2 * cosh(z) = exp(scale * L) + exp(-scale * L).
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosh(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.coshm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of coshm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            nmax must be >= 1.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import coshm
        >>> scale = 0.01
        >>> N = 10
        >>> L = np.eye(N, M=N, k=0)
        >>> E1 = coshm(L, scale=scale, nmax=32, backend='serie')
        >>> E2 = sp.linalg.coshm(scale * L)
        >>> E3 = coshm(eye(N, n=N, k=0), scale=scale, nmax=32, backend='serie')
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E1 @ X, E2 @ X)
        True
        >>> np.allclose(E2 @ X, E3 @ X)
        True

    References:
        See also `scipy.linalg.coshm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.coshm.html>`_.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):
            L = np.eye(L.shape[0], M=L.shape[0]) @ L
        if use_numba:
            C = sp.linalg.coshm(scale * L) @ X
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            @njit(nopython=True, parallel=True, cache=True)
            def _matmat(C, x):
                if x.ndim == 1:
                    is_1d = True
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((C.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = C @ X[:, b]
                else:
                    y = C @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(C, X),
                rmatmat=lambda X: _matmat(C.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.coshm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.coshm(scale * L.T.conj()) @ X
            )
    elif backend == 'serie':
        if nmax < 1:
            raise ValueError("nmax must be >= 1.")
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            y = np.copy(x)
            # Taylor expansion
            # exp(scale * L) ~= Id + scale * L + (scale * L) ** 2 / 2 + ...
            # exp(-scale * L) ~= Id - scale * L + (scale * L) ** 2 / 2 + ...
            # cosh(scale * L) ~= Id + (scale * L) ** 2 / 2 + ...
            if nmax > 1:
                Lx = np.empty(L.shape[0], dtype=x.dtype)
                # loop over the batch size
                for b in range(batch_size):
                    pfactor = scale
                    mfactor = -scale
                    np.copyto(Lx, L @ x[:, b])
                    for i in range(1, nmax):
                        if (i % 2) == 0:
                            np.add(y[:, b], np.multiply(0.5 * (pfactor + mfactor), Lx), out=y[:, b])
                        pfactor *= scale / (i + 1)
                        mfactor *= -scale / (i + 1)
                        np.copyto(Lx, L @ Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def sinhm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs an hyperbolic cosine of linear operator L as a lazy linear operator S(L).
    It uses the equation 2 * sinh(z) = exp(scale * L) - exp(-scale * L).
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosh(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.sinhm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of sinhm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import sinhm
        >>> scale = 0.01
        >>> N = 10
        >>> L = np.eye(N, M=N, k=0)
        >>> E1 = sinhm(L, scale=scale, nmax=32, backend='serie')
        >>> E2 = sp.linalg.sinhm(scale * L)
        >>> E3 = sinhm(eye(N, n=N, k=0), scale=scale, nmax=32, backend='serie')
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E1 @ X, E2 @ X)
        True
        >>> np.allclose(E2 @ X, E3 @ X)
        True

    References:
        See also `scipy.linalg.sinhm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sinhm.html>`_.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):
            L = np.eye(L.shape[0], M=L.shape[0]) @ L
        if use_numba:
            S = sp.linalg.sinhm(scale * L) @ X
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            @njit(nopython=True, parallel=True, cache=True)
            def _matmat(S, x):
                if x.ndim == 1:
                    is_1d = True
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((S.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = S @ X[:, b]
                else:
                    y = S @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(S, X),
                rmatmat=lambda X: _matmat(S.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.sinhm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.sinhm(scale * L.T.conj()) @ X
            )
    elif backend == 'serie':
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            y = np.zeros((L.shape[0], batch_size), dtype=x.dtype)
            Lx = np.empty(L.shape[0], dtype=x.dtype)
            # loop over the batch size
            for b in range(batch_size):
                # Taylor expansion
                # exp(scale * L) ~= Id + scale * L + (scale * L) ** 2 / 2 + ...
                # exp(-scale * L) ~= Id - scale * L + (scale * L) ** 2 / 2 + ...
                # sinh(scale * L) ~= scale * L + ...
                pfactor = scale
                mfactor = -scale
                if nmax > 1:
                    np.copyto(Lx, L @ x[:, b])
                    for i in range(1, nmax):
                        if (i % 2) == 1:
                            np.add(y[:, b], np.multiply(0.5 * (pfactor - mfactor), Lx), out=y[:, b])
                        pfactor *= scale / (i + 1)
                        mfactor *= -scale / (i + 1)
                        np.copyto(Lx, L @ Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def sqrtm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs square root of linear operator L as a lazy linear operator R(L).
    It uses the equation L^1/2 = sum((-1)^n * (1/2 n) * (Id - L)^n, n=0 to inf).
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosh(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.sqrtm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of sqrtm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import sqrtm
        >>> scale = 0.01
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = sqrtm(L, scale=scale, nmax=4, backend='serie')
        >>> E2 = sp.linalg.sqrtm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.sqrtm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sqrtm.html>`_.
    """
    if True or backend == 'scipy':
        # backend has to be 'scipy' because 'serie' is not precise enough
        if isLazyLinearOp(L):
            R = sp.linalg.sqrtm(scale * np.eye(L.shape[0], M=L.shape[0]) @ L) @ X
        else:
            R = sp.linalg.sqrtm(scale * L) @ X
        nb.config.DISABLE_JIT = 0 if use_numba else 1
        @njit(nopython=True, parallel=True, cache=True)
        def _matmat(R, x):
            if x.ndim == 1:
                is_1d = True
                batch_size = 1
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            if use_numba:
                y = np.empty((R.shape[0], batch_size), dtype=x.dtype)
                for b in prange(batch_size):
                    y[:, b] = R @ X[:, b]
            else:
                y = R @ X
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(R, X),
            rmatmat=lambda X: _matmat(R.T.conj(), X)
        )
        # return LazyLinearOp(
        #     shape=L.shape,
        #     matmat=lambda X: sp.linalg.sqrtm(scale * L) @ X,
        #     rmatmat=lambda X: sp.linalg.sqrtm(scale * L.T.conj()) @ X
        # )
    elif backend == 'serie':
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                batch_size = 1
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            Lx = np.empty(L.shape[0], dtype=x.dtype)
            # Taylor expansion
            # It uses the equation (scale * L)^1/2 = sum((-1)^n * (1/2 n) * (Id - scale * L)^n, n=0 to inf)
            y = np.copy(x)
            if nmax > 1:
                # loop over the batch size
                for b in range(batch_size):
                    # compute (Id - scale * L) @ x
                    np.subtract(x[:, b], np.multiply(scale, L @ x[:, b]), out=Lx)
                    for n in range(1, nmax):
                        # factor = (1 - 2 * (n % 2)) * sp.special.comb(0.5, n)
                        factor = (1 - 2 * (n % 2)) * sp.special.binom(0.5, n)
                        np.add(y[:, b], np.multiply(factor, Lx), out=y[:, b])
                        np.subtract(Lx, np.multiply(scale, L @ Lx), out=Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")
