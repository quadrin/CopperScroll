"""Target candidate sets (frozen with the protocol). Each candidate is a COMPLETE line string; the part outside
the disputed word(s) is identical across the candidates of a line (ETCBC text, Greek groups dropped).
Sources: XII 10 strings R1-R7 from the frozen XII 10 protocol (agent_review_2026-10-07/wave1/T03_T04_registry/
XII10_IMAGE_READING_PROTOCOL.md, SHA-256 0e19467c...2c5); the context words of XII 10 (בשית ... בצפון כחלת
פתחא צפון) as given in that protocol and the ETCBC/DQCAAS transcription (protocol: 'preceding בשית, following
בצפון'). IX 10, I 12, VII 11, X 15: research/text/edition_confusions/variants.csv rows for those lines and
text/readings.json records e41-*, e4-immersion, e31-landmark, e49-*."""
XII10_CTX_L = 'בשית'
XII10_CTX_R = 'בצפון כחלת פתח אצפון'   # ETCBC word division of the rest of the line
TARGETS = {
 'XII 10': dict(col=12, line=10, cands={
    'R1': f'{XII10_CTX_L} שכנה {XII10_CTX_R}',
    'R2': f'{XII10_CTX_L} שבנה {XII10_CTX_R}',
    'R3': f'{XII10_CTX_L} שבצח {XII10_CTX_R}',
    'R4': f'{XII10_CTX_L} שבינח {XII10_CTX_R}',
    'R5': f'{XII10_CTX_L} שכינה {XII10_CTX_R}',
    'R6': f'{XII10_CTX_L} שכונה {XII10_CTX_R}',
    'R7': f'{XII10_CTX_L} שבצהב {XII10_CTX_R}'}),
 'IX 10': dict(col=9, line=10, cands={
    'D1_Puech_mnhh_rb': 'בקומעה כסף מנחה רב',
    'D2_Wolters_mnh_hrm': 'בקומעה כסף מנה חרם',
    'D3_Allegro_Lefkovits_mn_hhrm': 'בקומעה כסף מן החרם'}),
 'I 12': dict(col=1, line=12, cands={
    'N1_Milik_nyqrt': 'אמות שש עד ניקרת הטבילה',
    'N2_Puech_mqrt': 'אמות שש עד מקרת הטבילה',
    'N3_Eshel_nqrt': 'אמות שש עד נקרת הטבילה'}),
 'VII 11': dict(col=7, line=11, cands={
    'M1_Milik_hmsmrh': 'בדוק תחת פנת המשמרה',
    'M2_Puech_hmsth': 'בדוק תחת פנת המשטח'}),
 'X 15': dict(col=10, line=15, cands={
    'S1_ETCBC_Milik_rhyl': 'בים בית חמים של רחיל תחת',
    'S2_Puech_engraved_slwh_wl': 'בים בית המים שלוח ולתחת'}),
}
ORDER = ['IX 10', 'I 12', 'VII 11', 'X 15', 'XII 10']   # XII 10 last
