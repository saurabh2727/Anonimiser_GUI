import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel
import re
import json
from sql_metadata import Parser
import pyperclip
import difflib
from sqlparse.keywords import KEYWORDS

class SQLMaskerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Masker for AI Use")
        self.root.geometry("1600x900")

        self.catalog_map = {}
        self.schema_map = {}
        self.table_map = {}
        self.column_map = {}
        self.string_map = {}

        self.sql_keywords = set(kw.lower() for kw in KEYWORDS.keys())

        self.copy_buttons = []
        self._setup_layout()

    def _setup_layout(self):
        self.root.grid_rowconfigure([1, 3, 5, 7, 9], weight=1)
        self.root.grid_columnconfigure(0, weight=4)
        self.root.grid_columnconfigure(1, weight=1)

        self._create_text_section("Original SQL (Sensitive):", 0, 'input_text')
        self._create_text_section("Masked SQL (Safe for AI):", 2, 'masked_text')
        self._create_text_section("Paste AI-Modified (Masked) SQL:", 4, 'ai_text')
        self._create_text_section("Final SQL (Restored with original names):", 6, 'unmasked_text')
        self._create_text_section("Diff Viewer:", 8, 'diff_text', readonly=True)

        self.mapping_text = scrolledtext.ScrolledText(self.root, width=40, state='disabled')
        self.mapping_text.grid(row=1, column=1, rowspan=7, sticky="nsew", padx=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")
        for i in range(5): btn_frame.columnconfigure(i, weight=1)

        tk.Button(btn_frame, text="Mask SQL", command=self.prepare_masking).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Unmask SQL", command=self.unmask_sql).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Show Diff", command=self.show_diff).grid(row=0, column=2, padx=5, sticky="ew")
        tk.Button(btn_frame, text="View Mapping", command=self.update_mapping_display).grid(row=0, column=3, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Load SQL File", command=self.load_file).grid(row=0, column=4, padx=5, sticky="ew")

    def _create_text_section(self, label_text, row, attr_name, readonly=False):
        label = tk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 0))
        text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=8)
        text_widget.grid(row=row+1, column=0, sticky="nsew", padx=10, pady=5)
        if readonly:
            text_widget.configure(state='disabled')
        setattr(self, attr_name, text_widget)
        self._add_copy_button(text_widget, row+2, 0)

    def _add_copy_button(self, text_widget, row, col):
        btn = tk.Button(self.root, text="Copy")
        btn.grid(row=row, column=col, sticky="e", padx=10, pady=(0, 10))
        btn.configure(command=lambda b=btn, w=text_widget: self.copy_text(w, b))
        self.copy_buttons.append(btn)

    def copy_text(self, widget, button):
        widget.configure(state='normal')
        content = widget.get("1.0", tk.END)
        widget.configure(state='disabled')
        pyperclip.copy(content.strip())
        original_text = button['text']
        button.config(text="✅")
        button.after(2000, lambda: button.config(text=original_text))

    def extract_tables(self, sql):
        return Parser(sql).tables

    def extract_columns(self, sql):
        return Parser(sql).columns

    def extract_strings(self, sql):
        return re.findall(r"'[^']*'", sql)

    def generate_placeholders(self, tables, columns, strings):
        def add_map(d, key, prefix, count):
            if key not in d:
                d[key] = {"mask": f"{prefix}_{count[0]}", "enabled": True}
                count[0] += 1

        self.catalog_map, self.schema_map, self.table_map = {}, {}, {}
        self.column_map, self.string_map = {}, {}
        c_count = s_count = t_count = col_count = str_count = [1]

        for tbl in tables:
            if tbl.lower() in self.sql_keywords:
                continue
            parts = tbl.split('.')
            if len(parts) == 3:
                add_map(self.catalog_map, parts[0], "catalog", c_count)
                add_map(self.schema_map, parts[1], "schema", s_count)
            elif len(parts) == 2:
                add_map(self.schema_map, parts[0], "schema", s_count)
            add_map(self.table_map, tbl, "table", t_count)

        for col in columns:
            if col.lower() not in self.sql_keywords and col != '*':
                add_map(self.column_map, col, "column", col_count)

        for s in strings:
            add_map(self.string_map, s, "'string" + str(str_count[0]) + "'", str_count)

    def prepare_masking(self):
        sql = self.input_text.get("1.0", tk.END)
        self.tables = self.extract_tables(sql)
        self.columns = self.extract_columns(sql)
        self.strings = self.extract_strings(sql)
        self.generate_placeholders(self.tables, self.columns, self.strings)
        self.show_mapping_editor()

    def show_mapping_editor(self):
        top = Toplevel(self.root)
        top.title("Edit Mapping Toggles")
        top.geometry("600x600")

        canvas = tk.Canvas(top)
        scrollbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        checkbox_vars = []
        category_vars = {}
        item_vars_by_category = {}
        row = 0

        for label, attr_key in [("Catalogs", "catalog_map"), ("Schemas", "schema_map"),
                                ("Tables", "table_map"), ("Columns", "column_map"), ("Strings", "string_map")]:
            category_var = tk.BooleanVar(value=True)
            category_vars[attr_key] = category_var
            item_vars_by_category[attr_key] = []
            tk.Checkbutton(
                scroll_frame, text=f"Enable {label}", variable=category_var, font=('Arial', 10, 'bold')
            ).grid(row=row, column=0, sticky='w', padx=5, pady=3)
            row += 1
            attr = getattr(self, attr_key)
            for key, val in attr.items():
                var = tk.BooleanVar(value=val["enabled"])
                cb = tk.Checkbutton(
                    scroll_frame, text=f"{key} → {val['mask']}", variable=var, anchor="w", justify="left"
                )
                cb.grid(row=row, column=0, sticky='w', padx=15)
                checkbox_vars.append((var, attr, key, category_var))
                item_vars_by_category[attr_key].append(var)
                row += 1

            # Add trace to category_var to update all item vars when toggled
            def make_callback(item_vars):
                def callback(*args):
                    value = category_var.get()
                    for v in item_vars:
                        v.set(value)
                return callback
            category_var.trace_add("write", make_callback(item_vars_by_category[attr_key]))

        def apply_and_close():
            for var, d, k, cat_var in checkbox_vars:
                d[k]["enabled"] = var.get() and cat_var.get()
            self.mask_sql()
            self.update_mapping_display()
            top.destroy()

        tk.Button(top, text="Apply & Mask SQL", command=apply_and_close).pack(pady=10)


    def mask_sql(self):
        sql = self.input_text.get("1.0", tk.END)
        for d in [self.catalog_map, self.schema_map, self.table_map, self.column_map]:
            for k, v in d.items():
                if v["enabled"]:
                    sql = re.sub(rf'\b{re.escape(k)}\b', v["mask"], sql)
        for k, v in self.string_map.items():
            if v["enabled"]:
                sql = sql.replace(k, v["mask"])
        self.masked_text.delete("1.0", tk.END)
        self.masked_text.insert(tk.END, sql)

    def unmask_sql(self):
        sql = self.ai_text.get("1.0", tk.END)
        for d in [self.catalog_map, self.schema_map, self.table_map, self.column_map]:
            for k, v in d.items():
                if v["enabled"]:
                    sql = re.sub(rf'\b{re.escape(v["mask"])}\b', k, sql)
        for k, v in self.string_map.items():
            if v["enabled"]:
                sql = sql.replace(v["mask"], k)
        self.unmasked_text.delete("1.0", tk.END)
        self.unmasked_text.insert(tk.END, sql)

    def show_diff(self):
        masked_sql = self.masked_text.get("1.0", tk.END).splitlines()
        ai_sql = self.ai_text.get("1.0", tk.END).splitlines()
        diff = difflib.unified_diff(masked_sql, ai_sql, lineterm='')
        diff_output = '\n'.join(diff)
        self.diff_text.configure(state='normal')
        self.diff_text.delete("1.0", tk.END)
        self.diff_text.insert(tk.END, diff_output or "No changes detected.")
        self.diff_text.configure(state='disabled')

    def update_mapping_display(self):
        self.mapping_text.configure(state='normal')
        self.mapping_text.delete("1.0", tk.END)
        for title, d in [("Catalogs", self.catalog_map), ("Schemas", self.schema_map),
                         ("Tables", self.table_map), ("Columns", self.column_map), ("Strings", self.string_map)]:
            # Insert bold title using a tag
            start_idx = self.mapping_text.index(tk.END)
            self.mapping_text.insert(tk.END, f"{title} (Enabled ✔️ / Disabled ❌):\n")
            end_idx = self.mapping_text.index(tk.END)
            self.mapping_text.tag_add("bold", start_idx, end_idx)
            for k, v in d.items():
                status = "✔️" if v["enabled"] else "❌"
                self.mapping_text.insert(tk.END, f"{k} → {v['mask']} {status}\n")
            self.mapping_text.insert(tk.END, "\n")
        self.mapping_text.tag_configure("bold", font=('TkDefaultFont', 10, 'bold'))
        self.mapping_text.configure(state='disabled')

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt")])
        if path:
            with open(path, 'r') as f:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, f.read())

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLMaskerGUI(root)
    root.mainloop()
