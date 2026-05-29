import urllib.request
import re
import sys

URL = "https://github-readme-stats-eight-theta.vercel.app/api?username=AniruddhaMJois&show_icons=true&theme=tokyonight&hide_border=true&border_radius=15&include_all_commits=true"
OUTPUT_FILE = "github-stats.svg"

def main():
    print("Fetching SVG from", URL)
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            svg = response.read().decode('utf-8')
    except Exception as e:
        print("Error fetching URL:", e)
        sys.exit(1)
    
    commits_match = re.search(r'data-testid="commits"\s*>(\d+)</text>', svg)
    if not commits_match:
        print("Could not find total commits in SVG!")
        sys.exit(1)
    
    total_commits = commits_match.group(1)
    print("Found total commits:", total_commits)
    
    # Split the SVG exactly at the start of the stats block
    split_marker = '<svg x="0" y="0">'
    if split_marker not in svg:
        print("Could not find split marker!")
        sys.exit(1)
        
    parts = svg.split(split_marker)
    top_part = parts[0]
    
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
    </svg>
        </g>
      </svg>
'''
    
    final_svg = top_part + creative_commits_svg
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_svg)
    
    print(f"Saved modified SVG to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
