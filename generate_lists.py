#!/usr/bin/env python3
"""
Reads all_proxies.txt (lines like: tg://proxy?server=...&port=...&secret=...)
and generates:
  - all_proxies.md   (clickable https://t.me/proxy?... links, for Markdown viewers)
  - all_proxies.html (clickable tg://proxy?... buttons, for browsers where t.me is blocked)
  - index.html       (identical copy of all_proxies.html, so it shows up at the
                       root of the GitHub Pages site automatically)
"""
import pathlib
from datetime import datetime, timezone

SRC = "all_proxies.txt"
MD_OUT = "all_proxies.md"
HTML_OUT = "all_proxies.html"
INDEX_OUT = "index.html"


def tg_to_tme(line: str) -> str:
    """Convert a tg://proxy?... link into an https://t.me/proxy?... link."""
    return line.replace("tg://proxy?", "https://t.me/proxy?", 1)


def main() -> None:
    src_path = pathlib.Path(SRC)
    if not src_path.exists():
        raise SystemExit(f"{SRC} not found — run the download step first.")

    lines = [l.strip() for l in src_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ---------- Markdown ----------
    md_lines = [
        "# 🌐 MTProto Proxy List",
        "",
        f"Auto-updated: **{timestamp}**  ",
        f"Total proxies: **{len(lines)}**",
        "",
        "Click any link below to open it in Telegram:",
        "",
    ]
    for i, line in enumerate(lines, 1):
        md_lines.append(f"{i}. [Connect proxy #{i}]({tg_to_tme(line)})")
    pathlib.Path(MD_OUT).write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    # ---------- HTML ----------
    rows = []
    for i, line in enumerate(lines, 1):
        tme_link = tg_to_tme(line)
        rows.append(
            "<tr>"
            f"<td>{i}</td>"
            f'<td><a class="open" href="{line}">Open</a></td>'
            f'<td><a class="open alt" href="{tme_link}">t.me link</a></td>'
            f'<td><button class="copy" data-link="{line}">Copy</button></td>'
            "</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MTProto Proxy List</title>
<style>
  body {{ font-family: system-ui, sans-serif; background:#0f1115; color:#eee; padding:24px; max-width:720px; margin:auto; }}
  h1 {{ font-size:1.4rem; }}
  .meta {{ color:#9aa0a6; margin-bottom:20px; }}
  table {{ width:100%; border-collapse: collapse; }}
  td, th {{ padding:10px 8px; border-bottom:1px solid #2a2d34; text-align:left; }}
  a.open {{ color:#4ea1ff; text-decoration:none; font-weight:600; }}
  a.alt {{ color:#8ab4f8; font-weight:400; }}
  button.copy {{ background:#1f2329; color:#eee; border:1px solid #3a3f47; border-radius:6px; padding:4px 10px; cursor:pointer; }}
  button.copy:hover {{ background:#2a2f36; }}
</style>
</head>
<body>
  <h1>🌐 MTProto Proxy List</h1>
  <p class="meta">Auto-updated: {timestamp} &middot; Total proxies: {len(lines)}</p>
  <table>
    <tr><th>#</th><th>tg:// link</th><th>t.me link</th><th>Copy</th></tr>
    {''.join(rows)}
  </table>
  <script>
    document.querySelectorAll('.copy').forEach(btn => {{
      btn.addEventListener('click', () => {{
        navigator.clipboard.writeText(btn.dataset.link);
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy', 1200);
      }});
    }});
  </script>
</body>
</html>
"""
    pathlib.Path(HTML_OUT).write_text(html, encoding="utf-8")
    pathlib.Path(INDEX_OUT).write_text(html, encoding="utf-8")

    print(f"Generated {MD_OUT}, {HTML_OUT} and {INDEX_OUT} with {len(lines)} proxies.")


if __name__ == "__main__":
    main()
