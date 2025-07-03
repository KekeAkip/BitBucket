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
    ) -> None:
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

    def get_expenses(self) -> list[Expense]:
        """获取所有账目列表"""
        return self.store.list()

    def export_csv(self, csv_path="expenses.csv") -> None:
        """导出账目为 CSV"""
        self.store.export_csv(csv_path)
