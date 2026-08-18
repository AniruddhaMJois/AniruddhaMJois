import urllib.request
import time
import sys
import re

URL_STREAK = "https://streak-stats.demolab.com/?user=AniruddhaMJois&theme=tokyonight&hide_border=true&border_radius=15&timezone=Asia%2FKolkata"
URL_COMMITS = "https://github-readme-stats-eight-theta.vercel.app/api?username=AniruddhaMJois&include_all_commits=true"
OUTPUT_FILE = "streak.svg"

def get_total_commits():
    try:
        req = urllib.request.Request(URL_COMMITS, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'data-testid="commits"[^>]*>([0-9,kK\+]+)<', res)
        if match:
            return match.group(1)
    except:
        pass
    return "1.3k+" # fallback

total_commits = get_total_commits()

for i in range(5):
    try:
        req = urllib.request.Request(URL_STREAK, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            svg_data = response.read().decode('utf-8')
            if "Failed to retrieve" not in svg_data:
                
                # Extract original Total Contributions number
                contrib_match = re.search(r'(<!-- Total Contributions big number -->.*?<text[^>]*>)\s*([\d,]+)\s*(</text>)', svg_data, re.DOTALL)
                total_contribs = contrib_match.group(2) if contrib_match else "0"

                # Rename the first column (Total Contributions -> Total Commits)
                svg_data = svg_data.replace("Total Contributions", "Total Commits", 4)
                
                # Modify Column 1 (Total Commits)
                svg_data = re.sub(
                    r'(<!-- Total Commits big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
                    r'\g<1>' + str(total_commits) + r'\g<2>',
                    svg_data, flags=re.DOTALL
                )
                svg_data = re.sub(
                    r'(<!-- Total Commits range -->.*?<text[^>]*>)[^<]+(</text>)',
                    r'\g<1>All Time\g<2>',
                    svg_data, flags=re.DOTALL
                )

                # Rename the third column (Longest Streak -> Total Contributions)
                svg_data = svg_data.replace("Longest Streak", "Total Contributions", 4)
                
                # Modify Column 3
                svg_data = re.sub(
                    r'(<!-- Total Contributions big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
                    r'\g<1>' + total_contribs + r'\g<2>',
                    svg_data, flags=re.DOTALL
                )
                svg_data = re.sub(
                    r'(<!-- Total Contributions range -->.*?<text[^>]*>)[^<]+(</text>)',
                    r'\g<1>Last 1 Year\g<2>',
                    svg_data, flags=re.DOTALL
                )

                # Modify Column 2 (Current Streak to "5" and "Aug 14 - Present")
                svg_data = re.sub(
                    r'(<!-- Current Streak big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
                    r'\g<1>5\g<2>',
                    svg_data, flags=re.DOTALL
                )
                svg_data = re.sub(
                    r'(<!-- Current Streak range -->.*?<text[^>]*>)[^<]+(</text>)',
                    r'\g<1>Aug 14 - Present\g<2>',
                    svg_data, flags=re.DOTALL
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
