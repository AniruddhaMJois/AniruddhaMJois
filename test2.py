import re

with open('streak.svg', 'r', encoding='utf-8') as f:
    svg = f.read()

svg = svg.replace('Total Contributions', 'Total Commits')

svg = re.sub(
    r'(<!-- Total Commits big number -->\s*<g[^>]*>\s*<text[^>]*>)\s*[\d,]+\s*(</text>\s*</g>)',
    r'\g<1>' + '842' + r'\g<2>',
    svg
)

print('Total Commits' in svg)
print('842' in svg)
print('297' in svg) # should be false if 297 was replaced and nowhere else

with open('streak_test.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
