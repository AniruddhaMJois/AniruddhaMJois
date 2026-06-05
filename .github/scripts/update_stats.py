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
      <g transform="translate(247.5, 70)">

        
        <!-- Animated Number -->
        <text x="0" y="-15" alignment-baseline="central" dominant-baseline="central" text-anchor="middle" style="font: 800 64px 'Inter', Ubuntu, Sans-Serif; fill: #70a5fd; opacity: 0;">
          {total_commits}
          <animate attributeName="opacity" values="0;1" dur="1s" begin="0.3s" fill="freeze" />
          <animateTransform attributeName="transform" type="translate" values="0,15; 0,0" dur="1s" begin="0.3s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.2 1"/>
        </text>
        
        <!-- Animated Divider Line -->
        <rect x="-40" y="25" width="80" height="2" fill="#38bdae" opacity="0" rx="1">
          <animate attributeName="opacity" values="0;1" dur="0.8s" begin="0.7s" fill="freeze" />
          <animate attributeName="width" values="0;80" dur="0.8s" begin="0.7s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.2 1" />
          <animate attributeName="x" values="0;-40" dur="0.8s" begin="0.7s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.2 1" />
        </rect>
        
        <!-- Label -->
        <text x="0" y="45" alignment-baseline="central" dominant-baseline="central" text-anchor="middle" style="font: 600 13px 'Inter', Ubuntu, Sans-Serif; fill: #a9b1d6; letter-spacing: 3px; opacity: 0;">
          TOTAL COMMITS
          <animate attributeName="opacity" values="0;1" dur="1s" begin="0.9s" fill="freeze" />
          <animateTransform attributeName="transform" type="translate" values="0,10; 0,0" dur="1s" begin="0.9s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.2 1"/>
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
