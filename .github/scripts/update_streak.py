import urllib.request
import time
import sys

URL = "https://streak-stats.demolab.com/?user=AniruddhaMJois&theme=tokyonight&hide_border=true&border_radius=15&hide_longest_streak=true"
OUTPUT_FILE = "streak.svg"

for i in range(5):
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            svg_data = response.read().decode('utf-8')
            if "Failed to retrieve" not in svg_data:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write(svg_data)
                print("Successfully fetched streak SVG.")
                sys.exit(0)
            else:
                print(f"Attempt {i+1} failed: GitHub API rate limited.")
    except Exception as e:
        print(f"Attempt {i+1} failed: {e}")
    time.sleep(10)

print("Failed to fetch streak SVG after 5 attempts.")
sys.exit(1)
