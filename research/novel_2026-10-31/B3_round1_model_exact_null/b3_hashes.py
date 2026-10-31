"""SHA-256 of every round-1 file copied verbatim into this folder, against the same file at round-1 commit
bd06dcc6 (extracted with `git archive bd06dcc6 research/novel_2026-10-30/B_analysis_by_synthesis` into
SP/products/B3/r1_pinned/) and against the hash stated in round 1's PROTOCOL_FROZEN.md -> model_files_sha256.csv"""
import hashlib, csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad'
R1 = f'{SP}/products/B3/r1_pinned/research/novel_2026-10-30/B_analysis_by_synthesis'
STATED = {'model.py': '191855431575fcfe91a023c57b34527de707ef7355d7cb0b755c755c0b6ed39a',
          'abs_score.py': '6d0f1362145299bbbcc49f51d4cbd45158f9a105d63a33fa17c70963b3295c61',
          'glyphs.json': '9a320070084363b3c7223ae30b29d86a2f690ca13defc19b9886f8879df4fefa',
          'frozen_params.json': 'df825c762bb3784b71051744a6cc5f74bc1ab680403fcc8c7d4a06f030d23f39',
          'candidates.py': '4702a998e6d138bc7d92b48384038deefa48313795ca5a098f80a1dc271988e1',
          'calibration_items.json': '66b0979bb6d0b3334d6fd1d84539046851dd90b50462fbbde0472bc8ff4c7996',
          'prep.py': '0d52fced5d4a281fcee78b74d333e47f120bcb6368cbb6dc9c6c8992ab0cf8b7',
          'targets.py': '29f5fe8d42688328f9464cddf9dca1adafe093913c6a1596d0e3b00852af885f',
          'etcbc_lines.json': '3959751b6d0c2fdcc3f686673ba12c2728f2457d149602996885a66689dceebe'}
FILES = ['model.py', 'abs_score.py', 'glyphs.py', 'glyphs.json', 'frozen_params.json', 'candidates.py', 'confirm.py',
         'prep.py', 'targets.py', 'etcbc_lines.json', 'calibration_items.json']
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
if __name__ == '__main__':
    rows = []
    for f in FILES:
        a, b = h(f'{HERE}/{f}'), h(f'{R1}/{f}')
        rows.append(dict(file=f, sha256_b3_copy=a, sha256_round1_at_bd06dcc6=b, identical=a == b,
                         sha256_stated_in_round1_protocol=STATED.get(f, ''),
                         matches_round1_protocol=(STATED[f] == a) if f in STATED else 'not stated'))
        print(f, a == b, rows[-1]['matches_round1_protocol'])
    with open(f'{HERE}/model_files_sha256.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
