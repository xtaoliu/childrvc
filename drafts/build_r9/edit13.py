import sys, re
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2]]
exec(open('edit.py').read().split("# ---- 3. Strong/Weak ----")[0])  # helpers: find, replace_span, add_runs, insert_after
p23 = find("What a V1 conveys about a result")
replace_span(p23, "allow zero-change construals (Martin et al., 2023).", "allow zero-change construals (Martin et al., 2020, 2026).")
replace_span(p23, "span adverbials (Martin et al., 2023).", "span adverbials (Martin et al., 2020, 2026). This diagnostic, however, is binary, and it tracks whether a result construal of the verb phrase is available, which the object and the context can supply; it therefore does not grade how strongly a verb implies a result. The V1s in the present materials were originally selected as strong and weak with this diagnostic, but the present study characterizes them by adult ratings instead (see Materials).")
p48 = find("When the materials were designed")
replace_span(p48, "following Martin et al. (2020, 2023).", "following Martin et al. (2020, 2026).")
ref = find("Martin, F., Sun, H., Liu, J., & Demirdache, H. (2023).")
replace_span(ref, "Demirdache, H. (2023).", "Demirdache, H. (2020).")
insert_after(ref, "Martin, F., Sun, H., Liu, J., & Demirdache, H. (2026). *Zero-change construals as a probe into event structure: Mandarin Chinese simple verbs and their anticausative vs. antiagentive alternants* [Manuscript]. ResearchGate. ⟦待核：发表状态与链接⟧")
assert not any("2023)" in p.text and "Martin" in p.text for p in doc.paragraphs)
doc.save(OUT); print("ok")
