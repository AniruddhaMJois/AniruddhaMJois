import urllib.request
import time
import sys
import os
import json

import re

URL_STREAK = "https://streak-stats.demolab.com/?user=AniruddhaMJois&theme=tokyonight&hide_border=true&border_radius=15&hide_longest_streak=true&timezone=Asia%2FKolkata"
URL_COMMITS = "https://github-readme-stats-eight-theta.vercel.app/api?username=AniruddhaMJois&include_all_commits=true"
OUTPUT_FILE = "streak.svg"

def get_total_commits():
    token = os.environ.get("GH_TOKEN")
    if token:
        try:
            # Get contribution years
            query_years = """
            query {
              user(login: "AniruddhaMJois") {
                contributionsCollection {
                  contributionYears
                }
              }
            }
            """
            req = urllib.request.Request("https://api.github.com/graphql", 
                                         data=json.dumps({"query": query_years}).encode("utf-8"),
                                         headers={"Authorization": f"Bearer {token}"})
            res = urllib.request.urlopen(req)
            years = json.loads(res.read())["data"]["user"]["contributionsCollection"]["contributionYears"]

            total = 0
            for year in years:
                query_commits = f"""
                query {{
                  user(login: "AniruddhaMJois") {{
                    contributionsCollection(from: "{year}-01-01T00:00:00Z", to: "{year}-12-31T23:59:59Z") {{
                      totalCommitContributions
                      restrictedContributionsCount
                    }}
                  }}
                }}
                """
                req = urllib.request.Request("https://api.github.com/graphql", 
                                             data=json.dumps({"query": query_commits}).encode("utf-8"),
                                             headers={"Authorization": f"Bearer {token}"})
                res = urllib.request.urlopen(req)
                data = json.loads(res.read())["data"]["user"]["contributionsCollection"]
                total += data["totalCommitContributions"]
                total += data["restrictedContributionsCount"]
            
            # Format with commas for better readability (e.g., 1,024 instead of 1024)
            return f"{total:,}"
        except Exception as e:
            print(f"GraphQL API failed: {e}. Falling back to Vercel API.")

    try:
        req = urllib.request.Request(URL_COMMITS, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'data-testid="commits"[^>]*>([^<]+)<', res)
        if match:
            return match.group(1).strip()
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
