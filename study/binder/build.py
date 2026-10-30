"""Build the CoA open-book binder: python build.py [--preview]"""
import sys, os, glob, re, weasyprint, pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "cheatsheet", "fonts")
parts = sorted(glob.glob(os.path.join(HERE, "parts", "*.html")))
body = "\n".join(open(p).read() for p in parts)

NAVY, LIGHT, ORANGE = "#1f3a5f", "#f2f5fa", "#9a5b00"
css = f"""
@font-face {{ font-family: 'DV'; src: url('file://{FONTS}/DejaVuSansCondensed.ttf'); }}
@font-face {{ font-family: 'DV'; src: url('file://{FONTS}/DejaVuSansCondensed-Bold.ttf'); font-weight: bold; }}
@font-face {{ font-family: 'DV'; src: url('file://{FONTS}/DejaVuSansCondensed-Oblique.ttf'); font-style: italic; }}
@font-face {{ font-family: 'DV'; src: url('file://{FONTS}/DejaVuSansCondensed-BoldOblique.ttf'); font-weight: bold; font-style: italic; }}
@font-face {{ font-family: 'DVM'; src: url('file://{FONTS}/DejaVuSansMono.ttf'); }}
@page {{
  size: A4; margin: 14mm 14mm 15mm 14mm;
  @bottom-left {{ content: "CoA Open-Book Binder  ·  " string(sec); font-family: 'DV'; font-size: 7.5pt; color: #666; }}
  @bottom-right {{ content: "p. " counter(page); font-family: 'DV'; font-size: 9pt; color: #333; }}
}}
html {{ font-family: 'Noto Sans', 'DV', sans-serif; font-size: 9.6pt; line-height: 1.38; color: #1a1a1a; }}
section {{ string-set: sec attr(data-short); }}
section.tab {{ break-before: page; }}
h1.title {{ font-size: 25pt; line-height: 1.15; margin: 18mm 0 4mm; }}
p.subtitle {{ font-size: 11pt; color: #444; margin: 0 0 2mm; }}
.tabhead {{ background: {NAVY}; color: #fff; font-size: 15pt; font-weight: bold; padding: 5pt 9pt;
            border-radius: 4pt; margin: 0 0 6pt; }}
.tabhead .sm {{ font-size: 10pt; font-weight: normal; }}
h3 {{ color: {NAVY}; font-size: 11.5pt; border-bottom: 1.2pt solid {NAVY}; margin: 10pt 0 5pt; padding-bottom: 1pt;
      break-after: avoid; }}
h4 {{ color: {NAVY}; font-size: 10pt; margin: 6pt 0 3pt; break-after: avoid; }}
p {{ margin: 0 0 5pt; }}
ul, ol {{ margin: 0 0 5pt; padding-left: 15pt; }}
li {{ margin-bottom: 2pt; }}
.id {{ color: {ORANGE}; font-style: italic; }}
.small {{ font-size: 8pt; color: #444; }}
p.links {{ font-size: 8.5pt; color: #333; background: #eef1f6; padding: 2pt 6pt; border-radius: 3pt; }}
.cs {{ display: inline-block; background: {NAVY}; color: #fff; font-weight: bold; font-size: 0.82em;
       padding: 0 4pt; border-radius: 6pt; }}
a.pg {{ color: {NAVY}; font-weight: bold; text-decoration: none; }}
a.pg::after {{ content: "p." target-counter(attr(href), page); }}
.row {{ column-count: 2; column-gap: 9pt; margin-bottom: 2pt; }}
.col {{ display: block; }}
.formula, .ex, .trap, .tip, .method, .check {{ border-radius: 4pt; padding: 5pt 7pt; margin: 0 0 7pt; break-inside: avoid; }}
.formula {{ background: {LIGHT}; border: 0.8pt solid {NAVY}; }}
.ex {{ border: 0.8pt solid #b9c2cf; }}
.ex .et, .ct {{ color: {NAVY}; font-weight: bold; margin: 0 0 2pt; }}
.src {{ float: right; font-weight: normal; color: #777; font-size: 8pt; }}
.trap {{ background: #fdf0f0; border: 0.8pt solid #c0392b; }}
.trap b:first-child {{ color: #c0392b; }}
.tip {{ background: #eef7ee; border-left: 3pt solid #2e7d32; border-radius: 0 4pt 4pt 0; }}
.method {{ border: 0.9pt dashed #555; }}
.check {{ background: #fffbea; border: 0.8pt solid #c9a227; }}
.ans {{ background: #fff3b0; font-weight: bold; padding: 0 2pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 0 0 7pt; break-inside: auto; }}
tr {{ break-inside: avoid; }}
td, th {{ border: 0.5pt solid #9aa3af; padding: 2pt 4pt; vertical-align: top; text-align: left; }}
th {{ background: #dfe6f1; }}
table.mono td {{ font-family: 'DVM', monospace; font-size: 8.8pt; }}
table.toc td:last-child, table.toc th:last-child {{ text-align: center; white-space: nowrap; }}
table.idx tr.grp td {{ background: {NAVY}; color: #fff; font-weight: bold; text-align: center; }}
code, .mono {{ font-family: 'DVM', monospace; font-size: 0.92em; }}
.kq {{ border-top: 1.2pt solid {NAVY}; padding-top: 4pt; margin-top: 7pt; break-inside: avoid; }}
.kq .kt {{ color: {NAVY}; font-weight: bold; font-size: 10.5pt; }}
.qq {{ margin: 0 0 9pt; break-inside: avoid; }}
.qq .qn {{ color: {NAVY}; font-weight: bold; }}
.qq .pts {{ float: right; color: #777; font-size: 8pt; }}
.qq .en {{ font-style: italic; color: #555; font-size: 8.8pt; }}
"""
html = f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
out = os.path.join(HERE, "CoA_Open_Book_Binder.pdf")
doc = weasyprint.HTML(string=html, base_url=HERE).render()
doc.write_pdf(out)

# sanity: every link target exists
ids = set(re.findall(r'id="([^"]+)"', body))
missing = sorted(set(re.findall(r'href="#([^"]+)"', body)) - ids)
d = pymupdf.open(out)
print("pages:", len(d), "| missing link targets:", missing or "none")
if "--preview" in sys.argv:
    os.makedirs(os.path.join(HERE, "prev"), exist_ok=True)
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=80).save(os.path.join(HERE, "prev", f"p{i+1:02d}.png"))
