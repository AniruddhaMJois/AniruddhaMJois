import urllib.request
import re

URL = "https://github-readme-stats-eight-theta.vercel.app/api?username=AniruddhaMJois&show_icons=true&theme=tokyonight&hide_border=true&border_radius=15&include_all_commits=true"
OUTPUT_FILE = "github-stats.svg"

def main():
    print("Fetching SVG from", URL)
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        svg = response.read().decode('utf-8')
    
    # 1. Extract total commits
    commits_match = re.search(r'data-testid="commits"\s*>(\d+)</text>', svg)
    if not commits_match:
        print("Could not find total commits in SVG!")
        return
    
    total_commits = commits_match.group(1)
    print("Found total commits:", total_commits)
    
    # 2. Move rank circle to the right
    # Original is transform="translate(400, 47.5)" or similar
    svg = re.sub(r'(data-testid="rank-circle"\s*transform="translate\()400', r'\g<1>430', svg)
    
    # 3. Add Commits under A+ text and adjust A+ text position
    # The A+ text looks like:
    # <text x="0" y="0" alignment-baseline="central" dominant-baseline="central" text-anchor="middle">
    #   A+
    # </text>
    
    rank_text_pattern = re.compile(
        r'(<g class="rank-text">\s*<text\s*x="0"\s*y=")0("\s*alignment-baseline="central"\s*dominant-baseline="central"\s*text-anchor="middle"\s*>\s*A\+\s*</text>)',
        re.MULTILINE
    )
    
    replacement = r'''\g<1>-8\g<2>
          <text
            x="0"
            y="18"
            style="font: 700 12px 'Inter', Ubuntu, Sans-Serif; fill: #38bdae;"
            alignment-baseline="central"
            dominant-baseline="central"
            text-anchor="middle"
          >
            ''' + total_commits + ''' Commits
          </text>'''
    
    new_svg = rank_text_pattern.sub(replacement, svg)
    
    if new_svg == svg:
        print("Warning: Rank text replacement failed! Trying alternative pattern...")
        # fallback if A+ isn't exact or formatted differently
        fallback_pattern = re.compile(
            r'(<g class="rank-text">\s*<text\s*x="0"\s*y=")0("\s*[^>]*>\s*[^<]+\s*</text>)',
            re.MULTILINE | re.DOTALL
        )
        new_svg = fallback_pattern.sub(replacement, svg)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_svg)
    
    print(f"Saved modified SVG to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
