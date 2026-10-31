"""Write sha256_inputs.txt: SHA-256 of B4 inputs and frozen files."""
import hashlib, glob, os
import b4lib as B

W = "../../agent_review_2026-10-07/wave2/W2F_plates_model/data"
groups = [
    ("A2 code and outputs reused unchanged (origin/claude/novel-2026-10-31-A2 at 6a309e75042d872988712235f7e32cd26d568ae3)",
     sorted(glob.glob("a2_reused/*.py")) + sorted(glob.glob("a2_reused/reg/*.json")) + sorted(glob.glob("a2_reused/place/*.json"))),
    ("Reader (scratchpad)", [B.SP + "/tools/hexview/hexview.py"]),
    ("Text and edition data", ["etcbc_lines.json", "../../text/edition_confusions/variants.csv",
                               "../../text/edition_confusions/confusions.csv", "../../text/plate_check.md",
                               "../../agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md"]),
    ("W2F letter boxes and alignment", [f"{W}/labels_verified.csv", f"{W}/registration.json", f"{W}/viterbi_col10.json",
                                        f"{W}/fac_components_col10.json"]),
    ("B4 code and pre-freeze data", ["b4lib.py", "items4.py", "model4.py", "run4.py", "targets4.py", "prepare4.py",
                                     "hash4.py", "items4.json", "placements4.csv", "x_explore.py", "x_codetest.py",
                                     "x_place.py", "x_inspect.py", "x_montage.py"] + sorted(glob.glob("explore/*.json"))),
    ("Private TRAIN patch cache (scratchpad, not in the repository)", [B.PROD + "/train_patches.npz"]),
]
os.chdir(B.HERE)
with open("sha256_inputs.txt", "w") as fh:
    fh.write("# SHA-256 of B4 inputs and frozen files (31 Oct 2026). Relative paths are relative to this folder.\n")
    for title, files in groups:
        fh.write(f"## {title}\n")
        for f in files:
            fh.write(f"{hashlib.sha256(open(f, 'rb').read()).hexdigest()}  {f}\n")
print(open("sha256_inputs.txt").read())
