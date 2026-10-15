import sys
exec(open('edit.py').read().split("# ---- 3. Strong/Weak ----")[0])
p21 = [p for p in doc.paragraphs if 'not equally conventional' in p.text][0]
# remove from " These combinations" to end, then append new text
full = p21.text; k = full.find(" These combinations are not equally conventional")
replace_span(p21, full[k:], "") if False else None
# italics exist inside the old span (chuī-miè etc.), so rebuild tail manually
pos = 0
for r in list(p21.runs):
    t = r.text; a, b = pos, pos + len(t); pos = b
    if b <= k: continue
    if a >= k: r._r.getparent().remove(r._r)
    else: r.text = t[:k - a]
add_runs(p21, " These combinations are not equally conventional, however. By *conventional* we mean how established an RVC is as an expression, that is, how commonly speakers use it: *chuī-miè* \"blow-extinguished\" is a common expression, whereas *huī-miè* \"wave-extinguished\" is hardly ever used. This is different from how natural the action is as a means of bringing about the result: The former concerns the expression, the latter the event. Existing accounts do not specify what makes a given action a more or less natural means of bringing about a given result. The next section addresses this relation.")
p63 = find("We also examined how conventional each RVC is")
replace_span(p63, "We also examined how conventional each RVC is. Conventionality concerns the RVC as an expression rather than the relation between the action and the result, but the two are likely to go together, because an action that reliably brings about a result is likely to be described often with the corresponding RVC. If the RVCs formed with stronger-association V1s are also more conventional, children may be more familiar with them, and familiarity with an RVC could itself affect how they interpret the corresponding V1 (see General Discussion). We therefore searched",
 "We also examined how conventional each RVC is. As noted in the Introduction, whether a V1 and a V2 combine depends on how the action named by V1 relates to the result named by V2. If the two actions in a pair differ in their association with the target result, this difference should also be reflected in the language, such that the RVC formed with the stronger-association V1 is the more conventional one. Corpus frequency thus provides a check on the contrast between the paired V1s that does not rely on the adult ratings, although conventionality concerns the RVC as an expression rather than the action–result relation itself. We therefore searched")
doc.save(OUT); print("ok")
