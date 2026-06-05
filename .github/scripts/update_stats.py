import urllib.request
import re
import sys

URL = "https://github-readme-stats-eight-theta.vercel.app/api?username=AniruddhaMJois&show_icons=true&theme=tokyonight&hide_border=true&border_radius=15&include_all_commits=true&hide_rank=true"
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
        <!-- Professional Subtle Ring Animation -->
        <circle cx="0" cy="0" r="46" fill="none" stroke="#70a5fd" stroke-width="2" stroke-dasharray="289" stroke-dashoffset="289">
          <animate attributeName="stroke-dashoffset" values="289;0" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" />
        </circle>
        
        <!-- Animated Number -->
        <text x="0" y="-10" alignment-baseline="central" dominant-baseline="central" text-anchor="middle" style="font: 800 48px 'Inter', Ubuntu, Sans-Serif; fill: #70a5fd; opacity: 0;">
          {total_commits}
          <animate attributeName="opacity" values="0;1" dur="1s" begin="0.5s" fill="freeze" />
          <animateTransform attributeName="transform" type="translate" values="0,10; 0,0" dur="1s" begin="0.5s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.2 1"/>
        </text>
        
        <!-- Label -->
        <text x="0" y="32" alignment-baseline="central" dominant-baseline="central" text-anchor="middle" style="font: 600 13px 'Inter', Ubuntu, Sans-Serif; fill: #a9b1d6; letter-spacing: 2px; opacity: 0;">
          TOTAL COMMITS
          <animate attributeName="opacity" values="0;1" dur="1s" begin="0.8s" fill="freeze" />
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
