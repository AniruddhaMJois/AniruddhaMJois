import urllib.request
import time
import sys

import re

URL_STREAK = "https://streak-stats.demolab.com/?user=AniruddhaMJois&theme=tokyonight&hide_border=true&border_radius=15&hide_longest_streak=true"
URL_COMMITS = "https://github-readme-stats-eight-theta.vercel.app/api?username=AniruddhaMJois&include_all_commits=true"
OUTPUT_FILE = "streak.svg"

def get_total_commits():
    try:
        req = urllib.request.Request(URL_COMMITS, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'data-testid="commits"[^>]*>([0-9,]+)<', res)
        if match:
            return match.group(1)
    except:
        pass
    return None

total_commits = get_total_commits()

for i in range(5):
    try:
        req = urllib.request.Request(URL_STREAK, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            svg_data = response.read().decode('utf-8')
            if "Failed to retrieve" not in svg_data:
                if total_commits:
                    svg_data = svg_data.replace("Total Contributions", "Total Commits")
                    svg_data = re.sub(
                        r'(<!-- Total Commits big number -->\s*<g[^>]*>\s*<text[^>]*>)\s*[\d,]+\s*(</text>\s*</g>)',
                        r'\g<1>' + total_commits + r'\g<2>',
                        svg_data
                    )
                    svg_data = re.sub(
                        r'(<!-- Total Commits range -->\s*<g[^>]*>\s*<text[^>]*>)[^<]+(</text>\s*</g>)',
                        r'\g<1>' + 'All Time' + r'\g<2>',
                        svg_data
                    )
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write(svg_data)
                print("Successfully fetched and processed streak SVG.")
                sys.exit(0)
            else:
                print(f"Attempt {i+1} failed: GitHub API rate limited.")
    except Exception as e:
        print(f"Attempt {i+1} failed: {e}")
    time.sleep(10)

print("Failed to fetch streak SVG after 5 attempts.")
sys.exit(1)
