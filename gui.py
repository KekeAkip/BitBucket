import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry  # 日期选择器组件（需 pip 安装）
from controller import AppController
from datetime import date

class ExpenseApp(tk.Tk):
    def __init__(self, controller: AppController):
        super().__init__()
        self.controller = controller
        self.title("旅行记账本")
        self.geometry("800x500")

        self._build_form()
        self._build_table()
        self._refresh_table()

    def _build_form(self):
        """构建输入表单区域"""
        frame = ttk.LabelFrame(self, text="添加账目")
        frame.pack(fill="x", padx=10, pady=10)

        # 金额
        ttk.Label(frame, text="金额").grid(row=0, column=0)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.amount_var).grid(row=0, column=1)

        # 币种
        ttk.Label(frame, text="币种").grid(row=0, column=2)
        self.currency_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.currency_var, values=["JPY", "CNY", "GBP"]).grid(row=0, column=3)

        # 分类
        ttk.Label(frame, text="分类").grid(row=1, column=0)
        self.category_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.category_var, values=["餐饮", "交通", "住宿", "门票", "购物"]).grid(row=1, column=1)

        # 备注
        ttk.Label(frame, text="备注").grid(row=1, column=2)
        self.note_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.note_var).grid(row=1, column=3)

        # 地点
        ttk.Label(frame, text="地点").grid(row=2, column=0)
        self.location_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.location_var).grid(row=2, column=1)

        # 日期选择器（tkcalendar）
        ttk.Label(frame, text="日期").grid(row=2, column=2)
        self.date_entry = DateEntry(frame, date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=2, column=3)

        # 添加按钮
        ttk.Button(frame, text="添加记录", command=self._add_expense).grid(row=3, column=3, pady=10)

        # 导出按钮
        ttk.Button(frame, text="导出 CSV", command=self._export_csv).grid(row=3, column=0, pady=10)

    def _build_table(self):
        """构建账目展示表格"""
        columns = ["日期", "金额", "币种", "分类", "备注", "地点"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def _refresh_table(self):
        """刷新表格数据"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for e in self.controller.get_expenses():
            self.tree.insert("", "end", values=(
                e.date.isoformat(),
                e.amount,
                e.currency,
                e.category,
                e.note,
                e.location
            ))

    def _add_expense(self):
        """处理添加账目按钮逻辑"""
        try:
            self.controller.add_expense(
                amount=self.amount_var.get(),
                currency=self.currency_var.get(),
                category=self.category_var.get(),
                note=self.note_var.get(),
                location=self.location_var.get(),
                date_value=self.date_entry.get_date()
            )
            self._refresh_table()
            messagebox.showinfo("成功", "账目已添加并保存！")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _export_csv(self):
        """处理导出按钮逻辑"""
        self.controller.export_csv()
        messagebox.showinfo("导出完成", "账目已导出为 expenses.csv")