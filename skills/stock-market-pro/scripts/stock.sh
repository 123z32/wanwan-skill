#!/bin/bash
# 股票/基金行情查询工具
# 数据源: 东方财富 + 天天基金 (中国可用)
# 用法: ./stock.sh <代码> [类型]

TICKER="${1}"
ACTION="${2:-price}"

if [ -z "$TICKER" ]; then
  echo "📊 股票/基金行情查询工具"
  echo ""
  echo "用法: bash scripts/stock.sh <代码> [price|history|fund]"
  echo ""
  echo "=== 股票 ==="
  echo "  A股:   600519(茅台), 000858(五粮液), 300750(宁德时代)"
  echo "  港股:  hk00700(腾讯), hk09988(阿里)"
  echo "  美股:  usAAPL(苹果), usNVDA(英伟达), usTSLA(特斯拉)"
  echo "  指数:  sh000001(上证), sz399001(深证), sz399006(创业板)"
  echo ""
  echo "=== 基金 ==="
  echo "  基金:  fund110011(易方达中小盘), fund001632(前海开源金银珠宝)"
  echo "         fund510300(沪深300ETF), fund159919(沪深300ETF深)"
  echo ""
  echo "=== 操作 ==="
  echo "  price   - 实时行情(默认)"
  echo "  history - 历史走势"
  echo "  fund    - 基金详情(净值/持仓/排名)"
  exit 0
fi

# 判断市场类型
get_secid() {
  local code="$1"
  if [[ "$code" == us* ]]; then echo "105.${code:2}"; return; fi
  if [[ "$code" == hk* ]]; then echo "116.${code:2}"; return; fi
  if [[ "$code" == sh0* ]]; then echo "1.${code:2}"; return; fi
  if [[ "$code" == sz39* ]]; then echo "0.${code:2}"; return; fi
  if [[ "$code" == fund* ]]; then echo "fund.${code:4}"; return; fi
  if [[ "$code" == 6* ]] || [[ "$code" == 9* ]]; then echo "1.$code"
  else echo "0.$code"; fi
}

SECID=$(get_secid "$TICKER")

# 基金查询
if [[ "$TICKER" == fund* ]] || [[ "$ACTION" == "fund" ]]; then
  FUND_CODE="${TICKER#fund}"
  # 如果是纯数字且不是fund前缀，可能用户直接输了基金代码
  if [[ "$ACTION" == "fund" ]]; then FUND_CODE="$TICKER"; fi
  
  echo "📊 查询基金 $FUND_CODE ..."
  
  # 天天基金实时估值
  GZ_DATA=$(curl -s "https://fundgz.1234567.com.cn/js/$FUND_CODE.js" \
    -H "Referer: https://fund.eastmoney.com" 2>/dev/null)
  
  # 天天基金基本信息
  INFO_DATA=$(curl -s "https://fund.eastmoney.com/pingzhongdata/$FUND_CODE.js" \
    -H "Referer: https://fund.eastmoney.com" 2>/dev/null)
  
  python3 << PYEOF
import json, re, sys

# 解析实时估值
gz_raw = '''$GZ_DATA'''
gz = None
m = re.search(r'jsonpgz\(({.*?})\)', gz_raw)
if m:
    gz = json.loads(m.group(1))

# 解析基金信息
info_raw = '''$INFO_DATA'''

# 提取基金名称
fund_name = ''
m = re.search(r'fS_name\s*=\s*"([^"]*)"', info_raw)
if m: fund_name = m.group(1)

# 提取基金代码
fund_code = ''
m = re.search(r'fS_code\s*=\s*"([^"]*)"', info_raw)
if m: fund_code = m.group(1)

# 提取基金经理
fund_manager = []
for m in re.finditer(r'"name":"([^"]*)"', info_raw[:2000]):
    fund_manager.append(m.group(1))

# 提取净值走势(最近几个数据点)
nav_data = []
m = re.search(r'Data_netWorthTrend\s*=\s*(\[.*?\]);', info_raw)
if m:
    try:
        nav_data = json.loads(m.group(1))
    except: pass

if not gz and not fund_name:
    print(f'❌ 未找到基金: $FUND_CODE')
    print('提示: 基金代码前加fund，如 fund110011')
    sys.exit(1)

print()
print(f'📊 {fund_name} ({fund_code})')
print('─' * 40)

if gz:
    print(f'📅 估值日期: {gz.get("gztime","")}')
    print(f'   实时估值: {gz.get("gsz","")}')
    print(f'   估算涨跌: {gz.get("gszzl","")}%')
    print(f'   单位净值: {gz.get("dwjz","")} (上一日)')
    print()

# 基金经理
if fund_manager:
    print(f'👤 基金经理: {", ".join(fund_manager[:2])}')

