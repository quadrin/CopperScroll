# Magen, Misgav & Tsfania 2004, *Mount Gerizim Excavations I*: NLI library photos, screened reading (21 Oct 2026)

Source: Y. Magen, H. Misgav and L. Tsfania, *Mount Gerizim Excavations I: The Aramaic, Hebrew and Samaritan Inscriptions* (Judea and Samaria Publications 2, Jerusalem 2004). Hebrew title page: "הר גריזים, כרך א: הכתובות הארמיות, העבריות והשומרוניות", JSP 2. NLI copy. Spine label (partly visible on IMG_0691): "S 308 תז", "Mount Ger[izim]…", "Magen, Izc[hak]…", "Vol. 2/1: The …", "JRR". The full shelf mark is cut off in the photo.

Photos: 39 HEIC originals, IMG_0681–0719, taken on 21 Oct 2026 between 17:57 and 18:07. Each file's Drive ID, SHA-256, capture time and page are in [gerizim_I_2004_originals.csv](gerizim_I_2004_originals.csv). All 39 SHA-256 values were recomputed from the originals and match the index. The images are not in the repo.

## How this was done

1. A screened reader (a subagent) opened only the rows of `nli_photos/sorted.csv` for this book whose `protected` field was empty. It converted the HEICs, rotated each one by OCR orientation scoring and read the pages from the OCR text and from crops.
2. English pages were OCR'd with `tesseract -l eng`. The Hebrew summary pages 2*–5* and 34*–37* were OCR'd with `heb+eng`, using the `heb` model added for this pass.
3. Every number quoted below was matched against the OCR text. The loci on Map 1 and in the locus concordance were also checked against a crop of the photo.
4. Withholding rules 1–4 were applied. Nothing in this book fell under them (see "Withheld").

## What the photos cover

| Part | Pages | Photos | Coverage |
|---|---|---|---|
| Hebrew title page; Hebrew contents | – | IMG_0681–0682 | complete |
| Hebrew introduction (summary) | 2*–5* | IMG_0683–0684 | complete, with Figs. 2 and 5 legends |
| Hebrew summary end; Hebrew bibliography | 34*–37* | IMG_0685–0686 | complete |
| English introduction | 1, 2 (Fig. 2), 4 (Fig. 3), 5 (Fig. 5), 7 (Figs. 6–7), 8–17, 25–41 | IMG_0692–0710 | **pp. 3, 6, 18–24 not photographed** |
| Explanatory notes; catalogue nos. 1–14 | 45–59 | IMG_0711–0718 | **pp. 42–44 not photographed** |
| Catalogue nos. 136–137 | 132 | IMG_0719 | single page |
| Index I, personal names | 265 | IMG_0690 | single page |
| Locus concordance (Areas S, P, J, A, B) | 271 (the photo shows the facing page also) | IMG_0687, 0689 | complete |
| Map 1, "Mount Gerizim excavations" | folding map | IMG_0688 | complete |
| Plates I–II | – | IMG_0691 | complete |

## Findings

EVIDENCE = stated in the source. INFERENCE = the project's. BK = the reader's background knowledge, not from these pages.

### P5178 and Area P

- EVIDENCE: **P5178 does not appear anywhere in the photographed pages of vol. I.** The Area P section of the locus concordance (IMG_0687) lists only loci 4004, 4034, 4036, 4166, 4204, 4227, 4300, 4385, 4462 and 4498. It also lists four surface groups: "Twelve Stones" vicinity, the Fortified Enclosure, the "Vicinity of the staircase of the southern entrance to the sacred precinct" (no. 227), and the "Mansion" (nos. 5, 180, 277–278).
- EVIDENCE: Map 1 marks no 51xx locus. Its Area P labels are 4004, 4034, 4036, 4166, 4204, 4227, 4300, 4462 and 4498.
- EVIDENCE: the mansion (Area P) is no. 17 on Fig. 2 (p. 2). Fig. 10 (p. 14) has the caption "The mansion (Area P) near the sacred precinct, where several inscriptions were found." Cat. no. 5 [K34357] came from "Area P, on the surface of the mansion" (p. 53).
- EVIDENCE: cat. no. 136 [K27836] came from "Area P, near the tower in front of the southwest staircase of the sacred precinct (L.4004)" (p. 132).
- INFERENCE: vol. I cannot close the P5178 question. Its concordance covers only inscription findspots, and no inscription is recorded from 5178. This is consistent with the 1 Oct note (`research/sites/gerizim_locus5178_followup_2026-10-01.md`) that the architectural concordance is in vol. II / JSP 20. That note's request is unchanged.

### Sacred precinct and gates

- EVIDENCE (p. 1): the temple was "built in the Persian period, during the fifth century BCE". In the Hellenistic period the city reached "about 400 dunams (800 m. long and some 500 m. wide)".
- EVIDENCE (p. 3*, Hebrew): the Persian-period precinct measured "96x98 מ', כולל השערים", glossed as about 200 × 200 cubits. It had three gates, on the north, south and east. The north gate is a six-chambered gate and was fully exposed. Remains of a stair to the east gate lie under the second-phase stair. There was no west gate, "משום קרבתו לחלקו האחורי של המקדש, קודש הקודשים" (because of its nearness to the back of the temple, the holy of holies).
- EVIDENCE (p. 8): in the Hellenistic phase the south side was doubled in length, and a two-storey fortress was added in the SE corner. The precinct "had three entrances": the western gate, for the city's inhabitants (Figs. 8–9); the eastern gate, for pilgrims; and the northern gate, "used both by those entering the temple and by the priests and Levites".
- EVIDENCE: Fig. 5 (p. 5) key: 13–14 northern chamber gates; 19 monumental staircase leading to the eastern gate; 20/22 eastern gate; 21 paved street to the eastern gate; 23 "Remains of an altar beneath the eastern gate, apparently dating to the Persian period"; also the western entrance, a tower protecting the western entrance, and the fortified enclosure. Fig. 2 (p. 2) adds the lower gatehouse, the southern city-gate and the courtyards for pilgrims' accommodation.
- EVIDENCE (p. 14): the precinct was destroyed when John Hyrcanus I conquered the mountain "in 112–111 BCE". Zeno built a church and fortified enclosure in 484 CE, and Justinian extended the enclosure in 529 CE.
- EVIDENCE (pp. 12–13): "A Hasmonean garrison was stationed there until the reign of Alexander Jannaeus, and perhaps even later". Hundreds of coins postdate 128 BCE. The latest Seleucid coins date to 112–111 BCE.

