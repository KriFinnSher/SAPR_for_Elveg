import json
import tkinter as tk
from collections import defaultdict
from tkinter import messagebox, filedialog

import checks
import picture
import tables


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("САПР")
        self.geometry("950x500")
        self.resizable(False, False)
        self.lines = []
        self.usrd = defaultdict(list)
        self.c1 = (self.register(checks.ch1), '%P')
        self.c2 = (self.register(checks.ch2), '%P')
        self.c3 = (self.register(checks.ch3), '%P')

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # === Секция "Схема" ===
        frame_scheme = tk.LabelFrame(main_frame, text="Схема", padx=5, pady=5)
        frame_scheme.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        canvas = tk.Canvas(frame_scheme)
        scrollbar = tk.Scrollbar(frame_scheme, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        headers = ["F нач.", "F кон.", "A", "L", "E", "[σ]", "q"]
        for i, text in enumerate(headers):
            tk.Label(self.scroll_frame, text=text).grid(row=0, column=i+1, padx=5, pady=2)

        main_line = []
        l = tk.Label(self.scroll_frame, text="Стержень 1")
        l.grid(row=1, column=0, padx=5, pady=2)
        main_line.append(l)
        entries = [tk.Entry(self.scroll_frame, width=5, validate='all') for _ in range(7)]
        for e in range(len(entries)):
            if e in (0, 1, 6):
                entries[e].config(validatecommand=self.c3)
            else:
                entries[e].config(validatecommand=self.c2)
        main_line.extend(entries)
        self.lines.append(main_line)
        for i, entry in enumerate(entries):
            entry.grid(row=1, column=i+1, padx=5, pady=2)

        btn_plus = tk.Button(self.scroll_frame, text="+", width=3, command=lambda: self.add_line())
        btn_minus = tk.Button(self.scroll_frame, text="-", width=3, command=lambda: self.del_line())
        btn_plus.grid(row=1, column=8, padx=5)
        btn_minus.grid(row=1, column=9, padx=5)

        # === Секция "Опоры" ===
        frame_supports = tk.LabelFrame(main_frame, text="Опоры", padx=5, pady=5)
        frame_supports.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.support_var = tk.IntVar(value=1)

        tk.Radiobutton(frame_supports, text="Опора слева", variable=self.support_var, value=1).pack(anchor="w")
        tk.Radiobutton(frame_supports, text="Опора справа", variable=self.support_var, value=2).pack(anchor="w")
        tk.Radiobutton(frame_supports, text="Обе опоры", variable=self.support_var, value=3).pack(anchor="w")

        # === Секция "Файл" ===
        frame_file = tk.LabelFrame(main_frame, text="Файл", padx=5, pady=5)
        frame_file.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        btn_open = tk.Button(frame_file, text="Открыть", command=lambda: self.file_open())
        btn_save = tk.Button(frame_file, text="Сохранить", command=lambda: self.file_save())
        btn_open.pack(padx=5, pady=(45, 5))
        btn_save.pack(padx=5, pady=5)

        # === Секция "Изображение" ===
        frame_image = tk.LabelFrame(main_frame, text="Изображение", padx=5, pady=5)
        frame_image.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        btn_show_image = tk.Button(frame_image, text="Показать", command=lambda: self.pic())
        btn_show_image.pack(pady=5)

        self.canvas_image = tk.Canvas(frame_image, bg="white", width=280, height=300, relief="solid")
        self.canvas_image.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # === Секция "Расчеты" ===
        frame_calc = tk.LabelFrame(main_frame, text="Расчеты", padx=5, pady=5)
        frame_calc.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        btn_show_calc = tk.Button(frame_calc, text="Показать", command=lambda: self.make_calc())
        btn_show_calc.pack(pady=5)

        self.canvas_calc = tk.Canvas(frame_calc, bg="white", width=280, height=350, relief="solid")
        self.canvas_calc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.scrollbar_calc = tk.Scrollbar(frame_calc, orient="vertical", command=self.canvas_calc.yview)
        self.scrollbar_calc.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_calc.configure(yscrollcommand=self.scrollbar_calc.set)

        self.frame_calc_inner = tk.Frame(self.canvas_calc)
        self.canvas_calc.create_window((0, 0), window=self.frame_calc_inner, anchor="nw")

        self.frame_calc_inner.bind("<Configure>",
                                   lambda x: self.canvas_calc.configure(scrollregion=self.canvas_calc.bbox("all")))

        main_frame.rowconfigure(0, weight=2)
        main_frame.rowconfigure(1, weight=3)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=2)

    def add_line(self):
        ster = len(self.lines) + 1

        l = tk.Label(self.scroll_frame, text=f"Стержень {ster}")
        l.grid(row=ster + 2, column=0, padx=5, pady=5)

        temp_row = [l]
        for i in range(7):
            e = tk.Entry(self.scroll_frame, width=5)
            e.grid(row=ster + 2, column=i + 1, padx=5, pady=5)
            temp_row.append(e)
            if i in (0, 1, 6):
                e.config(validate='all')
            else:
                e.config(validate='all')
        self.lines.append(temp_row)

    def del_line(self):
        if len(self.lines) == 1:
            return
        for w in self.lines[-1]:
            w.grid_remove()
        self.lines.pop(-1)

    def collect(self):
        self.usrd.clear()

        if not self.nothing():
            for number, vals in enumerate(self.lines):
                self.usrd['f1'].append(float(vals[1].get()))
                self.usrd['f2'].append(float(vals[2].get()))
                self.usrd['a'].append(float(vals[3].get()))
                self.usrd['l'].append(float(vals[4].get()))
                self.usrd['e'].append(float(vals[5].get()))
                self.usrd['max'].append(float(vals[6].get()))
                self.usrd['q'].append(float(vals[7].get()))
            self.usrd['z'] = [self.support_var.get()]

    def nothing(self):
        for number, vals in enumerate(self.lines):
            for w in vals[1:]:
                if w.get() == '':
                    messagebox.showerror('Ошибка', 'Присутствуют пустые поля')
                    return True
        return False

    def clean(self):
        while len(self.lines) != 1:
            self.del_line()
        for e in self.lines[0][1:]:
            e.delete(0, tk.END)

    def pic(self):
        self.collect()
        if not self.nothing():
            self.usrd['l'] = picture.prp(self.usrd['l'], 10)
            section_lengths = [float(value) for value in self.usrd['l']]

            section_heights = [float(value) for value in self.usrd['a']]
            scaled_values = picture.prp(section_heights + section_lengths, 10)
            section_heights, section_lengths = scaled_values[:len(section_heights)], scaled_values[
                                                                                     len(section_heights):]
            scaled_values = picture.prp(section_heights + section_lengths, 10)

            section_heights, section_lengths = scaled_values[:len(section_heights)], scaled_values[
                                                                                     len(section_heights):]

            point_loads = []
            load_array_1 = self.usrd['f1']
            load_array_2 = self.usrd['f2']

            point_loads.append(load_array_1[0])
            for i in range(1, min(len(load_array_1), len(load_array_2))):
                point_loads.append(float(load_array_1[i]) + float(load_array_2[i - 1]))
            point_loads.append(load_array_2[-1])

            distributed_loads = self.usrd['q']

            support_type = self.support_var.get()

            picture.gt(self.canvas_image, section_lengths, section_heights, point_loads, distributed_loads,
                                support_type)

    def file_save(self):
        self.collect()
        if not self.nothing():
            file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.usrd, file, ensure_ascii=False, indent=4)

    def file_open(self):
        self.clean()

        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                for i in range(len(data['a'])):
                    self.lines[-1][1].delete(0, tk.END)
                    self.lines[-1][2].delete(0, tk.END)
                    self.lines[-1][7].delete(0, tk.END)

                    self.lines[i][1].insert(0, data['f1'][i])
                    self.lines[i][2].insert(0, data['f2'][i])
                    self.lines[i][3].insert(0, data['a'][i])
                    self.lines[i][4].insert(0, data['l'][i])
                    self.lines[i][5].insert(0, data['e'][i])
                    self.lines[i][6].insert(0, data['max'][i])
                    self.lines[i][7].insert(0, data['q'][i])

                    self.add_line()

                for w in self.lines[-1]:
                    w.grid_remove()
                del self.lines[-1]
                self.support_var.set(data['z'][0])

                self.pic()

    def make_calc(self):
        self.collect()
        if not self.nothing():
            ts = tables.prp_seg(self.usrd, 5)
            tables.show(ts, self.canvas_calc)



if __name__ == "__main__":
    app = App()
    app.mainloop()
