from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from io import BytesIO
import warnings


def crt(l, h, p, q, s):
    fig, ax = plt.subplots()
    t_l, t_h = sum(l), sum(h)
    a_h, a_lf = sum(h) / len(h), (sum(l) / len(l)) / 15
    min_l, max_h, min_h = min(l), max(h), min(h)
    x, hlc = 0, []

    for sl, sh in zip(l, h):
        y = max_h / 2 - sh / 2 + max_h * 2.5
        ax.add_patch(plt.Rectangle((x, y), sl, sh, edgecolor='black', facecolor='white'))
        hlc.append((sh, sl, y))
        x += sl

    if s in [1, 3]:
        sy = max(hlc, key=lambda x: x[0])[2] + max_h / 2 - a_h / 2
        ax.arrow(0, sy, 0, a_h, head_width=0, head_length=0, fc='black', ec='black', width=min_l / 1000)
        [plt.arrow(0, sy + i * a_h / 9, -a_lf, -a_h / 15, color='black', head_width=0, head_length=0, width=min_h / 1000)
         for i in range(10)]

    if s in [2, 3]:
        sy = max(hlc, key=lambda x: x[0])[2] + max_h / 2 - a_h / 2
        ax.arrow(t_l, sy, 0, a_h, head_width=0, head_length=0, fc='black', ec='black', width=min_l / 1000)
        [plt.arrow(t_l, sy + i * a_h / 9, a_lf, a_h / 15, color='black', head_width=0, head_length=0, width=min_h / 1000)
         for i in range(10)]

    acc_l = [0] + l
    for i in range(1, len(acc_l)): acc_l[i] += acc_l[i - 1]

    for i, dq in enumerate(q):
        li = i // 2
        y, rh = hlc[li][2], hlc[li][0]
        d = 1 if float(dq) > 0 else -1 if float(dq) < 0 else 0

        if d > 0:
            sx, ex = float(acc_l[i]), float(acc_l[i + 1])
            sl, sp = abs(ex - sx), abs((ex - sx) / 10)
            x = sx
            for _ in range(10):
                plt.arrow(x, y + rh / 2, abs(sp * d - t_l / 100), 0,
                          color='red', head_width=t_h / 20, head_length=t_l / 90,
                          width=min_h / 10000, ec='red')
                x += sp

        elif d < 0:
            sx, ex = float(acc_l[i + 1]), float(acc_l[i])
            sl, sp = abs(ex - sx), abs((ex - sx) / 10)
            x = sx
            for _ in range(10):
                arrow_offset = sp * d + t_l / 100
                arrow_offset = -arrow_offset if arrow_offset > 0 else arrow_offset
                plt.arrow(x, y + rh / 2, arrow_offset, 0,
                          color='red', head_width=t_h / 20, head_length=t_l / 90,
                          width=min_h / 10000, ec='red')
                x -= sp

    for i, f in enumerate(p):
        d = 1 if float(f) > 0 else -1 if float(f) < 0 else 0
        x, y, rh = float(acc_l[i]), hlc[i // 2][2], hlc[i // 2][0]

        if d > 0:
            a = hlc[i][1] if i < len(hlc) else t_l / 4
        elif d == 0:
            continue
        else:
            a = -hlc[i - 1][1] if x != 0 else -t_l / 4

        plt.arrow(x, y + rh / 2, a / 3, 0, color='green', head_width=t_h / 15,
                  head_length=t_l / 20, width=min_h / 10000, ec='green')

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        ax.set_xlim(-sum(l) * 0.15, sum(l) * 1.45)
        ax.set_ylim(0, max_h * 4)
    ax.axis('off')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


def gt(c, l, h, p, q, s):
    img = Image.open(crt(l, h, p, q, s))
    img = ImageTk.PhotoImage(img)
    c.delete("all")
    c.image = img
    c.create_image(-100, -70, anchor='nw', image=img)


def prp(v, sf):
    v = [float(x) for x in v]
    mn, mx = min(v), max(v)
    if mx <= mn * sf:
        return v
    return [mn + (x - mn) * ((mn * sf - mn) / (mx - mn)) for x in v]
