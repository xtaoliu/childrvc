"""Look up Zipf frequencies of the study's RVCs and V1s in wordfreq (zh).

Only items that are single entries in wordfreq's Chinese word list are reported
with a frequency; for other items wordfreq would return an estimate composed from
the parts, which is not a frequency of the compound, so they are reported as absent.
"""
import csv, sys
from wordfreq import zipf_frequency, iter_wordlist, tokenize

PAIRS = [  # pair, stronger RVC, stronger V1, weaker RVC, weaker V1
    (1, "剥开", "剥", "捏开", "捏"),
    (2, "掀翻", "掀", "拍翻", "拍"),
    (3, "掰弯", "掰", "按弯", "按"),
    (4, "撕破", "撕", "拽破", "拽"),
    (5, "吹灭", "吹", "挥灭", "挥"),
    (6, "踢倒", "踢", "推倒", "推"),
    (7, "掐醒", "掐", "叫醒", "叫"),
    (8, "涂红", "涂", "挠红", "挠"),
    (9, "擦干净", "擦", "冲干净", "冲"),
    (10, "夹碎", "夹", "锤碎", "锤"),
    (10, "夹碎", "夹", "捶碎", "捶"),
]

vocab = set(iter_wordlist("zh", wordlist="large"))

def look(w):
    if w in vocab:
        return f"{zipf_frequency(w, 'zh', wordlist='large'):.2f}"
    return "absent"

out = csv.writer(sys.stdout)
out.writerow(["pair", "stronger_RVC", "zipf", "stronger_V1", "zipf",
              "weaker_RVC", "zipf", "weaker_V1", "zipf", "tokenization_of_weaker_RVC"])
for p, sr, sv, wr, wv in PAIRS:
    out.writerow([p, sr, look(sr), sv, look(sv), wr, look(wr), wv, look(wv),
                  "/".join(tokenize(wr, "zh"))])
