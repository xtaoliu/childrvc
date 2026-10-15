import sys
exec(open('edit.py').read().split("# ---- 3. Strong/Weak ----")[0])
# 1. first mention of conventionality: distinguish expression vs event
p21 = [p for p in doc.paragraphs if 'not equally conventional' in p.text][0]
replace_span(p21, " These combinations are not equally conventional, however, and existing accounts do not specify what makes the action named by a given V1 a more or less natural means of bringing about a given result. The next section addresses this relation.", "")
add_runs(p21, " These combinations are not equally conventional, however: *chuī-miè* \"blow-extinguished\" is an established expression, whereas *huī-miè* \"wave-extinguished\" is hardly used. Conventionality is a property of the compound as an expression. It is related to, but distinct from, how natural the action named by V1 is as a means of bringing about the result named by V2, which is a property of the event. Existing accounts do not specify what makes a given action a more or less natural means of bringing about a given result. The next section addresses this relation.")
# 2. ratings are event-level
p25 = [p for p in doc.paragraphs if 'whereas waving at it is neither.' in p.text][0]
replace_span(p25, "whereas waving at it is neither.", "whereas waving at it is neither. Both ratings concern the relation between an action and a result in the event, not how conventional the corresponding RVC is.")
# 3. why CCL
p63 = find("We also examined how conventional each RVC is")
replace_span(p63, "We also examined how conventional each RVC is, for two reasons. First, as noted in the Introduction, V1–V2 combinations differ in how conventional they are, and an action that reliably brings about a result is likely to be described often with the corresponding RVC; corpus frequency thus characterizes the pairs independently of the adult ratings. Second, children may be more familiar with the RVCs formed with stronger-association V1s, and familiarity with an RVC could itself affect how they interpret the corresponding V1 (see General Discussion). We therefore searched",
 "We also examined how conventional each RVC is. Conventionality concerns the RVC as an expression rather than the relation between the action and the result, but the two are likely to go together, because an action that reliably brings about a result is likely to be described often with the corresponding RVC. If the RVCs formed with stronger-association V1s are also more conventional, children may be more familiar with them, and familiarity with an RVC could itself affect how they interpret the corresponding V1 (see General Discussion). We therefore searched")
doc.save(OUT); print("ok")
