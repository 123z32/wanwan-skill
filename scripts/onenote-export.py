#!/usr/bin/env python3
"""OneNote → RAG v3: 逐笔记本处理，flush输出"""
import urllib.request, urllib.parse, json, os, time, re, sys
from html.parser import HTMLParser

API_KEY = os.environ.get("MATON_API_KEY", "")
RAG_URL = "http://localhost:9900/api/add"
BASE = "https://gateway.maton.ai/one-note/v1.0/me/onenote"
SKIP_NB = {"待做事项", "需办事项"}
SKIP_KEYWORDS = {"待做", "需办", "TODO", "待办"}
OUT_DIR = "/openclaw_data/.openclaw/workspace/onenote-export"

class HtmlToText(HTMLParser):
    def __init__(self):
        super().__init__(); self.r=[]; self.skip=False
    def handle_starttag(self,t,a):
        if t in('script','style'): self.skip=True
        if t in('br','p','div','h1','h2','h3','h4','h5','h6','li','tr'): self.r.append('\n')
        if t in('td','th'): self.r.append(' | ')
        # Convert heading tags to markdown
        d = dict(a)
        if t == 'h1': self.r.append('# ')
        elif t == 'h2': self.r.append('## ')
        elif t == 'h3': self.r.append('### ')
        elif t == 'h4': self.r.append('#### ')
        if t == 'b' or t == 'strong': self.r.append('**')
        if t == 'i' or t == 'em': self.r.append('*')
        if t == 'code': self.r.append('`')
        if t == 'li': self.r.append('- ')
        if t == 'a':
            href = d.get('href','')
            if href: self.r.append('[')
        if t == 'img':
            alt = d.get('alt','图片')
            src = d.get('src','')
            self.r.append(f'![{alt}]({src})')
    def handle_endtag(self,t):
        if t in('script','style'): self.skip=False
        if t in('p','div','h1','h2','h3','h4','h5','h6','table','ul','ol'): self.r.append('\n')
        if t == 'b' or t == 'strong': self.r.append('**')
        if t == 'i' or t == 'em': self.r.append('*')
        if t == 'code': self.r.append('`')
    def handle_data(self,d):
        if not self.skip: self.r.append(d)
    def text(self):
        t=''.join(self.r); t=re.sub(r'\n{3,}','\n\n',t); t=re.sub(r'[ \t]+',' ',t)
        return t.strip()

def h2t(html):
    p=HtmlToText()
    try: p.feed(html); return p.text()
    except: return re.sub(r'<[^>]+>',' ',html).strip()

def get(path, accept="application/json"):
    url = path if path.startswith("http") else f"{BASE}{path}"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {API_KEY}')
    req.add_header('Accept', accept)
    resp = urllib.request.urlopen(req, timeout=60)
    if accept == "application/json":
        return json.loads(resp.read().decode('utf-8'))
    return resp.read().decode('utf-8')

def should_skip(title):
    for kw in SKIP_KEYWORDS:
        if kw in title:
            return True
    return False

def upload_rag(title, content, tags):
    doc = {"title": title, "content": content, "tags": tags}
    data = json.dumps(doc).encode('utf-8')
    req = urllib.request.Request(RAG_URL, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read().decode('utf-8'))

def P(msg):
    print(msg, flush=True)

