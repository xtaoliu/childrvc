import sys
exec(open('edit.py').read().split("# ---- 3. Strong/Weak ----")[0])
p21 = [p for p in doc.paragraphs if 'not equally conventional' in p.text][0]
replace_span(p21, " This is different from how natural the action is as a means of bringing about the result: The former concerns the expression, the latter the event.",
 " If whether a compound is possible depends on how the action relates to the result, how conventional it is may depend on this relation as well: An action that is a natural means of bringing about a result is likely to be described often with the corresponding RVC. The two are nonetheless distinct, because conventionality concerns the expression, whereas the relation concerns the event.")
doc.save(OUT); print(p21.text[-760:])
