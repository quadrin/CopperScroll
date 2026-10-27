"""Run 15 (hoard_contexts_2026-10-27): re-run run 4's run.py with the recovered hoard values, nothing else changed.

Usage: python3 -I rerun.py [main|explore]
  main    : apply only values recovered from sources (OVERRIDES) -> out/rerun/
  explore : additionally apply exploratory Feshkha denomination scenarios (not part of the verdict) -> out/explore_*/
run.py is run 4's script copied unchanged except for its OUT path.
"""
import sys, json, importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('run4', os.path.join(HERE, 'run.py'))
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

# Values recovered from sources (EVIDENCE quoted; coding = INFERENCE using the hoards_full/precedent rules).
OVERRIDES = {
    # CHRE 8180 comment quoting Zissu & Eshel 2000-02 (INJ 14), p. 165: "A hoard was found in an agricultural field in a
    # riverbed about two km from the ruin". Land use: Cultivated Land; discovery: Agricultural or drainage work.
    # Precedent coding: open ground, placement not stated -> C11 field or open ground, G5 (cf. El Fawar, Jericho 1973).
    'chre8180': dict(setting='open_ground', placement='not_stated', fine='C11', coarse='G5',
                     context_text='found in an agricultural field in a riverbed about two km from the ruin '
                                  '(Zissu & Eshel 2000-02: 165, quoted in CHRE 8180)'),
}
# Unchanged after reading (recorded for the log; no field changes):
#  chre7541 St Stephen's Gate: Hill, QDAP 6 (1936) 78: "Information as to the circumstances of the find is not forthcoming"; Ophel or St Stephen's Gate.
#  chre8082 Jericho 1874: Evans, Academy 12 Sep 1874, 296-297; Madden 1881, 69 n.1: earthen pot, cover secured with lead; no setting.
#  chre7586 'Ein Feshkha 1953: ADAJ 2 (1953) 89-90: "In a cave somewhere in the neighbourhood of Feshkha"; coin list by ruler, no denominations.
#  chre7901, 7953, 7956, 8117: no new source reached.

# Exploratory only: Feshkha mass if denominations were uniform (INFERENCE, not stated in ADAJ).
EXPLORE = {
    'feshkha_all_3.8g': {'chre7586': dict(ag=(277 * 3.8, 277 * 3.8))},
    'feshkha_roman14.2_nab3.8': {'chre7586': dict(ag=(206 * 14.2 + 71 * 3.8, 206 * 14.2 + 71 * 3.8))},
}

_orig_build = R.build_hoards


def make_build(over):
    def build(variant):
        hs = _orig_build(variant)
        for h in hs:
            if h['id'] in over:
                h.update(over[h['id']])
        return hs
    return build


def run(over, outdir):
    os.makedirs(outdir, exist_ok=True)
    R.OUT = outdir
    R.build_hoards = make_build(over)
    R.main()


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'main'
    if mode == 'main':
        run(OVERRIDES, os.path.join(BASE, 'out', 'rerun'))
    else:
        for name, ex in EXPLORE.items():
            o = copy.deepcopy(OVERRIDES)
            for k, v in ex.items():
                o.setdefault(k, {}).update(v)
            run(o, os.path.join(BASE, 'out', 'explore_' + name))
