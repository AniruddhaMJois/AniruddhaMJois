import urllib.request
import time
import sys
import re
from datetime import datetime

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
    return "1.3k+"

total_commits = get_total_commits()

# Calculate dynamic streak from Aug 14, 2026
start_date = datetime(2026, 8, 14).date()
today = datetime.now().date()
dynamic_streak = (today - start_date).days + 1
if dynamic_streak < 1:
    dynamic_streak = 1

for i in range(5):
    try:
        req = urllib.request.Request(URL_STREAK, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            svg_data = response.read().decode('utf-8')
            if "Failed to retrieve" not in svg_data:
                
                # Expand SVG to 4 columns (Width from 495 to 660)
                svg_data = svg_data.replace('495', '660')
                svg_data = svg_data.replace('494', '659')
                
                svg_data = svg_data.replace(
                    "<line x1='330' y1='28' x2='330' y2='170'",
                    "<line x1='330' y1='28' x2='330' y2='170' vector-effect='non-scaling-stroke' stroke-width='1' stroke='#E4E2E2' stroke-linejoin='miter' stroke-linecap='square' stroke-miterlimit='3'/>\n                <line x1='495' y1='28' x2='495' y2='170'"
                )

                # Fetch original Total Contributions
                contrib_match = re.search(r'<!-- Total Contributions big number -->.*?<text[^>]*>\s*([\d,]+)\s*</text>', svg_data, re.DOTALL)
                total_contribs = contrib_match.group(1) if contrib_match else "0"

                longest_match = re.search(r'(<g style=\'isolation: isolate\'>\s*<!-- Longest Streak big number -->.*?<!-- Longest Streak range -->.*?</g>\s*</g>\s*</g>)', svg_data, re.DOTALL)
                
                if longest_match:
                    longest_group = longest_match.group(1)
                    
                    # Create Col 4 (Total Contributions)
                    col4_group = longest_group.replace("412.5", "577.5")
                    col4_group = col4_group.replace("Longest Streak", "Total Contributions")
                    
                    col4_group = re.sub(r'(<!-- Total Contributions big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)', r'\g<1>' + total_contribs + r'\g<2>', col4_group, flags=re.DOTALL)
                    col4_group = re.sub(r'(<!-- Total Contributions range -->.*?<text[^>]*>)[^<]+(</text>)', r'\g<1>All Time\g<2>', col4_group, flags=re.DOTALL)

                    # Inject col4_group
                    svg_data = svg_data.replace(longest_group, longest_group + "\n            " + col4_group)

                # Modify Col 1 (Total Commits)
                svg_data = svg_data.replace("Total Contributions", "Total Commits", 4)
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

                # Modify Col 2 (Current Streak to dynamic_streak and Aug 14)
                svg_data = re.sub(
                    r'(<!-- Current Streak big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
                    r'\g<1>' + str(dynamic_streak) + r'\g<2>',
                    svg_data, flags=re.DOTALL
                )
                svg_data = re.sub(
                    r'(<!-- Current Streak range -->.*?<text[^>]*>)[^<]+(</text>)',
                    r'\g<1>Aug 14 - Present\g<2>',
                    svg_data, flags=re.DOTALL
                )

                # Also update Longest Streak if dynamic streak > longest streak!
                longest_num_match = re.search(r'<!-- Longest Streak big number -->.*?<text[^>]*>\s*([\d,]+)\s*</text>', svg_data, re.DOTALL)
                if longest_num_match:
                    longest_num = int(longest_num_match.group(1))
                    if dynamic_streak > longest_num:
                        svg_data = re.sub(
                            r'(<!-- Longest Streak big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
                            r'\g<1>' + str(dynamic_streak) + r'\g<2>',
                            svg_data, flags=re.DOTALL
                        )
                        svg_data = re.sub(
                            r'(<!-- Longest Streak range -->.*?<text[^>]*>)[^<]+(</text>)',
                            r'\g<1>Aug 14 - Present\g<2>',
                            svg_data, flags=re.DOTALL
                        )

                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write(svg_data)
                print("Successfully generated 4-column SVG.")
                sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(10)

print("Failed to fetch streak SVG after 5 attempts.")
sys.exit(1)
