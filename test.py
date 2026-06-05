import urllib.request, re
svg = urllib.request.urlopen('https://github-readme-stats-eight-theta.vercel.app/api?username=AniruddhaMJois&include_all_commits=true').read().decode('utf-8')
match = re.search(r'data-testid="commits"[^>]*>([0-9,]+)<', svg)
if match:
    print(match.group(1))
else:
    print("Not found")
