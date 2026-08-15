import urllib.request
import urllib.error
import time
import sys
import os
import json
import re

URL_STREAK = "https://streak-stats.demolab.com/?user=AniruddhaMJois&theme=tokyonight&hide_border=true&border_radius=15&hide_longest_streak=true&timezone=Asia%2FKolkata"
OUTPUT_FILE = "streak.svg"
USER = "AniruddhaMJois"

def api_request(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    gh_token = os.environ.get('GH_TOKEN')
    if gh_token:
        headers['Authorization'] = f"Bearer {gh_token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        time.sleep(0.1) # Avoid rate limits
        with urllib.request.urlopen(req) as response:
            return response.read(), response.info()
    except Exception as e:
        print(f"Error for {url}: {e}")
        return None, None

def get_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}"
        data, _ = api_request(url)
        if not data: break
        batch = json.loads(data)
        if not batch: break
        repos.extend(batch)
        page += 1
    return repos

def get_branches(repo_name):
    branches = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{USER}/{repo_name}/branches?per_page=100&page={page}"
        data, _ = api_request(url)
        if not data: break
        batch = json.loads(data)
        if not batch: break
        branches.extend(batch)
        page += 1
    return branches

def get_commit_count(repo_name, branch_name):
    url = f"https://api.github.com/repos/{USER}/{repo_name}/commits?sha={branch_name}&per_page=1"
    data, headers = api_request(url)
    if not headers: return 0
    link_header = headers.get('Link')
    if link_header:
        match = re.search(r'&page=(\d+)>; rel="last"', link_header)
        if match:
            return int(match.group(1))
    if data:
        commits = json.loads(data)
        return len(commits)
    return 0

def get_total_commits():
    try:
        repos = get_repos()
        if not repos:
            return None
        
        total_commits = 0
        for repo in repos:
            repo_name = repo['name']
            branches = get_branches(repo_name)
            if not branches:
                continue
            for branch in branches:
                branch_name = branch['name']
                total_commits += get_commit_count(repo_name, branch_name)
        
        if total_commits > 0:
            return f"{total_commits:,}"
    except Exception as e:
        print(f"Stats API failed: {e}")
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
                        r'(<!-- Total Commits big number -->\s*<g[^>]*>\s*<text[^>]*>)\s*[\d,\+]+\s*(</text>\s*</g>)',
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

print("Failed to fetch streak SVG after 5 attempts, but exiting with 0 to prevent GitHub Action failure email spam.")
sys.exit(0)
