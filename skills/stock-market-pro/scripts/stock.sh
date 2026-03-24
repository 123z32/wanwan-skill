#!/bin/bash
# 股票行情查询工具 - Stock Market Query Tool
# 数据源: 东方财富 + 腾讯财经 (中国可用)
# 用法: ./stock.sh <代码> [类型]
# 类型: price(行情), history(历史), us(美股)

TICKER="${1}"
ACTION="${2:-price}"

if [ -z "$TICKER" ]; then
  echo "📊 股票行情查询工具"
  echo ""
  echo "用法: bash scripts/stock.sh <代码> [price|history|us]"
  echo ""
  echo "A股示例:"
  echo "  600519  - 贵州茅台(上海)"
  echo "  000858  - 五粮液(深圳)"
  echo "  300750  - 宁德时代(创业板)"
  echo ""
  echo "港股示例:"
  echo "  hk00700 - 腾讯控股"
  echo "  hk09988 - 阿里巴巴"
  echo ""
  echo "美股示例:"
  echo "  usAAPL  - 苹果"
  echo "  usNVDA  - 英伟达"
  echo "  usTSLA  - 特斯拉"
  echo ""
  echo "指数示例:"
  echo "  sh000001 - 上证指数"
  echo "  sz399001 - 深证成指"
  echo "  sz399006 - 创业板指"
  exit 0
fi

# 判断市场类型并构建东方财富 secid
get_secid() {
  local code="$1"
  # 美股
  if [[ "$code" == us* ]]; then
    local symbol="${code:2}"
    echo "105.$symbol"
    return
  fi
  # 港股
  if [[ "$code" == hk* ]]; then
    local symbol="${code:2}"
    echo "116.$symbol"
    return
  fi
  # 指数
  if [[ "$code" == sh0* ]]; then
    echo "1.${code:2}"
    return
  fi
  if [[ "$code" == sz39* ]]; then
    echo "0.${code:2}"
    return
  fi
  # A股: 6开头上海，其他深圳
  if [[ "$code" == 6* ]] || [[ "$code" == 9* ]]; then
    echo "1.$code"
  else
    echo "0.$code"
  fi
}

SECID=$(get_secid "$TICKER")

case "$ACTION" in
  price|行情|p)
    # 东方财富实时行情
    DATA=$(curl -s "https://push2.eastmoney.com/api/qt/stock/get?secid=$SECID&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,f57,f58,f60,f116,f117,f162,f167,f168,f169,f170,f171" \
      -H "User-Agent: Mozilla/5.0" 2>/dev/null)
    
    python3 -c "
import json,sys
d=json.loads('''$DATA''')
if d.get('data') is None:
    print('❌ 未找到股票: $TICKER')
    print('提示: A股直接输数字(600519), 港股加hk(hk00700), 美股加us(usAAPL)')
    sys.exit(1)

info=d['data']
name=info.get('f58','')
code=info.get('f57','')
price=info.get('f43',0)
high=info.get('f44',0)
low=info.get('f45',0)
open_p=info.get('f46',0)
vol=info.get('f47',0)
amount=info.get('f48',0)
prev=info.get('f60',0)
change=info.get('f169',0)
pct=info.get('f170',0)
pe=info.get('f162','-')
pb=info.get('f167','-')
mktcap=info.get('f116',0)
circap=info.get('f117',0)
amplitude=info.get('f171',0)
high52=info.get('f51',0)
low52=info.get('f52',0)

# 东方财富返回的价格需要除以100（部分情况）
# 判断是否需要处理
divisor = 100 if price > 100000 else 1  # 如果价格异常大说明是分为单位
if divisor > 1:
    price /= divisor
    high /= divisor
    low /= divisor
    open_p /= divisor
    prev /= divisor
    change /= divisor
    if high52: high52 /= divisor
    if low52: low52 /= divisor
    pct /= divisor

