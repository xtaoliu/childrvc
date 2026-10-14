"""Query the CCL modern Chinese corpus (PKU) for the study's RVCs.

Records the number of documents containing each string (CCL reports document
counts, not token counts) and saves up to MAXLINES concordance lines per query
for manual checking of false matches. Queries are sent sequentially with a pause.
"""
import re, html, json, os, subprocess, sys, time, urllib.parse

BASE = "http://ccl.pku.edu.cn:8080/ccl_corpus/search"
PROXY = os.environ["HTTPS_PROXY"]
OUT = os.path.join(os.path.dirname(__file__), "ccl_raw")
MAXLINES = int(os.environ.get("MAXLINES", "200"))

def fetch(q, start=0, num=50):
    params = dict(q=q, dir="xiandai", start=start, num=num, index="FullIndex",
                  outputFormat="HTML", encoding="UTF-8", maxLeftLength=30,
                  maxRightLength=30, orderStyle="score", LastQuery="", scopestr="")
    url = BASE + "?" + urllib.parse.urlencode(params)
    r = subprocess.run(["curl", "-sS", "-m", "90", "--proxytunnel", "-x", PROXY, url],
                       capture_output=True)
    return r.stdout.decode("utf-8", errors="replace")

def parse(page):
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)))
    m = re.search(r"共在\s*(\d+)\s*个文档中出现", text)
    n = int(m.group(1)) if m else (0 if "没有找到" in text or "共在 0" in text else None)
    lines = re.findall(r"\d+\.\d+\s+(.*?)\s+上下文", text)
    return n, lines

def run(terms):
    res = {}
    for q in terms:
        page = fetch(q, 0, 50)
        n, lines = parse(page)
        start = 50
        while n and start < min(n, MAXLINES):
            time.sleep(1.5)
            _, more = parse(fetch(q, start, 50))
            if not more: break
            lines += more; start += 50
        res[q] = n
        with open(os.path.join(OUT, f"{q}.txt"), "w", encoding="utf-8") as f:
            f.write(f"# {q}\tdocuments={n}\n" + "\n".join(lines) + "\n")
        print(q, n, len(lines), flush=True)
        time.sleep(1.5)
    return res

if __name__ == "__main__":
    terms = sys.argv[1:]
    res = run(terms)
    path = os.path.join(OUT, "counts.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update(res)
    json.dump(old, open(path, "w"), ensure_ascii=False, indent=1)
