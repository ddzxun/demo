def attack_position_system(T, c):
    """
    进攻仓资金管理制度生成器

    参数:
        T : float
            总资金
        c : float
            现金占比 (0 < c < 1)

    返回:
        dict : 进攻仓完整制度
    """

    assert 0 < c < 1, "现金占比 c 必须在 (0, 1) 之间"

    # 基础资金拆分
    cash = T * c
    position_init = T * (1 - c)

    # 建仓计划
    build_plan = {
        "第一阶段": [
            position_init * 0.25,
            position_init * 0.25
        ],
        "第二阶段": [
            position_init * 0.50
        ]
    }

    # 补仓计划
    drawdown_levels = [0.06, 0.12]
    add_ratios = [0.4, 0.6]
    storage_location = ["黄金", "底仓"]
    add_plan = []
    for d, k, l in zip(drawdown_levels, add_ratios, storage_location):
        add_plan.append({
            "回撤": d,
            "补仓金额": cash * k,
            "存放位置": l
        })

    # 止盈计划
    take_profit_plan = [
        {"收益率": 0.30, "减仓比例": 0.55},
        {"收益率": 0.45, "减仓比例": 0.45},
    ]    

    # 最大允许回撤（风控）
    max_drawdown = min(0.25, 1.5 * c)

    return {
        "total_capital": T,
        "cash_ratio": c,
        "建仓": position_init,
        "预留现金": cash,

        "建仓计划": build_plan,
        "补仓计划": add_plan,
        "止盈计划": take_profit_plan,

        "最大回撤->建议清仓": max_drawdown
    }


def base_position_allocation(T):
    """
    底仓初始买入计算器
    以 011730 70% + 007029 30% 配置
    
    参数：
        T : float
            底仓总金额
    
    返回：
        dict : 各基金初始买入金额
    """
    allocation = {
        "011730 工银聚享混合C": T * 0.7,
        "007029 中证500ETF": T * 0.3
    }
    return allocation


def position_allocation(total_amount):
    """
    总资金按底仓/进攻仓比例分配
    
    参数：
        total_amount : float
            总资金金额
    
    返回：
        dict : 底仓金额和进攻仓金额
    """
    base_ratio = 0.6   # 底仓占比
    attack_ratio = 0.4 # 进攻仓占比

    allocation = {
        "底仓金额": total_amount * base_ratio,
        "进攻仓金额": total_amount * attack_ratio
    }
    return allocation


# 6成 底仓
# 4成 进攻仓
total_money = 600000
alloc = position_allocation(total_money)
print("------------------------------------------")
for k, v in alloc.items():
    print(f"{k}: {v:.2f} 元")
print("------------------------------------------\n")


base_buy = base_position_allocation(T=4000)
print("------------------------------------------")
for fund, amount in base_buy.items():
    print(f"{fund} 初始买入金额: {amount:.2f} 元")
print("------------------------------------------\n")


print("------------------------------------------")
# T = 进攻仓总资金
# c = 现金占比
system = attack_position_system(T=200000, c=0.10)
for k, v in system.items():
    print(k, ":", v)
print("------------------------------------------")

# 1️⃣ 判断补仓（只在收盘后调用） -  ✅ 按「相对历史最高收盘价回撤」而不是 「当天收盘价回撤」
#   补仓信号看昨日(T)收盘，T+1 若盘中震荡则当日补仓，若单边趋势则延后至 T+2 观察，每档补仓只执行一次。
# 2️⃣ 判断止盈（盘中或收盘都可以）
#   止盈按T收盘收益率判断，T+1 开盘执行，分档减仓，每档止盈只触发一次。