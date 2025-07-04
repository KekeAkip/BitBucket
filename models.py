from dataclasses import dataclass, field
from datetime import date
import uuid

@dataclass
class Expense:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # 自动生成唯一ID
    date: date               # 记账日期
    amount: float            # 金额
    currency: str            # 货币种类，如 "JPY", "GBP", "CNY"
    category: str            # 类别，如 "餐饮", "交通"
    note: str                # 备注，例如 "东京塔门票"
    location: str            # 地点，例如 "东京"
