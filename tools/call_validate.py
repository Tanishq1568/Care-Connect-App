import urllib.request
url = 'http://127.0.0.1:5090/__debug/validate_index'
try:
    r = urllib.request.urlopen(url, timeout=5)
    data = r.read().decode('utf-8')
    print('STATUS', r.getcode())
    print(data[:4000])
except Exception as e:
    print('ERROR', e)