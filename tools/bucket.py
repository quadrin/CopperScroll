#!/usr/bin/env python3
"""Read gs://copper-scroll-cog-1030 with the HMAC key (no gcloud needed).
Key: Drive file "Copper Scroll gcloud env.rtf" (ID 1oldXIyl1QEVMjpIeFEbOZaTCdHPZx6eY).
Set HEXCOG_HMAC_ID and HEXCOG_HMAC_SECRET in the environment.
  python3 bucket.py ls [prefix]          list one level
  python3 bucket.py get <key> [out]      download (stdout if no out)
"""
import os, sys, hmac, hashlib, datetime, urllib.request, urllib.parse, re
B, H = 'copper-scroll-cog-1030', 'storage.googleapis.com'
K, S = os.environ['HEXCOG_HMAC_ID'], os.environ['HEXCOG_HMAC_SECRET']

def req(path, params=None, rng=None):
    t = datetime.datetime.now(datetime.timezone.utc); amz = t.strftime('%Y%m%dT%H%M%SZ'); d = amz[:8]
    q = '&'.join(f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}" for k, v in sorted((params or {}).items()))
    path = '/' + B + ('/' + urllib.parse.quote(path, safe='/') if path else '')
    ph = hashlib.sha256(b'').hexdigest(); sh = 'host;x-amz-content-sha256;x-amz-date'
    cr = f"GET\n{path}\n{q}\nhost:{H}\nx-amz-content-sha256:{ph}\nx-amz-date:{amz}\n\n{sh}\n{ph}"
    scope = f"{d}/auto/s3/aws4_request"
    k = ('AWS4' + S).encode()
    for m in (d, 'auto', 's3', 'aws4_request'): k = hmac.new(k, m.encode(), hashlib.sha256).digest()
    sig = hmac.new(k, f"AWS4-HMAC-SHA256\n{amz}\n{scope}\n{hashlib.sha256(cr.encode()).hexdigest()}".encode(), hashlib.sha256).hexdigest()
    h = {'x-amz-date': amz, 'x-amz-content-sha256': ph,
         'Authorization': f"AWS4-HMAC-SHA256 Credential={K}/{scope}, SignedHeaders={sh}, Signature={sig}"}
    if rng: h['Range'] = rng
    return urllib.request.urlopen(urllib.request.Request(f"https://{H}{path}" + (f"?{q}" if q else ''), headers=h), timeout=120)

if __name__ == '__main__':
    cmd, *a = sys.argv[1:] or ['ls']
    if cmd == 'ls':
        x = req('', {'delimiter': '/', 'prefix': a[0] if a else '', 'max-keys': '1000'}).read().decode()
        for p in re.findall(r'<CommonPrefixes><Prefix>([^<]*)', x): print(p)
        for k in re.findall(r'<Key>([^<]*)</Key>', x): print(k)
    elif cmd == 'get':
        data = req(a[0]).read()
        open(a[1], 'wb').write(data) if len(a) > 1 else sys.stdout.buffer.write(data)
