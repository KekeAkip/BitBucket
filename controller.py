from models import Expense
from storage import DataStore
from datetime import date

class AppController:
    def __init__(self, data_path="expenses.json"):
        self.store = DataStore(data_path)  # 初始化数据存储
        self.store.load()                  # 加载已有账目数据

    def add_expense(
        self,
        amount: float,
        currency: str,
        category: str,
        note: str,
        location: str,
        date_value: date = date.today()   # 可选：默认使用今天
    ) -> str:
        """添加一条新的支出记录"""
        expense = Expense(
            date=date_value,
            amount=amount,
            currency=currency,
            category=category,
            note=note,
            location=location
        )
        self.store.add(expense)
        self.store.save()
        return expense.id  # 返回新账目的 ID

    def get_expenses(self) -> list[Expense]:
        """获取所有账目列表"""
        return self.store.list()

    def export_csv(self, csv_path="expenses.csv") -> None:
        """导出账目为 CSV"""
        self.store.export_csv(csv_path)
        
    def update_expense(
        self,
        expense_id: str,
        *,
        amount: float,
        currency: str,
        category: str,
        note: str,
        location: str,
        date_value: date
    ) -> bool:
        """按 ID 更新指定账目，成功返回 True"""
        updated_exp = Expense(
            id=expense_id,            # 保持原 ID
            date=date_value,
            amount=amount,
            currency=currency,
            category=category,
            note=note,
            location=location
        )
        updated = self.store.update(expense_id, updated_exp)
        if updated:
            self.store.save()
        return updated
    
    def delete_expense(self, expense_id: str) -> bool:
        """按 ID 删除一条账目，成功返回 True"""
        removed = self.store.delete(expense_id)
        if removed:
            self.store.save()
        return removed
    
    def get_total_rmb(self) -> float:
        """返回全部支出折合人民币的总额"""
        rates = {
            "CNY": 1.0,
            "JPY": 0.045,   # 例：1 JPY ≈ 0.045 RMB
            "GBP": 9.2      # 例：1 GBP ≈ 9.2 RMB
        }

        total = 0.0
        for e in self.store.list():
            rate = rates.get(e.currency.upper(), 1.0)
            total += e.amount * rate
        return total