### Water installations and cisterns

- EVIDENCE: the only water installations named in these pages are:
  - bathtubs in private houses, which the authors relate to priests' ritual purity (p. 10): bathing in flowing water such as a spring was the norm, yet "bathtubs were found inside private residences";
  - a cistern in Area S. Cat. nos. 7 [K23974] and 12 [K23975] came from "Area S, in a cistern in the northern part of the church enclosure (L.196)" (pp. 54, 57). L.196 is listed under Area S in the concordance.
- EVIDENCE: Fig. 2 marks a "Byzantine bathhouse" in the monastery complex (no. 3). It is not a temple-city water installation.
- EVIDENCE: these pages give no list or plan of cisterns, pools or channels for the Hellenistic city. The p. 1 sentence on the city's lack of natural advantages (it was built on "a high, cold, and bare mountain with no …") breaks off at the end of the photographed page.
- INFERENCE: the L.196 cistern lies within the Byzantine church enclosure on the summit. The inscribed stones were found in it, and nothing here says when it was built or used. It does not bear on the Area P courtyard cistern of the atlas text.

### Inscriptions relevant to treasure, deposits, priests or a "house"

- EVIDENCE: the formulae are "זי הקרב" ("that which offered"), with or without "לדכרן טב קדם אלהא באתרא דנה" ("for good remembrance before God in this place") (pp. 16–17). Two inscriptions name "this stone" ("אבנא דה", nos. 147, 148).
- EVIDENCE (p. 17): the root קרב "usually refers rather to the donation of a sacrifice than to a contribution of money or of stone". The authors nevertheless conclude that the קרב inscriptions "relate to contributions of money". "The only inscription from Mt. Gerizim that makes explicit mention of a sacrifice" is no. 199, which is not photographed. They compare the Jerusalem Temple's contributions of animals and of "silver" (Ex. 25:1–7) and the "value pledges" of Lev. 27.
- EVIDENCE (p. 15): the authors suggest that the size and position of the stones in the wall around the temple "may possibly be related to the amount of money or the nature of the offering given".
- EVIDENCE on priests (pp. 11, 25–28, 34–35): the title "priest" (כהן/כהניא) occurs in nos. 24–25, 382, 388–389. Priestly names include El'azar (nos. 1, 32, 390) and Pinhas ("five times", including nos. 24, 29, 384, 389). No. 388 names a priest and his wife. The Neo-Hebrew-script inscriptions are interpreted as priestly and are thought to have been set on the inner face of the precinct wall, "where only the priests had access" (p. 15).
- EVIDENCE: the only "house" words met are בית in place names and the "temple" (no בית with a treasure sense). "Mansion" is a modern label. No inscription in the photographed catalogue (nos. 1–14, 136–137) or in Index I (p. 265) mentions a treasury, a deposit, a chest, vessels, silver or the karsh.
- EVIDENCE: not one inscription was found in situ (pp. 14–15). Most come from the surface or from secondary contexts on the eastern slope and in Area S (pp. 14, 45).
- EVIDENCE: all the inscriptions are dated to the Hellenistic period (3rd–2nd c. BCE), except the medieval Samaritan-script ones (pp. 15, 41; p. 34* in the Hebrew summary).

### Other

- EVIDENCE (p. 25): the corpus names 144 people; 89 names can be identified, giving 55 different names.
- EVIDENCE (p. 27): one inscription contains "שמרין" (Samaria). Place names include Shechem, Kfar Haggai, Avarta(?), Yoqme'am and Tura Taba ("Good Mountain", which Josephus mentions in *Ant.* 18:86) (pp. 27–29).

## What these pages do NOT say

- They give no locus 5178, basket 51777, K35264, Area P plan or mansion cistern.
- They give no staircase step counts (seven-step or 15-step flights) and no "upper pit" or shaft.
- They give no Hellenistic-city cistern inventory and no water-supply description.
- They record no deposit or hoard and no inscription naming a treasury or stored valuables.
- They say nothing on use of the summit in the 1st c. CE beyond the garrison "perhaps even later".

## Withheld

Nothing withheld. The book contains no SULTAN-1, Jericho escarpment, Qumran cave or Kh. ʿAlmit material, and no image of the Copper Scroll. Figs. 13–14 on pp. 33–35 reproduce Qumran *biblical* scroll fragments (4QSam, 4QJer, Leviticus) for palaeography. These are not the Copper Scroll and are cited only by caption.

## Still missing

- pp. 3, 6, 18–24 and 42–44, and the rest of the catalogue (nos. 15–135 and 138–394), including no. 199 (sacrifice) and nos. 382–389 (priests). Index pp. 266–270 are also missing.
- Vol. II (JSP 8) and JSP 20 remain the targets for P5178.
