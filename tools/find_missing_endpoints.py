from app import app
import re, glob
names=set()
for t in glob.glob('templates/*.html'):
    s=open(t,encoding='utf-8').read()
    for m in re.finditer(r"url_for\('\s*([^'\)]+)\s*'\)", s):
        names.add(m.group(1))
print('Referenced endpoints in templates:')
print('\n'.join(sorted(names)))
print('\nRegistered endpoints in app.url_map:')
endpoints={rule.endpoint for rule in app.url_map.iter_rules()}
print('\n'.join(sorted(endpoints)))
missing=[n for n in names if n not in endpoints]
print('\nMissing endpoints:')
print('\n'.join(sorted(missing)) if missing else 'None')