# 最近净值走势
if nav_data and len(nav_data) > 5:
    print()
    print('📈 近5日净值:')
    from datetime import datetime
    for item in nav_data[-5:]:
        ts = item.get('x', 0) / 1000
        nav = item.get('y', 0)
        eq = item.get('equityReturn', 0)
        dt = datetime.fromtimestamp(ts).strftime('%m-%d')
        arrow = '🟢' if eq > 0 else '🔴' if eq < 0 else '⚪'
        print(f'   {dt}  净值: {nav:.4f}  {arrow} {eq:+.2f}%')

# 阶段收益
print()
m_rate = re.search(r'Data_rateInSimilarPersent\s*=\s*(\[.*?\]);', info_raw)
if m_rate:
    try:
        rate_data = json.loads(m_rate.group(1))
        if len(rate_data) >= 5:
            latest = rate_data[-1]
            pct = latest[1]
            print(f'📊 同类排名百分位: 前 {pct:.1f}%')
    except: pass

# 规模
m_scale = re.search(r'Data_fluctuationScale\s*=\s*({.*?});', info_raw)
if m_scale:
    try:
        scale = json.loads(m_scale.group(1))
        if scale.get('series'):
            latest = scale['series'][-1]
            print(f'💰 最新规模: {latest["y"]:.2f}亿')
    except: pass

print()
PYEOF
  exit 0
fi

case "$ACTION" in
  price|行情|p)
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

divisor = 100 if price > 100000 else 1
if divisor > 1:
    price /= divisor; high /= divisor; low /= divisor
    open_p /= divisor; prev /= divisor; change /= divisor
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
if vol:
    vol_str = f'{vol/1e8:.2f}亿手' if vol > 1e8 else f'{vol/1e4:.2f}万手' if vol > 1e4 else f'{vol}手'
    print(f'   成交量: {vol_str}')
if amount:
    amt_str = f'{amount/1e8:.2f}亿' if amount > 1e8 else f'{amount/1e4:.2f}万' if amount > 1e4 else str(amount)
    print(f'   成交额: {amt_str}')
if pe and pe != '-' and pe != 0:
    print(f'   市盈率(PE): {pe/100:.2f}' if pe > 100 else f'   市盈率(PE): {pe:.2f}')
if pb and pb != '-' and pb != 0:
    print(f'   市净率(PB): {pb/100:.2f}' if pb > 100 else f'   市净率(PB): {pb:.2f}')
if mktcap:
    cap_str = f'{mktcap/1e12:.2f}万亿' if mktcap > 1e12 else f'{mktcap/1e8:.2f}亿'
    print(f'   总市值: {cap_str}')
if high52 and low52:
    print(f'   52周高: {high52:.2f}  52周低: {low52:.2f}')
print()
" 2>/dev/null || echo "❌ 查询失败"
    ;;

  history|历史|h)
    echo "📉 查询 $TICKER 历史走势..."
    KDATA=$(curl -s "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=$SECID&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&beg=0&end=20500101&lmt=20" \
      -H "User-Agent: Mozilla/5.0" 2>/dev/null)
    
    echo "$KDATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if not d.get('data') or not d['data'].get('klines'):
    print('❌ 未找到历史数据'); sys.exit(1)
info=d['data']; name=info.get('name',''); code=info.get('code','')
klines=info['klines']
print(f'\n📊 {name} ({code}) 近期走势\n')
print(f'{\"日期\":<12} {\"开盘\":>8} {\"收盘\":>8} {\"最高\":>8} {\"最低\":>8} {\"涨跌%\":>8} {\"成交量\":>10}')
print('─' * 70)
for line in klines[-20:]:
    p=line.split(',')
    if len(p)<7: continue
    dt=p[0][5:]; o,c,h,l=float(p[1]),float(p[2]),float(p[3]),float(p[4])
    vol=float(p[5]); pct=float(p[6])
    color='🟢' if pct>0 else '🔴' if pct<0 else '⚪'
    vs=f'{vol/1e8:.1f}亿' if vol>1e8 else f'{vol/1e4:.0f}万' if vol>1e4 else str(int(vol))
    print(f'{dt:<12} {o:>8.2f} {c:>8.2f} {h:>8.2f} {l:>8.2f} {color}{pct:>+6.2f}% {vs:>10}')
closes=[float(k.split(',')[2]) for k in klines[-20:]]
if len(closes)>=2:
    tc=(closes[-1]-closes[0])/closes[0]*100
    print(f'\n区间涨跌: {tc:+.2f}%  最高: {max(closes):.2f}  最低: {min(closes):.2f}')
print()
" 2>/dev/null || echo "❌ 查询失败"
    ;;

  *)
    echo "用法: bash scripts/stock.sh <代码> [price|history|fund]"
    ;;
esac
