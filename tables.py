import calc
from tkinter import ttk


def prp_seg(d_in, dv):
    seg_tbl = [[] for _ in range(len(d_in['f1']) + 1)]
    u_v = calc.calc_disp(d_in)

    for i, (f_s, f_e, a_s, l_s, e_s, s_m, q_s) in enumerate(zip(d_in['f1'], d_in['f2'], d_in['a'], d_in['l'], d_in['e'], d_in['max'], d_in['q'])):
        u_s, u_e = u_v[i], u_v[i + 1]
        for j in range(dv + 1):
            x = round(float(l_s) / dv * j, 4)
            n_f = calc.force(x, u_s, u_e, float(l_s), float(q_s), float(e_s), float(a_s))
            u_c = calc.disp(x, u_s, u_e, float(l_s), float(q_s), float(e_s), float(a_s))
            s_c = calc.stress(n_f, float(a_s))
            seg_tbl[i + 1].append((x, n_f, u_c, s_c, float(s_m)))

    return seg_tbl[1:]


def show(t, c):
    [w.destroy() for w in c.winfo_children()]

    f = ttk.Frame(c)
    c.create_window((0, 0), window=f, anchor="nw")

    for i, d in enumerate(t):
        ttk.Label(f, text=f"Таблица {i + 1}", font=("Consolas", 12)).grid(row=i * 2, column=0, sticky="w", pady=(10, 0))

        tr = ttk.Treeview(f, columns=("X", "N", "U", "σ", "[σ]"), show="headings", height=6)
        tr.grid(row=i * 2 + 1, column=0, sticky="ew")

        [tr.heading(h, text=h) for h in ("X", "N", "U", "σ", "[σ]")]
        [tr.column(h, width=75, anchor="center") for h in ("X", "N", "U", "σ", "[σ]")]

        tr.tag_configure('alert', background='red')

        for r in d:
            tr.insert("", "end", values=r, tags=("alert",)) if abs(r[-2]) > r[-1] else tr.insert("", "end", values=r)

    f.update_idletasks()
    c.configure(scrollregion=c.bbox("all"))
