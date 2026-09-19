import urllib.request
import re
from datetime import datetime, timedelta

url = "https://github.com/users/AniruddhaMJois/contributions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

pattern = r'data-date="(\d{4}-\d{2}-\d{2})".*?id="(contribution-day-component[^"]+)"'
date_ids = re.findall(pattern, html)
date_to_id = {d: i for d, i in date_ids}

tooltip_pattern = r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>'
tooltips = re.findall(tooltip_pattern, html)
id_to_text = {i: t for i, t in tooltips}

contribs = {}
for date, id in date_to_id.items():
    text = id_to_text.get(id, "")
    if "No contributions" in text:
        contribs[date] = 0
    else:
        match = re.search(r'^(\d+) contribution', text)
        if match:
            contribs[date] = int(match.group(1))
        else:
            contribs[date] = 0

dates = sorted(contribs.keys())
longest_streak = 0
current_streak = 0
longest_start = ""
longest_end = ""
temp_start = ""
temp_streak = 0

for d in dates:
    if contribs[d] > 0:
        if temp_streak == 0:
            temp_start = d
        temp_streak += 1
        if temp_streak > longest_streak:
            longest_streak = temp_streak
            longest_start = temp_start
            longest_end = d
    else:
        temp_streak = 0

# Calc current
c_streak = 0
c_start = ""
c_end = ""
for i in range(len(dates)-1, -1, -1):
    d = dates[i]
    if contribs[d] > 0:
        c_streak += 1
        c_start = d
        if c_end == "":
            c_end = d
    else:
        # Check if they missed today. If they missed today, it's fine if yesterday was the end of the streak.
        if i == len(dates)-1:
            continue
        break
        
print(f"Longest Streak: {longest_streak} ({longest_start} to {longest_end})")
print(f"Current Streak: {c_streak} ({c_start} to {c_end})")
