import re, pathlib, html, os
p = pathlib.Path('WordPress.2026-04-01.xml')
text = p.read_text(encoding='utf-8')
items = re.findall(r'<item>(.*?)</item>', text, flags=re.S)
created = []
os.makedirs('generated', exist_ok=True)
for i, item in enumerate(items, 1):
    post_type_m = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
    if not post_type_m:
        continue
    typ = post_type_m.group(1)
    if typ not in ('page', 'post'):
        continue
    title_m = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
    slug_m = re.search(r'<wp:post_name><!\[CDATA\[(.*?)\]\]></wp:post_name>', item)
    content_m = re.search(r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>', item, flags=re.S)
    if not content_m:
        continue
    title = title_m.group(1) if title_m else f'item-{i}'
    slug = slug_m.group(1) if slug_m else title.replace(' ', '-')
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', slug).strip('-')
    if not slug:
        slug = f'item-{i}'
    content_html = content_m.group(1).strip() or '<p>(no content)</p>'
    outname = f'generated/{slug}-{i}.html'
    html_out = f'''<!doctype html>
<html lang="zh-TW">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="stylesheet" href="WordPress.2026-04-01.css"></head>
<body>
{content_html}
<script src="WordPress.2026-04-01.js"></script>
</body>
</html>'''
    pathlib.Path(outname).write_text(html_out, encoding='utf-8')
    created.append(outname)
print('created', created)
