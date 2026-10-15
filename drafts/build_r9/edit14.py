import sys
exec(open('edit.py').read().split("# ---- 3. Strong/Weak ----")[0])
ref = find("Martin, F., Sun, H., Liu, J., & Demirdache, H. (2026).")
replace_span(ref, "[Manuscript]. ResearchGate. ", "[Preprint]. ResearchGate. ")
for r in ref.runs:
    if "待核：发表状态与链接" in r.text: r.text = r.text.replace("待核：发表状态与链接", "待补：ResearchGate 链接或 DOI")
doc.save(OUT); print(ref.text)
