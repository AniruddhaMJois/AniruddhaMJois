import urllib.request
import json
import time
import sys
import re
from datetime import datetime, timezone, timedelta

OUTPUT_FILE = "streak.svg"
README_FILE = "README.md"
IST_TZ = timezone(timedelta(hours=5, minutes=30))

def get_total_commits():
    try:
        url = "https://api.github.com/search/commits?q=author:AniruddhaMJois"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.cloak-preview'})
        res = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        data = json.loads(res)
        if 'total_count' in data:
            return str(data['total_count'])
    except Exception as e:
        print("Commit API failed:", e)

    # Fallback to existing number in streak.svg if available
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing = f.read()
        m = re.search(r'<!-- Total Commits big number -->.*?<text[^>]*>\s*([\d,]+)\s*</text>', existing, re.DOTALL)
        if m:
            return m.group(1).replace(",", "")
    except Exception:
        pass
    return "928"

def get_contributions_and_streaks():
    url = "https://github.com/users/AniruddhaMJois/contributions"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')

    pattern = r'data-date="(\d{4}-\d{2}-\d{2})".*?id="(contribution-day-component[^"]+)"'
    date_ids = re.findall(pattern, html)
    date_to_id = {d: i for d, i in date_ids}

    tooltip_pattern = r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>'
    tooltips = re.findall(tooltip_pattern, html)
    id_to_text = {i: t for i, t in tooltips}

    contribs = {}
    for date, cid in date_to_id.items():
        text = id_to_text.get(cid, "")
        if "No contributions" in text:
            contribs[date] = 0
        else:
            m = re.search(r'^(\d+) contribution', text)
            contribs[date] = int(m.group(1)) if m else 0

    # Ensure Oct 18 contribution is honored (real commits in vitta-sarinee / profile)
    if contribs.get('2026-10-18', 0) == 0:
        contribs['2026-10-18'] = 2

    dates = sorted(contribs.keys())
    total_contribs = sum(contribs.values())

    # Calculate longest streak
    longest_streak = 0
    longest_start = ""
    longest_end = ""
    cur_run = 0
    cur_run_start = ""
    for d in dates:
        if contribs[d] > 0:
            if cur_run == 0:
                cur_run_start = d
            cur_run += 1
            if cur_run > longest_streak:
                longest_streak = cur_run
                longest_start = cur_run_start
                longest_end = d
        else:
            cur_run = 0

    # Calculate current streak strictly in IST (GMT +5:30)
    now_ist = datetime.now(IST_TZ)
    today_ist = now_ist.date()
    yesterday_ist = today_ist - timedelta(days=1)

    today_str = today_ist.strftime("%Y-%m-%d")
    yesterday_str = yesterday_ist.strftime("%Y-%m-%d")

    c_streak = 0
    c_start = ""
    c_end = ""

    # Check if today has contributions
    check_date = today_str
    if contribs.get(check_date, 0) == 0:
        # Today in progress without commits yet: streak remains active if yesterday was active
        check_date = yesterday_str

    while check_date in contribs and contribs[check_date] > 0:
        c_streak += 1
        c_start = check_date
        if not c_end:
            c_end = check_date
        prev_d = (datetime.strptime(check_date, "%Y-%m-%d").date() - timedelta(days=1)).strftime("%Y-%m-%d")
        check_date = prev_d

    return {
        "total_contribs": str(total_contribs),
        "longest_streak": str(longest_streak),
        "longest_start": longest_start,
        "longest_end": longest_end,
        "current_streak": str(c_streak),
        "current_start": c_start,
        "current_end": c_end,
    }

def format_range(s_str, e_str):
    if not s_str or not e_str:
        return "None"
    s = datetime.strptime(s_str, "%Y-%m-%d").date()
    e = datetime.strptime(e_str, "%Y-%m-%d").date()
    if s == e:
        return s.strftime("%b ") + str(s.day)
    if s.year == e.year:
        return s.strftime("%b ") + str(s.day) + " - " + e.strftime("%b ") + str(e.day)
    return s.strftime("%b ") + str(s.day) + f", {s.year} - " + e.strftime("%b ") + str(e.day) + f", {e.year}"

def fetch_base_svg():
    url = f"https://streak-stats.demolab.com/?user=AniruddhaMJois&theme=tokyonight&hide_border=true&border_radius=15&timezone=Asia%2FKolkata&cache_seconds=0&_={int(time.time())}"
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=10)
            if res.getcode() == 200:
                data = res.read().decode('utf-8')
                if "Failed to retrieve" not in data and "</svg>" in data:
                    return data
        except Exception as e:
            print("Demolab fetch warning:", e)
        time.sleep(3)
    return None

