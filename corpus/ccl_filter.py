"""Classify CCL concordance lines as true RVC uses vs. string matches across word
boundaries (e.g., 指挥|灭火 for 挥灭, 阻挠|红军 for 挠红).

A line counts as a candidate RVC use when jieba segmentation of the local context
places a word boundary immediately before V1 and immediately after V2, i.e.,
neither V1 is absorbed into a preceding word nor V2 into a following word.
Candidates are then checked by hand (see corpus_check.md).
"""
import csv, glob, json, os, re, sys
import jieba
jieba.setLogLevel(60)

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ccl_raw")
for w in ["剥开","捏开","掀翻","拍翻","掰弯","按弯","撕破","拽破","吹灭","挥灭","踢倒","推倒",
          "掐醒","叫醒","涂红","挠红","夹碎","锤碎","捶碎"]:
    jieba.add_word(w, freq=5)  # let the RVC be a candidate unit without forcing it

def boundaries(s):
    pos, b = 0, {0}
    for tok in jieba.cut(s, HMM=False):
        pos += len(tok); b.add(pos)
    return b

def classify(q, line):
    parts = line.split(f" {q} ")
    if len(parts) < 2:
        return None
    left, right = parts[0].replace("...", "").strip(), parts[1].replace("...", "").strip()
    lt, rt = left[-4:], right[:4]
    s = lt + q + rt
    b = boundaries(s)
    return (len(lt) in b) and (len(lt) + len(q) in b), lt, rt

counts = json.load(open(os.path.join(RAW, "counts.json")))
rows = []
w = csv.writer(open(os.path.join(RAW, "lines_coded.csv"), "w", newline="", encoding="utf-8-sig"))
w.writerow(["query", "auto_rvc", "left", "query_", "right", "line"])
for q, n in counts.items():
    lines = open(os.path.join(RAW, f"{q}.txt"), encoding="utf-8").read().splitlines()[1:]
    lines = [re.sub(r"^.*?条\s+\d+\.\d+\s+", "", l) for l in lines if l.strip()]
    res = [(classify(q, l), l) for l in lines]
    res = [(r, l) for r, l in res if r]
    k = sum(r[0] for r, l in res)
    for r, l in res:
        w.writerow([q, int(r[0]), r[1], q, r[2], l[:160]])
    rows.append((q, n, len(res), k))
print("query docs lines_checked auto_true share")
for q, n, m, k in rows:
    print(q, n, m, k, f"{k/m:.2f}" if m else "-")
