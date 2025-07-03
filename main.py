from controller import AppController
from gui import ExpenseApp

def main():
    controller = AppController()  # 默认使用 "expenses.json"
    app = ExpenseApp(controller)  # 初始化 GUI 并绑定控制器
    app.mainloop()                # 启动主事件循环

if __name__ == "__main__":
    main()