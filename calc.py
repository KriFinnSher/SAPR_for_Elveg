from collections import defaultdict
import numpy as np


def disp(x, d1, d2, l, q, e, a):
    return round(d1 + (x / l) * (d2 - d1) + (q * l ** 2) / (2 * e * a) * (x / l) * (1 - x / l), 4)


def force(x, d1, d2, l, q, e, a):
    return round((e * a / l) * (d2 - d1) + (q * l / 2) * (1 - 2 * x / l), 4)


def stress(f, a):
    return round(f / a, 4)


def load_vec(p, q, l, bc):
    n = len(l) + 2
    v_p, v_q = [0] * n, [0] * n

    for i in p:
        v_p[i] = p[i]
    for i in q:
        v_q[i] += q[i] * l[i] / 2
        v_q[i + 1] += q[i] * l[i] / 2

    v = [v_p[i] + v_q[i] for i in range(n)][1:]
    if bc in [1, 3]: v[0] = 0
    if bc in [2, 3]: v[-1] = 0

    return v


def stiff_mat(mats, bc):
    n = len(mats) + 1
    g = [[0] * n for _ in range(n)]

    for i in range(n - 1):
        for j in range(2):
            for k in range(2):
                g[j + i][k + i] += mats[i][j][k]

    if bc in [1, 3]:
        g[0][0] = 1
        for i in range(1, n):
            g[0][i] = g[i][0] = 0

    if bc in [2, 3]:
        g[-1][-1] = 1
        for i in range(n - 1):
            g[-1][i] = g[i][-1] = 0

    return g


def solve_disp(g, v):
    d = np.linalg.solve(np.array(g), np.array(v))
    return np.round(d, 4).tolist()


def prep_stiff(data):
    mats = []
    f1, f2, a, l, e, s, q = data['f1'], data['f2'], data['a'], data['l'], data['e'], data['max'], data['q']
    rods, em, ca = defaultdict(float), defaultdict(float), defaultdict(float)

    for i, rod in enumerate(zip(f1, f2, a, l, e, s, q)):
        rods[i + 1], em[i + 1], ca[i + 1] = float(rod[3]), float(rod[4]), float(rod[2])

    for i in range(1, len(f1) + 1):
        k = em[i] * ca[i] / rods[i]
        mats.append([[k, -k], [-k, k]])

    return mats


def calc_disp(data):
    f1, f2, a, l, e, s, q = data['f1'], data['f2'], data['a'], data['l'], data['e'], data['max'], data['q']
    rods = {i + 1: float(rod[3]) for i, rod in enumerate(zip(f1, f2, a, l, e, s, q))}
    q_dict = {i + 1: float(rod[-1]) for i, rod in enumerate(zip(f1, f2, a, l, e, s, q))}
    p_dict = defaultdict(float)

    for i in range(len(f1)):
        p_dict[i + 1] += float(f1[i])
    for i in range(len(f2)):
        p_dict[i + 2] += float(f2[i])

    v = load_vec(p_dict, q_dict, rods, data['z'][0])
    k = stiff_mat(prep_stiff(data), data['z'][0])

    return solve_disp(k, v)
