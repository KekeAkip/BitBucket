import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controller import AppController
from datetime import date
import re
import datetime

class ExpenseApp(tk.Tk):
    def __init__(self, controller: AppController):
        super().__init__()
        self.controller = controller
        self.title("旅行记账本")
        self.geometry("850x550")
        
        self.selected_id: str | None = None     # 当前选中的记录 ID

        self.sort_reverse: dict[str, bool] = {}   # 记录每列当前是否倒序
        
        self._build_form()
        self._build_table()
        self._refresh_table()

    def _build_form(self):
        """构建账目操作表单"""
        frame = ttk.LabelFrame(self, text="账目操作")
        frame.pack(fill="x", padx=10, pady=10)

        # 金额
        ttk.Label(frame, text="金额").grid(row=0, column=0, sticky="e")
        self.amount_var = tk.StringVar()
        # 注册校验回调；%P 代表“变更后预期写入控件的新文本”
        vcmd = (self.register(self._validate_amount), "%P")

        ttk.Entry(frame,
                textvariable=self.amount_var,
                validate="key",
                validatecommand=vcmd,
                width=15).grid(row=0, column=1)
        
        # 币种
        ttk.Label(frame, text="币种").grid(row=0, column=2, sticky="e")
        self.currency_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.currency_var,
                     values=["JPY", "CNY", "GBP"], width=12).grid(row=0, column=3)

        # 分类
        ttk.Label(frame, text="分类").grid(row=1, column=0, sticky="e")
        self.category_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.category_var,
                     values=["餐饮", "交通", "住宿", "门票", "购物"], width=12).grid(row=1, column=1)

        # 备注
        ttk.Label(frame, text="备注").grid(row=1, column=2, sticky="e")
        self.note_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.note_var, width=30).grid(row=1, column=3)

        # 地点
        ttk.Label(frame, text="地点").grid(row=2, column=0, sticky="e")
        self.location_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.location_var, width=15).grid(row=2, column=1)

        # 日期
        ttk.Label(frame, text="日期").grid(row=2, column=2, sticky="e")
        self.date_entry = DateEntry(frame, date_pattern="yyyy-mm-dd", width=12)
        self.date_entry.grid(row=2, column=3)

        # 操作按钮
        ttk.Button(frame, text="添加记录", command=self._add_expense).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="更新记录", command=self._update_expense).grid(row=3, column=1, pady=10)
        ttk.Button(frame, text="删除记录", command=self._delete_expense).grid(row=3, column=2, pady=10)
        ttk.Button(frame, text="导出 CSV", command=self._export_csv).grid(row=3, column=3, pady=10)
        
        # 计算总支出按钮
        ttk.Button(self, text="计算总支出（RMB）", command=self._show_total_rmb).pack(pady=5)


    def _build_table(self):
        """构建账目列表表格"""
        columns = ["日期", "金额", "币种", "分类", "备注", "地点"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")

        for col in columns:
            self.tree.heading(col, text=col,
                            command=lambda c=col: self._sort_by(c))
            # 根据需要调宽
            self.tree.column(col, anchor="center", width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)


    def _refresh_table(self):
        """刷新表格数据"""
        self.tree.delete(*self.tree.get_children())
        for e in self.controller.get_expenses():
            # 使用 id 作为 Treeview 条目 iid，便于后续精确操作
            self.tree.insert("", "end", iid=e.id, values=(
                e.date.isoformat(), e.amount, e.currency,
                e.category, e.note, e.location
            ))
            
    def _sort_by(self, col_name: str):
        """根据列名对 Treeview 中的记录升/降序排序"""
        # 获取当前列的排序方向（默认为升序 False）
        reverse = self.sort_reverse.get(col_name, False)

        # 1. 把所有行的信息拿下来
        items = []
        for iid in self.tree.get_children():
            values = self.tree.item(iid)["values"]
            items.append((iid, values))

        # 2. 根据列名决定 Key 如何解析
        col_index = {
            "日期": 0,
            "金额": 1,
            "币种": 2,
            "分类": 3,
            "备注": 4,
            "地点": 5
        }[col_name]

        def parse_key(values):
            val = values[col_index]
            if col_name == "日期":
                return datetime.datetime.strptime(val, "%Y-%m-%d")
            if col_name == "金额":
                return float(val)
            return val  # 其它列按字符串比较

        # 3. 排序
        items.sort(key=lambda tup: parse_key(tup[1]), reverse=reverse)

        # 4. 重新按排序后的顺序放回 Treeview
        for index, (iid, _) in enumerate(items):
            self.tree.move(iid, "", index)

        # 5. 切换该列方向
        self.sort_reverse[col_name] = not reverse
    
    def _on_row_select(self, _event):
        """处理行选择事件，回填表单"""
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_id = selection[0]             # Treeview 的 iid = Expense.id
        item = self.tree.item(self.selected_id)["values"]

        # 根据 columns 顺序依次回填
        self.date_entry.set_date(item[0])
        self.amount_var.set(float(item[1]))
        self.currency_var.set(item[2])
        self.category_var.set(item[3])
        self.note_var.set(item[4])
        self.location_var.set(item[5])

    def _add_expense(self):
        """处理添加账目按钮逻辑"""
        try:
            new_id = self.controller.add_expense(
                amount=float(self.amount_var.get()) if self.amount_var.get() else 0.0,
                currency=self.currency_var.get(),
                category=self.category_var.get(),
                note=self.note_var.get(),
                location=self.location_var.get(),
                date_value=self.date_entry.get_date()
            )
            self._refresh_table()
            self._clear_form()
            # 选中新写入的那一行
            if new_id:
                try:
                    self.tree.selection_set(new_id)
                except tk.TclError:
                    pass   # 忽略极少见的 “items not found”

            messagebox.showinfo("成功", "账目已添加并保存！")
        except Exception as e:
            messagebox.showerror("错误", str(e))
            
    def _validate_amount(self, new_value: str) -> bool:
        """
        仅允许：
        1) 空字符串（方便删改）
        2) 整数
        3) 小数，且小数点后最多两位
        """
        if new_value == "":
            return True
        return re.fullmatch(r"\d+(\.\d{0,2})?", new_value) is not None


    def _update_expense(self):
        """处理更新账目按钮逻辑"""
        if not self.selected_id:
            messagebox.showwarning("未选择", "请先在表格中选择要更新的记录。")
            return
        try:
            self.controller.update_expense(
                expense_id=self.selected_id,
                amount=float(self.amount_var.get()) if self.amount_var.get() else 0.0,
                currency=self.currency_var.get(),
                category=self.category_var.get(),
                note=self.note_var.get(),
                location=self.location_var.get(),
                date_value=self.date_entry.get_date()
            )
            self._refresh_table()
            self.tree.selection_set(self.selected_id)
            messagebox.showinfo("成功", "记录已更新！")
        except Exception as e:
            messagebox.showerror("错误", str(e))
            
    def _delete_expense(self):
        """处理删除账目按钮逻辑"""
        if not self.selected_id:
            messagebox.showwarning("未选择", "请先在表格中选择要删除的记录。")
            return
        if messagebox.askyesno("确认删除", "确定删除这条记录吗？"):
            if self.controller.delete_expense(self.selected_id):
                self._refresh_table()
                self._clear_form()
                self.selected_id = None
                messagebox.showinfo("已删除", "记录已删除。")
            else:
                messagebox.showerror("失败", "删除失败，记录未找到。")
    
    def _export_csv(self):
        """处理导出按钮逻辑"""
        self.controller.export_csv()
        messagebox.showinfo("导出完成", "账目已导出为 expenses.csv")
        
    def _clear_form(self):
        """清空表单输入"""
        self.amount_var.set("")
        self.currency_var.set("")
        self.category_var.set("")
        self.note_var.set("")
        self.location_var.set("")
        self.date_entry.set_date(date.today())
        
    def _show_total_rmb(self):
        total = self.controller.get_total_rmb()
        messagebox.showinfo("总支出", f"全部消费折合人民币约为：¥{total:.2f}")
