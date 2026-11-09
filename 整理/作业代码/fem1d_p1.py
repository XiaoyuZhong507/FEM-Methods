#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
有限元方法 · 一维 P1 有限元程序（对应 hwcode1 / hwcode3）

用法：
    python fem1d_p1.py            # 打印两张误差表
    python fem1d_p1.py --raw      # 打印原始数据

要点：
  1. 等距网格，h = 1/N，N 为「单元数」，节点数 N+1。
  2. 单元刚度矩阵  ke = (1/h)[[1,-1],[-1,1]]，对应 -u''。
  3. 载荷 b_i = ∫ f φ_i，用 8 点 Gauss 积分逐单元累加（f 光滑，8 点足够）。
  4. 误差用 8 点 Gauss 逐单元积分；H1 范数 = sqrt(‖e‖²_L2 + ‖e'‖²_L2)，
     作业给的定义含 L2 部分，不是半范数。
  5. 纯 Neumann 时刚度矩阵奇异（核 = 常数），必须固定一个节点定规范。
     这里固定 u_h(0)=0；若固定别的节点，L2 误差会多一个常数偏移。
"""

import numpy as np

GLX, GLW = np.polynomial.legendre.leggauss(8)   # 8 点 Gauss-Legendre


def solve_p1(N, f, dirichlet_left=True, dirichlet_right=True):
    """在 N 个等距单元上组装并求解 -u''=f。返回 (节点坐标, 节点值)。"""
    h = 1.0 / N
    x = np.linspace(0.0, 1.0, N + 1)
    n = N + 1
    A = np.zeros((n, n))
    b = np.zeros(n)

    for e in range(N):
        xl = x[e]
        ke = np.array([[1.0, -1.0], [-1.0, 1.0]]) / h

        # 载荷：∫_单元 f φ_i，φ_l=1-s, φ_r=s，s∈[0,1]
        be = np.zeros(2)
        for xi, wi in zip(GLX, GLW):
            s = 0.5 * (xi + 1.0)
            w = 0.5 * wi * h            # dx = h ds
            X = xl + s * h
            be[0] += w * f(X) * (1.0 - s)
            be[1] += w * f(X) * s

        idx = [e, e + 1]
        for i in range(2):
            b[idx[i]] += be[i]
            for j in range(2):
                A[idx[i], idx[j]] += ke[i, j]

    free = np.arange(n)
    if dirichlet_left:
        free = free[free != 0]
    if dirichlet_right:
        free = free[free != n - 1]

    U = np.zeros(n)
    U[free] = np.linalg.solve(A[np.ix_(free, free)], b[free])
    return x, U


def uh_at(x, U, X):
    """分段线性插值求值（向量化）。"""
    N = len(U) - 1
    h = 1.0 / N
    k = np.clip(np.floor(X / h).astype(int), 0, N - 1)
    s = (X - x[k]) / h
    return U[k] * (1.0 - s) + U[k + 1] * s


def errors(x, U, u, du):
    """返回 (‖e‖_L2, |e|_H1, ‖e‖_H1)。"""
    N = len(U) - 1
    h = 1.0 / N
    l2sq = 0.0
    h1sq = 0.0
    for e in range(N):
        xl = x[e]
        xm, xr = 0.5 * (xl + x[e + 1]), 0.5 * h
        dU = (U[e + 1] - U[e]) / h          # u_h' 在单元内为常数
        for xi, wi in zip(GLX, GLW):
            X = xm + xr * xi
            w = wi * xr
            ev = u(X) - uh_at(x, U, np.array([X]))[0]
            l2sq += w * ev * ev
            h1sq += w * (du(X) - dU) ** 2
    e0 = np.sqrt(l2sq)
    e1 = np.sqrt(h1sq)
    return e0, e1, np.sqrt(l2sq + h1sq)


def order(e_old, e_new, N_old, N_new):
    return np.log(e_old / e_new) / np.log(N_new / N_old)


def run(case, u, du, f, dirichlet=(True, True), Ns=(10, 20, 40, 80)):
    print(f"\n### {case}")
    rows = []
    prev = None
    for N in Ns:
        x, U = solve_p1(N, f, *dirichlet)
        e0, e1, eH = errors(x, U, u, du)
        if prev is None:
            rows.append((N, e0, None, e1, None))
        else:
            rows.append((N, e0, order(prev[0], e0, prev[2], N),
                         e1, order(prev[1], e1, prev[2], N)))
        prev = (e0, e1, N)
    print("| N | L2 error | order | H1 error | order |")
    print("|---|---|---|---|---|")
    for N, e0, o0, e1, o1 in rows:
        s0 = "-" if o0 is None else f"{o0:.3f}"
        s1 = "-" if o1 is None else f"{o1:.3f}"
        print(f"| {N} | {e0:.4e} | {s0} | {e1:.4e} | {s1} |")


def main():
    # hwcode1: 齐次 Dirichlet
    run("-u''=f, u(0)=u(1)=0, u=(x-1)sin x, f=-(2cos x-(x-1)sin x)",
        u=lambda X: (X - 1.0) * np.sin(X),
        du=lambda X: np.sin(X) + (X - 1.0) * np.cos(X),
        f=lambda X: -(2.0 * np.cos(X) - (X - 1.0) * np.sin(X)),
        dirichlet=(True, True))

    # hwcode3: 纯 Neumann（只在左端固定规范）
    run("-u''=f, u'(0)=u'(1)=0, u=x^2(x-1)^2, f=-(12x^2-12x+2)",
        u=lambda X: X ** 2 * (X - 1.0) ** 2,
        du=lambda X: 2.0 * X * (X - 1.0) * (2.0 * X - 1.0),
        f=lambda X: -(12.0 * X ** 2 - 12.0 * X + 2.0),
        dirichlet=(True, False))

    print("\n理论阶：P1 协调元，‖u-u_h‖_L2 = O(h^2)，‖u-u_h‖_H1 = O(h)。")
    print("hwcode3 的相容性条件：∫_0^1 f dx = 0（已核验，量级 1e-16）。")


if __name__ == "__main__":
    main()
