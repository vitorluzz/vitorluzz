#!/usr/bin/env python3
"""
Generate the neofetch-style GitHub profile SVGs (dark_mode.svg / light_mode.svg).

Reads the ASCII portrait from ascii_art.txt (same folder) and renders it next to
a neofetch-style info panel using GitHub's syntax colors.

Usage:
    python generate.py

Edit the INFO / stats values below to update the profile, then re-run.
No third-party dependencies required.
"""
import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
ART_PATH = os.path.join(HERE, "ascii_art.txt")

def load_ascii():
    with open(ART_PATH, encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]
    while lines and not lines[-1].strip():
        lines.pop()
    return lines

# ---------- content ----------
HOST_USER, HOST_HOST = "vitorluzz", "github"

INFO = [
    ("kv",  ["Role"],                      "AI Engineer & Solutions Architect"),
    ("kv",  ["Company"],                   "Stefanini Consulting"),
    ("kv",  ["Education"],                 "B.Tech Systems Analysis & Dev (2026)"),
    ("kv",  ["Location"],                  "São Paulo, Brazil"),
    ("kv",  ["OS"],                        "Linux · WSL2 · macOS"),
    ("blank",),
    ("kv",  ["Languages", "Programming"],  "Python, Rust, SQL, TypeScript"),
    ("kv",  ["Languages", "AI"],           "LangChain, LangGraph, Claude, RAG"),
    ("kv",  ["Languages", "Data"],         "PySpark, Databricks, Airflow, Kafka"),
    ("kv",  ["Languages", "Real"],         "Portuguese, English, Spanish"),
    ("blank",),
    ("kv",  ["Focus", "Now"],              "Auditable multi-agent AI in banking"),
    ("kv",  ["Focus", "Loves"],            "Agentic systems · guardrails · HITL"),
    ("blank",),
    ("section", "Contact"),
    ("kv",  ["Email"],                     "jaun.campos04@gmail.com"),
    ("kv",  ["LinkedIn"],                  "in/vitorluzz"),
    ("kv",  ["GitHub"],                    "vitorluzz"),
    ("blank",),
    ("section", "GitHub Stats"),
    ("stats1", None),
    ("stats2", None),
]

REPOS, CONTRIB, STARS, CONTRIBUTIONS, FOLLOWERS = "24", "18", "15", "386", "7"

T = 34            # alignment column (chars) where value begins
LINEW = 56        # width (chars) of section-header dashed lines
Y0, DY = 30, 20   # info panel: first baseline y, line height
INFO_FS = 16
ASCII_FS = 12     # ascii font-size (smaller -> more compact portrait)
ASCII_DY = 12
CHARW_ASCII = ASCII_FS * 0.60

def esc(s):
    return html.escape(s, quote=False)

def key_spans(parts):
    svg, length = "", 0
    for i, p in enumerate(parts):
        if i:
            svg += "."; length += 1
        svg += f'<tspan class="key">{esc(p)}</tspan>'; length += len(p)
    return svg, length

def kv_line(x, y, parts, value):
    ksvg, klen = key_spans(parts)
    dots = max(1, T - 5 - klen)
    leader = " " + "." * dots + " "
    return (f'<tspan x="{x}" y="{y}"><tspan class="cc">. </tspan>{ksvg}:'
            f'<tspan class="cc">{leader}</tspan>'
            f'<tspan class="value">{esc(value)}</tspan></tspan>')

def section_line(x, y, name):
    text = f"- {name} "
    dashes = "-" * max(3, LINEW - len(text))
    return f'<tspan x="{x}" y="{y}"><tspan class="hd">{esc(text)}</tspan><tspan class="cc">{dashes}</tspan></tspan>'

def host_line(x, y):
    text = f"{HOST_USER}@{HOST_HOST} "
    dashes = "-" * max(3, LINEW - len(text))
    return (f'<tspan x="{x}" y="{y}"><tspan class="host">{esc(HOST_USER)}</tspan>'
            f'<tspan class="cc">@</tspan><tspan class="host2">{esc(HOST_HOST)}</tspan>'
            f'<tspan class="cc"> {dashes}</tspan></tspan>')

