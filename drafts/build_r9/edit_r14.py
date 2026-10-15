import sys, re
exec(open('../r12/edit.py').read().split("# ---- 3. Strong/Weak ----")[0])
AR = "Action–Result Association"
R = [
 ("RQ2.", "differs between the two sets,", "differs between them,"),
 ("The materials comprise 10 pairs", "The 20 expressions form two sets of 10: the expected stronger-association expressions and their expected weaker-association partners.", "The 20 expressions thus comprise 10 expected stronger-association expressions and their 10 expected weaker-association partners."),
 ("When the materials were designed", "the two sets were defined as Strong and Weak V1s", "the V1s were classified as Strong and Weak V1s"),
 ("When the materials were designed", "Several V1s in the weaker set are also compatible", "Several of the Weak V1s in the present materials are also compatible"),
 ("When the materials were designed", "Third, the stronger set combined verbs", "Third, the Strong V1s grouped verbs"),
 ("Note. Likelihood was rated", "set labels follow the original design", "the stronger/weaker labels follow the original design"),
 ("Because each expression was paired", "Each participant saw the 10 videos of one set and described", "Each participant saw either the 10 videos of the stronger-association actions or the 10 videos of the weaker-association actions and described"),
 ("Four lists were constructed", "the 10 expressions of one set were presented first and the 10 expressions of the other set second, with the pairs", "the 10 stronger-association expressions and the 10 weaker-association expressions were presented in separate halves, with the pairs"),
 ("Four lists were constructed", "The stronger-association set came first in Lists 1 and 3, and the weaker-association set came first in Lists 2 and 4.", "The stronger-association expressions came first in Lists 1 and 3, and the weaker-association expressions came first in Lists 2 and 4."),
 ("A pair was retained", "cannot be assigned to the two sets.", "cannot be classified as stronger- or weaker-association actions."),
 ("Form (RVC vs. V1) and", "Form (RVC vs. V1) and Set (Stronger vs. Weaker association) were manipulated between participants, and result realization (full vs. zero) within participants.", f"Form (RVC vs. V1) and {AR} (Stronger vs. Weaker) were manipulated between participants, and Result Realization (Full vs. Zero) within participants."),
 ("Form (RVC vs. V1) and", "all from the same set,", "either all stronger-association or all weaker-association actions,"),
 ("Form (RVC vs. V1) and", "across the two event lists for each set,", "across the two event lists with the same actions,"),
 ("With about four children", "the V1 descriptions of each set were judged by", "the V1 descriptions of the stronger-association actions, like those of the weaker-association actions, were judged by"),
 ("With about four children", "Comparisons between the two sets are", "Comparisons between stronger- and weaker-association V1s are"),
 ("The first model addresses RQ1", "result realization (full vs. zero), age group", "Result Realization (Full vs. Zero), age group"),
 ("The first model addresses RQ1", "V1 trials from the two sets are pooled", "V1 trials with stronger- and weaker-association V1s are pooled"),
 ("The first model addresses RQ1", "a by-participant slope for result realization; and by-item slopes for form, result realization, and age group", "a by-participant slope for Result Realization; and by-item slopes for form, Result Realization, and age group"),
 ("The first model addresses RQ1", "which indicates whether result realization affects", "which indicates whether Result Realization affects"),
 ("The second model addresses RQ2", "It includes set (stronger vs. weaker association), result realization, age group", f"It includes {AR} (Stronger vs. Weaker), Result Realization, age group"),
 ("The second model addresses RQ2", "a by-participant slope for result realization; by-item slopes for result realization and age group; and a by-pair slope for set,", f"a by-participant slope for Result Realization; by-item slopes for Result Realization and age group; and a by-pair slope for {AR},"),
 ("The second model addresses RQ2", "(a) the difference between sets in zero-result events in each age group;", "(a) the difference in acceptance between stronger- and weaker-association V1s in zero-result events in each age group (hereafter, the association effect);"),
 ("The second model addresses RQ2", "(b) the Set × Result Realization interaction, which assesses whether this difference is larger", f"(b) the {AR} × Result Realization interaction, which assesses whether the association effect is larger"),
 ("The second model addresses RQ2", "the zero-result difference between sets.", "the association effect."),
 ("Three analyses assess", "assigned to sets as in the original design", "classified as stronger- or weaker-association as in the original design"),
 ("Three analyses assess", "reported by result realization and age group, to show whether a difference between sets is carried", "reported by Result Realization and age group, to show whether the association effect is carried"),
 ("The 40 critical videos were divided", "Each list contained the 10 actions of one set, five", "Each list contained either the 10 stronger-association or the 10 weaker-association actions, five"),
 ("All 10 pairs are included", "do not require the actions to be assigned to sets.", "do not require the actions to be classified as stronger- or weaker-association."),
 ("Two binary outcomes are modeled", "Each model includes result realization, age group", "Each model includes Result Realization, age group"),
 ("Two binary outcomes are modeled", "a by-participant slope for result realization; and by-item slopes for result realization and age group", "a by-participant slope for Result Realization; and by-item slopes for Result Realization and age group"),
 ("Two binary outcomes are modeled", "reported by result realization and age group and modeled", "reported by Result Realization and age group and modeled"),
 ("If children reject V1 descriptions", "a difference between sets cannot be attributed", "an association effect cannot be attributed"),
 ("If children reject V1 descriptions", "A difference between sets in adults", "An association effect in adults"),
 ("Why action–result association might matter", "interpretations of a difference between sets,", "interpretations of an association effect,"),
 ("A larger difference between sets in children", "A larger difference between sets in children", "A larger association effect in children"),
 ("Because the stronger- and weaker-association expressions differ", "underlies a difference between sets;", "underlies an association effect;"),
 ("Because the stronger- and weaker-association expressions differ", "The difference between sets also goes together", "The contrast between stronger- and weaker-association expressions also goes together"),
 ("Because the stronger- and weaker-association expressions differ", "an alternative account of a difference between sets.", "an alternative account of an association effect."),
 ("Several limitations follow", "Fourth, with eight pairs and sets assigned between participants, each difference between sets rests", "Fourth, with eight pairs and with stronger- and weaker-association V1s judged by different participants, each association effect rests"),
 ("Several limitations follow", "and a difference between sets needs to be replicated", "and an association effect needs to be replicated"),
]
for prefix, old, new in R:
    hits = [p for p in doc.paragraphs if p.text.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    replace_span(hits[0], old, new)
# placeholders: body ⟦⟧ -> [ ]; references: delete
for p in doc.paragraphs:
    if p.style.name == "Reference":
        if "⟦" in p.text:
            runs = p.runs; k = next(i for i, r in enumerate(runs) if "⟦" in r.text)
            pre, _, _ = runs[k].text.partition("⟦")
            runs[k].text = pre
            for r in runs[k + 1:]: r._r.getparent().remove(r._r)
            # strip trailing space
            for r in reversed(p.runs):
                if r.text:
                    r.text = r.text.rstrip(); break
            assert "⟦" not in p.text and "⟧" not in p.text
    else:
        for r in p.runs:
            if "⟦" in r.text or "⟧" in r.text:
                r.text = r.text.replace("⟦", "[").replace("⟧", "]")
# leftover check
left = [(i, p.text) for i, p in enumerate(doc.paragraphs) if re.search(r"\bsets?\b", p.text)]
print("remaining 'set':", [(i, re.findall(r".{0,40}\bsets?\b.{0,20}", t)) for i, t in left])
print("⟦ left:", any("⟦" in p.text or "⟧" in p.text for p in doc.paragraphs))
doc.save(OUT)