arrow='🔴' if pct < 0 else '🟢' if pct > 0 else '⚪'
print()
print(f'📊 {name} ({code})')
print(f'─' * 35)
print(f'{arrow} 当前: {price:.2f}  涨跌: {change:+.2f} ({pct:+.2f}%)')
print(f'   开盘: {open_p:.2f}  前收: {prev:.2f}')
print(f'   最高: {high:.2f}  最低: {low:.2f}')
if amplitude: print(f'   振幅: {amplitude/100:.2f}%')

# 成交量
if vol:
    if vol > 1e8:
        print(f'   成交量: {vol/1e8:.2f}亿手')
    elif vol > 1e4:
        print(f'   成交量: {vol/1e4:.2f}万手')
    else:
        print(f'   成交量: {vol}手')

# 成交额
if amount:
    if amount > 1e8:
        print(f'   成交额: {amount/1e8:.2f}亿')
    elif amount > 1e4:
        print(f'   成交额: {amount/1e4:.2f}万')

# 估值
if pe and pe != '-' and pe != 0:
    print(f'   市盈率(PE): {pe/100:.2f}' if pe > 100 else f'   市盈率(PE): {pe:.2f}')
if pb and pb != '-' and pb != 0:
    print(f'   市净率(PB): {pb/100:.2f}' if pb > 100 else f'   市净率(PB): {pb:.2f}')

# 市值
if mktcap:
    if mktcap > 1e12:
        print(f'   总市值: {mktcap/1e12:.2f}万亿')
    elif mktcap > 1e8:
        print(f'   总市值: {mktcap/1e8:.2f}亿')

if high52 and low52:
    print(f'   52周高: {high52:.2f}  52周低: {low52:.2f}')
print()
" 2>/dev/null || echo "❌ 查询失败，请检查代码: $TICKER"
    ;;

  history|历史|h)
    # 东方财富K线历史数据
    echo "📉 查询 $TICKER 历史走势..."
    KDATA=$(curl -s "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=$SECID&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&beg=0&end=20500101&lmt=30" \
      -H "User-Agent: Mozilla/5.0" 2>/dev/null)
    
    python3 << 'PYEOF'
import json,sys
data_str = sys.stdin.read()
d = json.loads(data_str)
if not d.get('data') or not d['data'].get('klines'):
    print('❌ 未找到历史数据')
    sys.exit(1)

info = d['data']
name = info.get('name','')
code = info.get('code','')
klines = info['klines']

print(f'\n📊 {name} ({code}) 近期走势\n')
print(f'{"日期":<12} {"开盘":>8} {"收盘":>8} {"最高":>8} {"最低":>8} {"涨跌%":>8} {"成交量":>10}')
print('─' * 70)

for line in klines[-20:]:  # 最近20天
    parts = line.split(',')
    if len(parts) < 7: continue
    date = parts[0][5:]  # MM-DD
    o, c, h, l = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
    vol = float(parts[5])
    pct = float(parts[6])
    
    arrow = '↑' if pct > 0 else '↓' if pct < 0 else '→'
    color = '🟢' if pct > 0 else '🔴' if pct < 0 else '⚪'
    
    vol_str = f'{vol/1e8:.1f}亿' if vol > 1e8 else f'{vol/1e4:.0f}万' if vol > 1e4 else str(int(vol))
    
    print(f'{date:<12} {o:>8.2f} {c:>8.2f} {h:>8.2f} {l:>8.2f} {color}{pct:>+6.2f}% {vol_str:>10}')

# 统计
closes = [float(k.split(',')[2]) for k in klines[-20:]]
if len(closes) >= 2:
    total_chg = (closes[-1] - closes[0]) / closes[0] * 100
    print(f'\n区间涨跌: {total_chg:+.2f}%  最高: {max(closes):.2f}  最低: {min(closes):.2f}')
print()
PYEOF
 <<< "$KDATA"
    ;;

  *)
    echo "用法: bash scripts/stock.sh <代码> [price|history]"
    ;;
esac
