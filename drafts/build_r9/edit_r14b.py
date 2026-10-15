import sys, re
exec(open('../r12/edit.py').read().split("# ---- 3. Strong/Weak ----")[0])
P = doc.paragraphs
TONE = re.compile(r'[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]')
n = 0
for i in [20, 21, 29, 30, 33]:
    for r in P[i].runs:
        if not r.italic and TONE.search(r.text) and re.fullmatch(r"[\w\-āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ ]+", r.text.strip()):
            r.italic = True; n += 1
print("italicized", n)
# 2. cross-reference
replace_span(find("The study comprises a comprehension experiment"), "(see Method)", "(see Pair Selection)")
# 3. heading
h = [p for p in P if p.text.strip() == "RVC and V1s"][0]; replace_span(h, "RVC and V1s", "RVC and V1 Descriptions")
# 4. Form / Age Group as factors
reps = [
 ("The first model addresses RQ1", "It includes form (RVC vs. V1), Result Realization (Full vs. Zero), age group (", "It includes Form (RVC vs. V1), Result Realization (Full vs. Zero), Age Group ("),
 ("The first model addresses RQ1", "by-item slopes for form, Result Realization, and age group", "by-item slopes for Form, Result Realization, and Age Group"),
 ("The second model addresses RQ2", "Result Realization, age group, and their interactions", "Result Realization, Age Group, and their interactions"),
 ("The second model addresses RQ2", "by-item slopes for Result Realization and age group", "by-item slopes for Result Realization and Age Group"),
 ("Three analyses assess", "reported by Result Realization and age group,", "reported by Result Realization and Age Group,"),
 ("Two binary outcomes are modeled", "Each model includes Result Realization, age group, and their interaction", "Each model includes Result Realization, Age Group, and their interaction"),
 ("Two binary outcomes are modeled", "by-item slopes for Result Realization and age group.", "by-item slopes for Result Realization and Age Group."),
 ("Two binary outcomes are modeled", "reported by Result Realization and age group and modeled", "reported by Result Realization and Age Group and modeled"),
]
for pre, o, nw in reps: replace_span(find(pre), o, nw)
# clean empty highlighted runs left in references
for p in P:
    if p.style.name == "Reference":
        for r in list(p.runs):
            if r.text == "" and r.font.highlight_color: r._r.getparent().remove(r._r)
doc.save(OUT); print("ok")
