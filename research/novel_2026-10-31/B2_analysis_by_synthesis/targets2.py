"""B2 target candidate sets (frozen with the protocol). Scored ONLY if the held-out test passes.

Each candidate is a complete line string; outside the disputed word(s) the text is identical across the
candidates of a line. The sets are the round-1 sets (research/novel_2026-10-30/B_analysis_by_synthesis/
targets.py on branch claude/novel-2026-10-30-B), which were taken from repository records:
  XII 10: R1-R7 from the frozen XII 10 protocol (research/agent_review_2026-10-07/wave1/T03_T04_registry/
          XII10_IMAGE_READING_PROTOCOL.md, SHA-256 0e19467c618f80438c12445b7380f77f5c59b7fe241da9c80878601e2e26a2c5);
          context words בשית ... בצפון כחלת פתח אצפון (ETCBC word division of the rest of the line).
  IX 10, I 12, X 15: research/text/edition_confusions/variants.csv rows for those lines and the
          text/readings.json records (e41-*, e4-immersion, e49-*).
  VII 11: cuts 13 and 14 are absent from the bucket, so VII 11 cannot be scored (recorded, not run).
The XII 10 images were released by the owner on 30 October 2026 and are exposed; IX 10 was read on CT17
on 30 October (branch claude/ix10-ct17-qumran-2026-10-30). Any target output is an exposed-image model
output, not a reading and not an unused-observation test.
"""
XII10_CTX_L = 'בשית'
XII10_CTX_R = 'בצפון כחלת פתח אצפון'
TARGETS = {
    'IX 10': dict(col=9, line=10, cuts=[16, 17], cands={
        'D1_Puech_mnhh_rb': 'בקומעה כסף מנחה רב',
        'D2_Wolters_mnh_hrm': 'בקומעה כסף מנה חרם',
        'D3_Allegro_Lefkovits_mn_hhrm': 'בקומעה כסף מן החרם'}),
    'I 12': dict(col=1, line=12, cuts=[2, 3, 4], cands={
        'N1_Milik_nyqrt': 'אמות שש עד ניקרת הטבילה',
        'N2_Puech_mqrt': 'אמות שש עד מקרת הטבילה',
        'N3_Eshel_nqrt': 'אמות שש עד נקרת הטבילה'}),
    'X 15': dict(col=10, line=15, cuts=[17, 18], cands={
        'S1_ETCBC_Milik_rhyl': 'בים בית חמים של רחיל תחת',
        'S2_Puech_engraved_slwh_wl': 'בים בית המים שלוח ולתחת'}),
    'XII 10': dict(col=12, line=10, cuts=[21, 22, 23], cands={
        'R1': f'{XII10_CTX_L} שכנה {XII10_CTX_R}',
        'R2': f'{XII10_CTX_L} שבנה {XII10_CTX_R}',
        'R3': f'{XII10_CTX_L} שבצח {XII10_CTX_R}',
        'R4': f'{XII10_CTX_L} שבינח {XII10_CTX_R}',
        'R5': f'{XII10_CTX_L} שכינה {XII10_CTX_R}',
        'R6': f'{XII10_CTX_L} שכונה {XII10_CTX_R}',
        'R7': f'{XII10_CTX_L} שבצהב {XII10_CTX_R}'}),
}
NOT_SCORABLE = {'VII 11': 'cuts 13 and 14 absent from the bucket'}
ORDER = ['IX 10', 'I 12', 'X 15', 'XII 10']
