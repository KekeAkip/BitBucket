from datetime import date
from models import Expense
from storage import DataStore

def main() -> None:
    store = DataStore("expenses.json")  # 若文件不存在会在 save() 时自动创建
    store.load()                        # 先尝试读取已有数据

    # 创建一条测试账目
    test_expense = Expense(
        date=date.today(),
        amount=1200.0,
        currency="JPY",
        category="餐饮",
        note="银座寿司套餐",
        location="东京"
    )

    store.add(test_expense)  # 添加到内存列表
    store.save()             # 写回 JSON
    store.export_csv()       # 额外导出 CSV

    # 打印当前账目，验证一切正常
    for e in store.list():
        print(e)

if __name__ == "__main__":
    main()
    print("Demo completed successfully!")
