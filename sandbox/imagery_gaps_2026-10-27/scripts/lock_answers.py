"""Lock a blind scorer's answers BEFORE the key is opened.
Usage: python3 -I lock_answers.py <stage A|B> <raw_answers_file>
Copies the file to answers/answers_<stage>.json (after checking it parses as JSON), appends
SHA-256 + UTC time to answers/answers.lock, and prints them. Refuses to overwrite an existing lock."""
import sys, json, hashlib, datetime, pathlib, shutil
RUN = pathlib.Path(__file__).parent.parent
stage, raw = sys.argv[1], pathlib.Path(sys.argv[2])
json.loads(raw.read_text())  # must parse
d = RUN / 'answers'; d.mkdir(exist_ok=True)
dst = d / f'answers_{stage}.json'
if dst.exists(): raise SystemExit(f'{dst} already locked; not overwriting')
shutil.copyfile(raw, dst)
h = hashlib.sha256(dst.read_bytes()).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with open(d / 'answers.lock', 'a') as f: f.write(f'stage {stage}  {now}  sha256 {h}  {dst.name}\n')
print(stage, now, h)
