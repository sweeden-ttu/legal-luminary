#!/usr/bin/env python3
"""Build _data/candidates/courts/<slug>.json from the news articles each judicial profile already cites.

Reads every markdown profile under collections/_candidates/courts/, collects [label](url) links whose host is a
news outlet, and writes them as the profile's "In the News" sidebar list. Titles come from the article URL slug
(KDH, San Antonio Report, etc. put the headline in the path); the excerpt is the sentence of the profile that cites it.
"""
import glob, json, os, re, sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS = {
    'kdhnews.com': 'Killeen Daily Herald', 'tdtnews.com': 'Temple Daily Telegram', 'kwtx.com': 'KWTX',
    'kcentv.com': 'KCEN-TV', 'kxxv.com': 'KXXV', 'fox44news.com': 'FOX 44', 'texastribune.org': 'The Texas Tribune',
    'sanantonioreport.org': 'San Antonio Report', 'newsfromthestates.com': 'States Newsroom', 'communityimpact.com': 'Community Impact',
    'houstonchronicle.com': 'Houston Chronicle', 'dallasnews.com': 'Dallas Morning News', 'statesman.com': 'Austin American-Statesman',
    'expressnews.com': 'San Antonio Express-News', 'texaslawyer.com': 'Texas Lawyer', 'law360.com': 'Law360',
    'austinchronicle.com': 'Austin Chronicle', 'reformaustin.org': 'Reform Austin', 'texasobserver.org': 'Texas Observer',
    'kvue.com': 'KVUE', 'click2houston.com': 'KPRC', 'apnews.com': 'AP News', 'reuters.com': 'Reuters',
}
LINK = re.compile(r'\[([^\]]+)\]\((https?://[^\s)]+)\)')

def title_from_url(url, host):
    path = urlparse(url).path.strip('/')
    segs = [s for s in path.split('/') if s]
    slug = ''
    for s in segs:
        if s.startswith('article_') or re.fullmatch(r'[0-9a-f-]{20,}', s): continue
        if re.search(r'[a-z]+-[a-z]+', s): slug = s
    slug = re.sub(r'\.html?$', '', slug)
    slug = '-'.join(w for w in slug.split('-') if not w.isdigit())
    if not slug: return NEWS.get(host, host)
    small = {'a','an','the','and','or','of','to','in','on','for','at','by','as','vs','with','from','after','ahead','is','its','be'}
    words = slug.split('-')
    t = ' '.join(w if (i and w in small) else w.capitalize() for i, w in enumerate(words))
    for w in ('jp', 'kdh', 'tx', 'gop', 'jag', 'kwtx', 'kcen'):
        t = re.sub(r'\b' + w + r'\b', w.upper(), t, flags=re.I)
    return t

def sentence_around(text, url):
    i = text.find(url)
    if i < 0: return ''
    abbr = re.compile(r'(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec|Gov|Jr|Sr|No|Rep|Sen|Dr|Mr|Ms|St|Lt|Col|Gen|Hon|U\.S|v|vs)\.$')
    start = i
    while True:
        j = max(text.rfind('. ', 0, start), text.rfind('\n', 0, start))
        if j < 0: start = 0; break
        if text[j] == '\n' or not abbr.search(text[:j + 1]): start = j + 1; break
        start = j
    end = i + len(url)
    while True:
        k = text.find('.', end)
        if k < 0: end = len(text); break
        if abbr.search(text[:k + 1]) or (k + 1 < len(text) and text[k+1].isdigit()): end = k + 1; continue
        end = k + 1; break
    s = text[start:end]
    s = LINK.sub(r'\1', s)
    s = re.sub(r'[*_]{1,2}', '', s).replace("''", "'").strip()
    return s[:300]

SUPPLEMENT = os.path.join(ROOT, '_data/candidates/courts/_supplement.json')
extra = json.load(open(SUPPLEMENT)) if os.path.exists(SUPPLEMENT) else {}

count = 0
for md in sorted(glob.glob(os.path.join(ROOT, 'collections/_candidates/courts/*/*.md'))):
    text = open(md, encoding='utf-8').read()
    m = re.search(r'^candidate_slug:\s*(\S+)', text, re.M)
    if not m: continue
    slug = m.group(1)
    t = re.search(r'^title:\s*(.+)$', text, re.M)
    name = t.group(1).strip().strip('"\'') if t else slug
    seen, arts = set(), []
    for label, url in LINK.findall(text):
        host = urlparse(url).netloc.lower().removeprefix('www.')
        if host not in NEWS or url in seen: continue
        seen.add(url)
        arts.append({'url': url, 'title': title_from_url(url, host), 'domain': host, 'outlet': NEWS[host],
                     'excerpt': sentence_around(text, url), 'confidence': 'high', 'field': 'cited_in_profile'})
    for a in extra.get(slug, []):
        if a['url'] in seen:
            for x in arts:
                if x['url'] == a['url'] and a.get('title'): x['title'] = a['title']
            continue
        seen.add(a['url']); host = urlparse(a['url']).netloc.lower().removeprefix('www.')
        arts.append({'url': a['url'], 'title': a.get('title') or title_from_url(a['url'], host), 'domain': host,
                     'outlet': NEWS.get(host, host), 'excerpt': a.get('excerpt', ''), 'confidence': 'high', 'field': 'news_coverage'})
    if not arts: continue
    out = {'candidate_slug': slug, 'name': name, 'city': 'courts', 'articles': arts}
    with open(os.path.join(ROOT, '_data/candidates/courts', slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False); f.write('\n')
    count += 1
    print(f'{slug}: {len(arts)} article(s)')
print(f'{count} files written', file=sys.stderr)
