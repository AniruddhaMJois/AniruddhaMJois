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
    
    # 2. Replace the entire stats list with our custom creative commits design
    # The stats are contained inside <svg x="0" y="0"> ... </svg> right before the end of main-card-body
    
    creative_commits_svg = f'''<svg x="0" y="0">
      <g transform="translate(180, 50)">
        <!-- Animated Background Glow -->
        <circle cx="0" cy="0" r="50" fill="#bf91f3" opacity="0.15">
          <animate attributeName="r" values="50;65;50" dur="3s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.15;0.3;0.15" dur="3s" repeatCount="indefinite" />
        </circle>
        
        <!-- Big Number -->
        <text x="0" y="-10" alignment-baseline="central" dominant-baseline="central" text-anchor="middle" style="font: 800 52px 'Inter', Ubuntu, Sans-Serif; fill: #70a5fd; text-shadow: 0px 4px 10px rgba(112, 165, 253, 0.4);">
          {total_commits}
        </text>
        
        <!-- Label -->
        <text x="0" y="35" alignment-baseline="central" dominant-baseline="central" text-anchor="middle" style="font: 600 14px 'Inter', Ubuntu, Sans-Serif; fill: #38bdae; letter-spacing: 2px;">
          TOTAL COMMITS
        </text>
      </g>
    </svg>'''
    
    # Replace the <svg x="0" y="0"> block
    # We use regex to find <svg x="0" y="0"> and the matching closing </svg>
    svg = re.sub(r'<svg x="0" y="0">.*?</svg>', creative_commits_svg, svg, flags=re.DOTALL)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg)
    
    print(f"Saved modified SVG to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