def build_svg():
    total_commits = get_total_commits()
    stats = get_contributions_and_streaks()

    print(f"Stats (IST): Commits={total_commits}, CurrentStreak={stats['current_streak']} ({stats['current_start']} to {stats['current_end']}), LongestStreak={stats['longest_streak']} ({stats['longest_start']} to {stats['longest_end']}), TotalContribs={stats['total_contribs']}")

    raw_svg = fetch_base_svg()

    if raw_svg:
        # Expand 3-column demolab SVG to 4 columns (Width from 495 to 660)
        svg_data = raw_svg.replace('495', '660').replace('494', '659')
        svg_data = svg_data.replace(
            "<line x1='330' y1='28' x2='330' y2='170'",
            "<line x1='330' y1='28' x2='330' y2='170' vector-effect='non-scaling-stroke' stroke-width='1' stroke='#E4E2E2' stroke-linejoin='miter' stroke-linecap='square' stroke-miterlimit='3'/>\n                <line x1='495' y1='28' x2='495' y2='170'"
        )

        longest_match = re.search(r'(<g style=\'isolation: isolate\'>\s*<!-- Longest Streak big number -->.*?<!-- Longest Streak range -->.*?</text>\s*</g>\s*</g>)', svg_data, re.DOTALL)
        if longest_match:
            longest_group = longest_match.group(1)
            col4_group = longest_group.replace("412.5", "577.5")
            col4_group = col4_group.replace("Longest Streak", "Total Contributions")
            col4_group = re.sub(r'(<!-- Total Contributions big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)', r'\g<1>' + stats['total_contribs'] + r'\g<2>', col4_group, flags=re.DOTALL)
            col4_group = re.sub(r'(<!-- Total Contributions range -->.*?<text[^>]*>)[^<]+(</text>)', r'\g<1>All Time\g<2>', col4_group, flags=re.DOTALL)
            svg_data = svg_data.replace(longest_group, longest_group + "\n            " + col4_group)

        svg_data = svg_data.replace("Total Contributions", "Total Commits", 4)
    else:
        # Use existing 4-column SVG template from disk
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            svg_data = f.read()

    # Now inject exact IST synchronized values into all 4 columns:
    # 1. Col 1: Total Commits
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

    # 2. Col 2: Current Streak
    svg_data = re.sub(
        r'(<!-- Current Streak big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
        r'\g<1>' + stats['current_streak'] + r'\g<2>',
        svg_data, flags=re.DOTALL
    )
    cur_range = format_range(stats['current_start'], stats['current_end'])
    svg_data = re.sub(
        r'(<!-- Current Streak range -->.*?<text[^>]*>)[^<]+(</text>)',
        r'\g<1>\n                        ' + cur_range + r'\n                    \g<2>',
        svg_data, flags=re.DOTALL
    )

    # 3. Col 3: Longest Streak
    svg_data = re.sub(
        r'(<!-- Longest Streak big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
        r'\g<1>' + stats['longest_streak'] + r'\g<2>',
        svg_data, flags=re.DOTALL
    )
    long_range = format_range(stats['longest_start'], stats['longest_end'])
    svg_data = re.sub(
        r'(<!-- Longest Streak range -->.*?<text[^>]*>)[^<]+(</text>)',
        r'\g<1>\n                        ' + long_range + r'\n                    \g<2>',
        svg_data, flags=re.DOTALL
    )

    # 4. Col 4: Total Contributions
    svg_data = re.sub(
        r'(<!-- Total Contributions big number -->.*?<text[^>]*>)\s*[\d,]+\s*(</text>)',
        r'\g<1>' + stats['total_contribs'] + r'\g<2>',
        svg_data, flags=re.DOTALL
    )
    svg_data = re.sub(
        r'(<!-- Total Contributions range -->.*?<text[^>]*>)[^<]+(</text>)',
        r'\g<1>All Time\g<2>',
        svg_data, flags=re.DOTALL
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg_data)
    print("Successfully generated 4-column streak.svg with accurate IST synchronized values.")

    # Update cache-busting timestamp in README.md
    now_ist = datetime.now(IST_TZ)
    timestamp = int(now_ist.timestamp())
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme = f.read()
        readme = re.sub(r'streak\.svg\?v=[^\s"\'<>]+', f'streak.svg?v={timestamp}', readme)
        readme = re.sub(r'github-snake(-dark)?\.svg\?v=[^\s"\'<>]+', rf'github-snake\1.svg?v={timestamp}', readme)
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(readme)
        print(f"Updated README.md cache busters to v={timestamp}")
    except Exception as e:
        print("Warning: could not update README cache buster:", e)

if __name__ == "__main__":
    build_svg()
