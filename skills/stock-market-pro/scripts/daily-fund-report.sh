#!/bin/bash
# 每日基金持仓播报
# 张的支付宝基金持仓

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/stock.sh"

FUNDS=(
  "018927|南方中证电池"
  "014143|银河创新成长"
  "022364|永赢科技智选"
  "013943|华宝稀有金属"
  "000854|鹏华养老"
  "012976|西部利得碳中和"
  "016875|交银滚动债"
)

echo "📊 基金日报 — $(date '+%Y-%m-%d')"
echo ""

for item in "${FUNDS[@]}"; do
  CODE="${item%%|*}"
  NAME="${item##*|}"
  
  # 获取天天基金实时估值
  GZ=$(curl -s "https://fundgz.1234567.com.cn/js/$CODE.js" \
    -H "Referer: https://fund.eastmoney.com" 2>/dev/null)
  
  python3 -c "
import re, json
raw = '''$GZ'''
m = re.search(r'jsonpgz\(({.*?})\)', raw)
if m:
    d = json.loads(m.group(1))
    gsz = d.get('gsz','?')
    gszzl = d.get('gszzl','?')
    dwjz = d.get('dwjz','?')
    pct = float(gszzl) if gszzl != '?' else 0
    arrow = '🟢' if pct > 0 else '🔴' if pct < 0 else '⚪'
    alert = '⚡' if abs(pct) > 3 else ''
    print(f'{arrow} $NAME($CODE): {gsz} ({gszzl}%) {alert}')
else:
    print(f'⚪ $NAME($CODE): 暂无数据')
" 2>/dev/null
done

echo ""
echo "💡 数据来自天天基金估值，仅供参考"
