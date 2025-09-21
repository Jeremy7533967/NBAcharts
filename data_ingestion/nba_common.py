import re
from datetime import datetime, timedelta
from typing import Optional

def convert_date(date_str: str) -> Optional[str]:
    """
    將相對時間表達式轉換為絕對日期時間字串。

    支援的格式：
    - "6小時 以前" -> 計算出對應的日期時間
    - "2天 以前" -> 計算出對應的日期時間
    - "30分鐘 以前" -> 計算出對應的日期時間
    - 其他格式（如絕對日期）直接返回原值

    返回格式：YYYY-MM-DD HH:MM:SS
    """
    if not date_str or date_str == 'N/A':
        return None

    # 定義時間單位的映射
    time_units = {
        '秒': 'seconds',
        '分鐘': 'minutes',
        '小時': 'hours',
        '天': 'days'
    }

    # 正則表達式匹配相對時間，如 "6小時 以前"
    pattern = r'(\d+)\s*([秒分鐘小時天]+)\s*以前'
    match = re.match(pattern, date_str.strip())

    if match:
        amount = int(match.group(1))
        unit_chinese = match.group(2)

        # 找到對應的英文單位
        unit_english = None
        for chinese_unit, english_unit in time_units.items():
            if chinese_unit in unit_chinese:
                unit_english = english_unit
                break

        if unit_english:
            # 獲取當前時間
            now = datetime.now()

            # 計算時間差
            delta_kwargs = {unit_english: amount}
            past_time = now - timedelta(**delta_kwargs)

            # 返回格式化的日期時間字串
            return past_time.strftime('%Y-%m-%d')

    # 如果不是相對時間格式，返回原值
    return date_str