def stats1_line(x, y):
    return (f'<tspan x="{x}" y="{y}"><tspan class="cc">. </tspan>'
            f'<tspan class="key">Repos</tspan>:<tspan class="cc"> ...... </tspan>'
            f'<tspan class="value">{REPOS}</tspan> {{<tspan class="key">Contributed</tspan>: '
            f'<tspan class="value">{CONTRIB}</tspan>}}  |  <tspan class="key">Stars</tspan>:'
            f'<tspan class="cc"> ...... </tspan><tspan class="value">{STARS}</tspan></tspan>')

def stats2_line(x, y):
    return (f'<tspan x="{x}" y="{y}"><tspan class="cc">. </tspan>'
            f'<tspan class="key">Contributions</tspan>:<tspan class="cc"> .... </tspan>'
            f'<tspan class="value">{CONTRIBUTIONS}</tspan>  |  <tspan class="key">Followers</tspan>:'
            f'<tspan class="cc"> ... </tspan><tspan class="value">{FOLLOWERS}</tspan></tspan>')

THEMES = {
    "dark":  dict(bg="#0d1117", stroke="#30363d", text="#c9d1d9", ascii="#c9d1d9",
                  key="#ffa657", value="#a5d6ff", host="#7ee787", host2="#a5d6ff",
                  hd="#d2a8ff", cc="#6e7681"),
    "light": dict(bg="#ffffff", stroke="#d0d7de", text="#1f2328", ascii="#1f2328",
                  key="#953800", value="#0a3069", host="#116329", host2="#0550ae",
                  hd="#8250df", cc="#6e7781"),
}

def build(art, theme):
    art_w = max((len(r) for r in art), default=0)
    RX = int(15 + art_w * CHARW_ASCII + 40)

    info_rows = 1 + len(INFO)
    info_bottom = Y0 + (info_rows - 1) * DY
    ascii_h = len(art) * ASCII_DY
    ascii_y0 = max(ASCII_DY + 4, Y0 + (info_bottom - Y0 - ascii_h) // 2)

    # build info panel
    right = [host_line(RX, Y0)]
    for i, item in enumerate(INFO, start=1):
        y = Y0 + i * DY
        t = item[0]
        if t == "kv":        right.append(kv_line(RX, y, item[1], item[2]))
        elif t == "section": right.append(section_line(RX, y, item[1]))
        elif t == "stats1":  right.append(stats1_line(RX, y))
        elif t == "stats2":  right.append(stats2_line(RX, y))
    right_svg = "\n".join(right)

    ascii_tspans = "\n".join(
        f'<tspan x="15" y="{ascii_y0 + i*ASCII_DY}">{esc(r)}</tspan>'
        for i, r in enumerate(art)
    )

    height = max(info_bottom, ascii_y0 + ascii_h) + 24
    width = RX + T * (INFO_FS * 0.60) + 40 * (INFO_FS * 0.60)  # rough; refined below
    # width driven by longest info line: value begins at char T, longest value ~ 37
    longest = 0
    for item in INFO:
        if item[0] == "kv":
            longest = max(longest, T + len(item[2]) + 2)
    longest = max(longest, T + 24)  # stats lines
    width = int(RX + longest * (INFO_FS * 0.60) + 24)

    c = THEMES[theme]
    return f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="Consolas,'Courier New',monospace" width="{width}px" height="{height}px" font-size="{INFO_FS}px">
<style>
.key {{fill: {c['key']};}}
.value {{fill: {c['value']};}}
.host {{fill: {c['host']}; font-weight: bold;}}
.host2 {{fill: {c['host2']}; font-weight: bold;}}
.hd {{fill: {c['hd']}; font-weight: bold;}}
.cc {{fill: {c['cc']};}}
.ascii {{fill: {c['ascii']};}}
text, tspan {{white-space: pre;}}
</style>
<rect x="0.5" y="0.5" width="{width-1}px" height="{height-1}px" fill="{c['bg']}" stroke="{c['stroke']}" rx="15"/>
<text class="ascii" font-size="{ASCII_FS}px" fill="{c['ascii']}">
{ascii_tspans}
</text>
<text fill="{c['text']}">
{right_svg}
</text>
</svg>
'''

def main():
    art = load_ascii()
    for theme in ("dark", "light"):
        out = os.path.join(HERE, f"{theme}_mode.svg")
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(art, theme))
        print("wrote", out, "| ascii", len(art), "rows x", max(len(r) for r in art), "cols")

if __name__ == "__main__":
    main()
