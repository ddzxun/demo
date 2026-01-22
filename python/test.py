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

    # 1. 基础资金拆分
    cash = T * c
    position_init = T * (1 - c)

    # 2. 回撤档位（相对最高点）
    drawdown_levels = [0.05, 0.08, 0.12]

    # 3. 补仓系数（总和 = 1）
    add_ratios = [0.25, 0.375, 0.375]

    # 4. 补仓金额临时存放位置
    storage_location = ["现金", "黄金", "底仓"]

    add_plan = []
    for d, k, l in zip(drawdown_levels, add_ratios, storage_location):
        add_plan.append({
            "回撤": d,
            "补仓金额": cash * k,
            "存放位置": l
        })

    # 4. 止盈档位（相对成本）
    take_profit_plan = [
        {"收益率": 0.25, "减仓比例": 0.30},
        {"收益率": 0.40, "减仓比例": 0.30},
        {"收益率": 0.60, "减仓比例": 0.40},
    ]

    # 5. 最大允许回撤（风控）
    max_drawdown = 1.5 * c

    return {
        "total_capital": T,
        "cash_ratio": c,
        "建仓": position_init,
        "预留现金": cash,

        # "drawdown_formula": "(H - P) / H",
        # "profit_formula": "(V - C) / C",

        "补仓计划": add_plan,
        "止盈计划": take_profit_plan,

        "最大回撤->建议清仓": max_drawdown
    }
# 6成 底仓
# 4成 进攻
# T = 总资金
# c = 现金占比（进攻仓常用 0.20 ～ 0.30）
system = attack_position_system(T=200000, c=0.2)

for k, v in system.items():
    print(k, ":", v)

# 1️⃣ 判断补仓（只在收盘后调用） -  ✅ 按「相对历史最高收盘价回撤」而不是 「当天收盘价回撤」
# 2️⃣ 判断止盈（盘中或收盘都可以）