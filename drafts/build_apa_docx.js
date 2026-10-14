// Build an APA 7 formatted .docx of the Introduction from Introduction_R8_APA.md.
// Conventions in the markdown source:
//   first line = title; "## " = APA Level 2 heading; "EX (n)|a.|line|gloss|translation" = glossed example;
//   [^1] footnote reference, "[^1]: text" footnote body; *x* = italic; ⟦...⟧ = author query (highlighted).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, Header, PageNumber,
  FootnoteReferenceRun, TabStopType, HighlightColor,
} = require("docx");

const SRC = path.join(__dirname, "Introduction_R8_APA.md");
const OUT = path.join(__dirname, "Introduction_R8_APA.docx");
const FONT = "Times New Roman";
const SIZE = 24; // 12 pt
const DOUBLE = { line: 480, before: 0, after: 0 };

function runs(text, base = {}) {
  text = text.replace(/"([^"]*)"/g, "\u201C$1\u201D").replace(/(\w)'/g, "$1\u2019");
  // split into italic, query and plain segments
  const out = [];
  const re = /(\*[^*]+\*|⟦[^⟧]+⟧|\[\^\d+\])/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size: SIZE, ...base }));
    const t = m[0];
    if (t.startsWith("*")) out.push(new TextRun({ text: t.slice(1, -1), italics: true, font: FONT, size: SIZE, ...base }));
    else if (t.startsWith("⟦")) out.push(new TextRun({ text: t, font: FONT, size: SIZE, highlight: HighlightColor.YELLOW, ...base }));
    else out.push(new FootnoteReferenceRun(parseInt(t.match(/\d+/)[0], 10)));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, size: SIZE, ...base }));
  return out;
}

const body = [];
const footnotes = {};
const lines = fs.readFileSync(SRC, "utf8").split("\n");
let first = true;
for (const raw of lines) {
  const line = raw.trimEnd();
  if (!line) continue;
  if (first) { // title, bold centered (APA 7 professional paper: title repeated on first page of text)
    body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: DOUBLE, children: runs(line, { bold: true }) }));
    first = false; continue;
  }
  let m;
  if ((m = line.match(/^\[\^(\d+)\]:\s*(.*)$/))) {
    footnotes[m[1]] = { children: [new Paragraph({ spacing: { line: 240 }, children: runs(m[2], { size: 20 }).map(r => r) })] };
    continue;
  }
  if (line.startsWith("## ")) { // APA Level 2: flush left, bold, title case
    body.push(new Paragraph({ spacing: DOUBLE, children: runs(line.slice(3), { bold: true }) }));
    continue;
  }
  if (line.startsWith("EX ")) { // glossed example: number, letter, three lines
    const [num, letter, form, gloss, trans] = line.slice(3).split("|");
    const tabs = [{ type: TabStopType.LEFT, position: 720 }, { type: TabStopType.LEFT, position: 1260 }];
    const sp = { line: 240, before: 0, after: 0 };
    const spFirst = { line: 240, before: letter.trim() === "a." ? 240 : 0, after: 0 };
    body.push(new Paragraph({ tabStops: tabs, spacing: spFirst, keepNext: true, children: [
      new TextRun({ text: num.trim(), font: FONT, size: SIZE }), new TextRun({ text: "\t" + letter + "\t", font: FONT, size: SIZE }),
      new TextRun({ text: form.replace(/'/g, "\u2019"), italics: true, font: FONT, size: SIZE })] }));
    body.push(new Paragraph({ tabStops: tabs, spacing: sp, keepNext: true, children: [new TextRun({ text: "\t\t" + gloss, font: FONT, size: SIZE })] }));
    body.push(new Paragraph({ tabStops: tabs, spacing: { line: 240, before: 0, after: 240 }, children: [new TextRun({ text: "\t\t" + trans.replace(/"([^"]*)"/g, "\u201C$1\u201D"), font: FONT, size: SIZE })] }));
    continue;
  }
  if (/^RQ\d:/.test(line)) { // research questions: indented block
    const [label, ...rest] = line.split(":");
    body.push(new Paragraph({ spacing: DOUBLE, indent: { left: 720 }, children: [
      new TextRun({ text: label + ".", italics: true, font: FONT, size: SIZE }), ...runs(rest.join(":"))] }));
    continue;
  }
  body.push(new Paragraph({ spacing: DOUBLE, indent: { firstLine: 720 }, children: runs(line) }));
}

// References (APA 7): new page, centered bold heading, hanging indent 0.5 in
const refs = fs.readFileSync(path.join(__dirname, "references_apa.txt"), "utf8").split("\n").filter(Boolean);
body.push(new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: DOUBLE, children: runs("References", { bold: true }) }));
for (const r of refs) body.push(new Paragraph({ spacing: DOUBLE, indent: { left: 720, hanging: 720 }, children: runs(r) }));

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: SIZE } } } },
  footnotes,
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: SIZE })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("wrote", OUT); });
