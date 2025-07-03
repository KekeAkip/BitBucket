import json
import csv
from pathlib import Path
from typing import List
from models import Expense
from datetime import datetime

class DataStore:
    def __init__(self, path: str = "expenses.json"):
        self.path = Path(path)               # 文件路径（使用 pathlib）
        self.expenses: List[Expense] = []    # 存储账目列表

    def load(self) -> None:
        # 从 JSON 文件读取数据并转换为 Expense 对象
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.expenses = [
                    Expense(
                        date=datetime.strptime(e["date"], "%Y-%m-%d").date(),
                        amount=e["amount"],
                        currency=e["currency"],
                        category=e["category"],
                        note=e["note"],
                        location=e["location"]
                    )
                    for e in data
                ]

    def save(self) -> None:
        # 将当前账目列表保存到 JSON 文件
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([
                {
                    "date": e.date.isoformat(),
                    "amount": e.amount,
                    "currency": e.currency,
                    "category": e.category,
                    "note": e.note,
                    "location": e.location
                } for e in self.expenses
            ], f, indent=2, ensure_ascii=False)

    def add(self, expense: Expense) -> None:
        # 添加一条账目记录
        self.expenses.append(expense)

    def list(self) -> List[Expense]:
        # 获取当前所有账目
        return self.expenses

    def export_csv(self, csv_path: str = "expenses.csv") -> None:
        # 将账目导出为 CSV 文件
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Amount", "Currency", "Category", "Note", "Location"])
            for e in self.expenses:
                writer.writerow([
                    e.date.isoformat(),
                    e.amount,
                    e.currency,
                    e.category,
                    e.note,
                    e.location
                ])
