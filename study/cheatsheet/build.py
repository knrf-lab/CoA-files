"""Build the 2-sided cheat sheet: python build.py [front_pt] [back_pt] [--preview]"""
import sys, os, weasyprint, pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
front = float(args[0]) if len(args) > 0 else 7.9
back = float(args[1]) if len(args) > 1 else 8.5
body = open(os.path.join(HERE, "content.html")).read()

def face(file, weight, style):
    return (f"@font-face {{ font-family: 'Sheet'; src: url('file://{FONTS}/{file}'); "
            f"font-weight: {weight}; font-style: {style}; }}")

NAVY, LIGHT = "#1f3a5f", "#f2f5fa"
css = "\n".join([
    face("DejaVuSansCondensed.ttf", "normal", "normal"),
    face("DejaVuSansCondensed-Bold.ttf", "bold", "normal"),
    face("DejaVuSansCondensed-Oblique.ttf", "normal", "italic"),
    face("DejaVuSansCondensed-BoldOblique.ttf", "bold", "italic"),
    f"@font-face {{ font-family: 'SheetMono'; src: url('file://{FONTS}/DejaVuSansMono.ttf'); }}",
]) + f"""
@page {{ size: A4; margin: 5mm; }}
body {{ font-family: 'Sheet'; line-height: 1.2; color: #111; margin: 0; }}
section.page {{ column-count: 2; column-gap: 4mm; }}
section.page:first-child {{ font-size: {front}pt; }}
section.page + section.page {{ break-before: page; font-size: {back}pt; }}
.bar {{ column-span: all; background: {NAVY}; color: #fff; font-weight: bold; font-size: 1.3em;
        padding: 2pt 5pt; border-radius: 3pt; margin-bottom: 3pt; }}
.bar .sub {{ font-weight: normal; font-size: 0.7em; margin-left: 6pt; }}
.bar .tag {{ background: #fff; color: {NAVY}; }}
h2 {{ font-size: 1.1em; color: {NAVY}; border-bottom: 1pt solid {NAVY}; margin: 3pt 0 2pt;
      break-after: avoid; }}
p {{ margin: 0 0 1.5pt; }}
.tag {{ display: inline-block; background: {NAVY}; color: #fff; font-weight: bold; font-size: 0.85em;
        padding: 0 3pt; border-radius: 6pt; margin-left: 2pt; }}
.card, .box {{ border: 0.6pt solid #9aa9bf; border-radius: 3pt; padding: 2pt 4pt; margin: 0 0 3pt;
               break-inside: avoid; }}
.box {{ background: {LIGHT}; }}
p.q {{ margin-bottom: 1.5pt; }}
p.ans {{ font-weight: bold; background: #fff3b0; padding: 0.5pt 3pt; display: inline-block; margin: 0; }}
p.bt {{ font-weight: bold; color: {NAVY}; font-size: 1.08em; margin-bottom: 1.5pt; }}
p.bt .tag {{ margin: 0 3pt 0 0; }}
ol.pq {{ margin: 0 0 3pt; padding-left: 13pt; }}
ol.pq li {{ margin-bottom: 1.5pt; }}
.key {{ border: 0.8pt dashed #b08900; background: #fffbea; border-radius: 3pt; padding: 2pt 4pt; }}
.key p {{ margin-bottom: 2pt; }}
mark {{ background: #fff3b0; font-weight: bold; }}
ul {{ margin: 0; padding-left: 10pt; }}
li {{ margin-bottom: 1pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 1pt 0 2pt; background: #fff; }}
td, th {{ border: 0.4pt solid #9aa9bf; padding: 0.3pt 2pt; vertical-align: top; text-align: left; }}
th {{ background: #dfe6f1; }}
table.hex td {{ font-family: 'SheetMono'; text-align: center; }}
"""
html = f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
out = os.path.join(HERE, "CoA_Midterm_CheatSheet.pdf")
weasyprint.HTML(string=html, base_url=HERE).write_pdf(out)
d = pymupdf.open(out)
starts = [pg.get_text().strip().split("\n")[0] for pg in d]
ok = len(d) == 2 and starts[1].startswith("SIDE B")
print("pages:", len(d), "| page starts:", [s[:20] for s in starts], "| OK" if ok else "| OVERFLOW")
if "--preview" in sys.argv:
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=120).save(os.path.join(HERE, f"prev_{i+1}.png"))