def main():
    mode = sys.argv[1] if len(sys.argv)>1 else "count"
    os.makedirs(OUT_DIR, exist_ok=True)

    P("🔍 获取笔记本列表...")
    nbs = get("/notebooks?$select=id,displayName").get("value",[])
    active = [n for n in nbs if n["displayName"] not in SKIP_NB]
    P(f"📚 共 {len(nbs)} 个笔记本，处理 {len(active)} 个（跳过事务性）\n")

    all_pages = []
    for nb in active:
        name = nb["displayName"]
        nid = urllib.parse.quote(nb["id"], safe='')
        time.sleep(0.3)
        try:
            secs = get(f"/notebooks/{nid}/sections?$select=id,displayName").get("value",[])
        except Exception as e:
            P(f"📓 {name}: ⚠️ {e}"); continue
        if not secs:
            P(f"📓 {name}: (空)"); continue

        nb_count = 0
        for sec in secs:
            sname = sec["displayName"]
            sid = urllib.parse.quote(sec["id"], safe='')
            time.sleep(0.3)
            try:
                pgs = get(f"/sections/{sid}/pages?$select=id,title,lastModifiedDateTime&$top=100").get("value",[])
            except Exception as e:
                P(f"  ⚠️ {name}/{sname}: {e}"); continue

            for p in pgs:
                t = p.get("title","无标题")
                if should_skip(t):
                    P(f"  ⏭️  跳过事务页: {t}")
                    continue
                all_pages.append({"id":p["id"],"title":t,"notebook":name,"section":sname,"modified":p.get("lastModifiedDateTime","")})
            nb_count += len(pgs)
            if pgs: P(f"  📄 {name} > {sname}: {len(pgs)} 页")

        P(f"📓 {name}: 共 {nb_count} 页\n")

    P(f"{'='*50}")
    P(f"📊 总计: {len(all_pages)} 个有效页面")

    with open(f'{OUT_DIR}/page-index.json','w') as f:
        json.dump(all_pages, f, ensure_ascii=False, indent=2)

    if mode == "count":
        P("✅ 统计完成，页面索引已保存"); return

    # === EXPORT ===
    P(f"\n🚀 开始导出...\n")
    ok=0; fail=0; skip=0; chars=0

    for i, pg in enumerate(all_pages):
        pid = pg["id"]
        title = pg["title"]
        nb = pg["notebook"]
        sec = pg["section"]
        tag = f"[{i+1}/{len(all_pages)}]"

        time.sleep(0.3)
        try:
            html = get(f"/pages/{urllib.parse.quote(pid, safe='')}/content", accept="text/html")
        except Exception as e:
            P(f"  {tag} ❌ {nb}/{sec}/{title}: {e}"); fail+=1; continue

        md = h2t(html)
        if len(md) < 10:
            P(f"  {tag} ⏭️  {title} (内容太短)"); skip+=1; continue

        # Save .md file
        safe_name = re.sub(r'[\\/:*?"<>|]', '_', title)[:80]
        safe_nb = re.sub(r'[\\/:*?"<>|]', '_', nb)
        safe_sec = re.sub(r'[\\/:*?"<>|]', '_', sec)
        dir_path = f"{OUT_DIR}/{safe_nb}/{safe_sec}"
        os.makedirs(dir_path, exist_ok=True)
        
        full_md = f"# {title}\n\n> 来源: OneNote > {nb} > {sec}\n> 修改: {pg['modified']}\n\n{md}"
        with open(f"{dir_path}/{safe_name}.md", 'w') as f:
            f.write(full_md)

        # Upload to RAG
        try:
            upload_rag(
                title=f"[OneNote] {nb}/{sec}/{title}",
                content=full_md,
                tags=["onenote", nb, sec]
            )
            ok+=1; chars+=len(md)
            P(f"  {tag} ✅ {nb}/{sec}/{title} ({len(md)}字)")
        except Exception as e:
            # Still saved as file, just RAG upload failed
            P(f"  {tag} ⚠️ {title} 文件已保存，RAG上传失败: {e}")
            fail+=1

        if (i+1)%20==0:
            P(f"\n  --- 进度 {i+1}/{len(all_pages)} | ✅{ok} ❌{fail} ⏭️{skip} ---\n")

    P(f"\n{'='*50}")
    P(f"🎉 导出完成!")
    P(f"  ✅ 成功: {ok}")
    P(f"  ❌ 失败: {fail}")
    P(f"  ⏭️  跳过: {skip}")
    P(f"  📝 总字数: {chars:,}")
    P(f"  📁 文件目录: {OUT_DIR}")

    with open(f'{OUT_DIR}/export-stats.json','w') as f:
        json.dump({"success":ok,"failed":fail,"skipped":skip,"total_chars":chars,"total":len(all_pages)}, f, ensure_ascii=False, indent=2)

if __name__=="__main__":
    main()
