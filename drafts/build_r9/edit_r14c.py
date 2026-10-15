import sys
exec(open('../r12/edit.py').read().split("# ---- 3. Strong/Weak ----")[0])
replace_span(find("RQ2."), "and is this difference larger in children than in adults?", "and do children differ from adults more for stronger- than for weaker-association V1s?")
replace_span(find("RVC descriptions are expected"), "This difference is expected to be larger in children than in adults: Adults accept V1 descriptions of zero-result events at high rates (Chen, 2017), whereas children’s stricter judgments leave room for the association to matter.",
 "In zero-result events, children are expected to accept descriptions with stronger-association V1s less often than adults, whereas the child–adult difference for weaker-association V1s is expected to be smaller or absent; that is, children’s stricter judgments of V1 descriptions (Chen, 2017; J. Liu et al., 2026) are expected to arise mainly when the action is strongly associated with the result.")
p86 = find("The second model addresses RQ2")
replace_span(p86, "and (c) the difference between children and adults in the association effect. Because adult acceptance in zero-result events may approach ceiling, the child–adult comparison is evaluated on the log-odds scale, and predicted probabilities are reported alongside.",
 "and (c) the difference in acceptance between children and adults in zero-result events, estimated separately for stronger- and weaker-association V1s. Because the prediction concerns how often children accept these descriptions, the child–adult differences are evaluated as differences in predicted acceptance probability. For weaker-association V1s, children and adults are considered equivalent if the 95% credible interval of the difference lies entirely within ±10 percentage points (Kruschke, 2018). Because adult acceptance may approach ceiling, the corresponding log-odds estimates and the Action–Result Association × Age Group interaction are also reported.")
# placeholder for equivalence bound
add_runs(p86, " [等价区间宽度待定]")
p116 = find("A larger association effect in children than in adults")
replace_span(p116, "A larger association effect in children than in adults would locate children’s stricter judgments mainly in V1s that name strongly associated actions.",
 "If children accept descriptions with stronger-association V1s less often than adults but do not differ from adults for weaker-association V1s, their stricter judgments would be located mainly in V1s that name strongly associated actions.")
replace_span(p116, "The pragmatic explanation fits less naturally with a larger difference in children,", "The pragmatic explanation fits less naturally with this pattern,")
replace_span(p116, "Because adult acceptance in zero-result events may approach ceiling, however, a larger child difference on the probability scale could partly reflect the adult ceiling, which is why the comparison is evaluated on the log-odds scale.",
 "Because adult acceptance in zero-result events may approach ceiling, however, a pattern found in acceptance probabilities need not hold on the log-odds scale, and conclusions about whether children are more sensitive than adults to action–result association take both scales into account.")
ref = find("Kou, X., & Hohenstein, J. (2024).")
insert_after(ref, "Kruschke, J. K. (2018). Rejecting or accepting parameter values in Bayesian estimation. *Advances in Methods and Practices in Psychological Science, 1*(2), 270–280. https://doi.org/10.1177/2515245918771304")
doc.save(OUT); print("ok")
