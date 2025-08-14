def calculate_risk(entry_price, atr, support=None, resistance=None, balance=10000, risk_pct=0.02):
    stop_loss = round(support if support else entry_price - 1.5 * atr, 2)
    take_profit = round(resistance if resistance else entry_price + 2 * atr, 2)

    risk_amount = balance * risk_pct
    position_size = round(risk_amount / (entry_price - stop_loss), 2)
    risk_ratio = round((take_profit - entry_price) / (entry_price - stop_loss), 2)
    risk_level = "Low" if risk_ratio >= 2.5 else "Moderate" if risk_ratio >= 1.5 else "High"

    return {
        "entry": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "position_size": position_size,
        "risk_ratio": risk_ratio,
        "risk_level": risk_level
    }
