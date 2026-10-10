/** Historical summaries are paraphrases. They do not alter research assessments. */
export const FILM_ARCHIVE_URL = "https://dqcaas.com/2016/11/24/1953-film-of-cutting-open-of-the-copper-scroll/";
export const HISTORY_REPO_URL = "https://github.com/quadrin/CopperScroll/blob/main/research/history/salvage_records/";
export const FILM_DURATION = 85.12;

export type FilmChapter = {
    id: "roll" | "cut" | "separate";
    start: number;
    end: number;
    title: string;
    caption: string;
    diagramLabel: string;
};

// Chapter boundaries describe changes in this supplied digital copy, not cuts
// in the metal. Diagrams are explanatory and are not traced from the footage.
export const FILM_CHAPTERS: FilmChapter[] = [
    {
        id: "roll", start: 0, end: 24, title: "The mounted roll",
        caption: "The rolled copper is held in the cutting apparatus. The camera shows the roll and the operator together.",
        diagramLabel: "Rolled sheet · explanatory diagram",
    },
    {
        id: "cut", start: 24, end: 65, title: "A closer view of cutting",
        caption: "The view moves closer to the blade and the surface of the roll. Cutting allowed the brittle document to be opened in sections.",
        diagramLabel: "Cutting into sections · explanatory diagram",
    },
    {
        id: "separate", start: 65, end: FILM_DURATION, title: "The separated edge",
        caption: "The final view shows a section separating from the roll. A physical cut and a written column are different ways of dividing the scroll.",
        diagramLabel: "Sections and writing · explanatory diagram",
    },
];

export function chapterAt(time: number): FilmChapter {
    return FILM_CHAPTERS.find(chapter => time >= chapter.start && time < chapter.end)
        ?? (time >= FILM_DURATION ? FILM_CHAPTERS[2] : FILM_CHAPTERS[0]);
}

export function filmTime(time: number): string {
    const seconds = Math.max(0, Math.floor(Number.isFinite(time) ? time : 0));
    return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}

type HistorySource = { title: string; detail: string; url: string };
export type HistoryEvent = {
    id: string;
    date: string;
    shortTitle: string;
    title: string;
    event: string;
    interpretation: string;
    connection: string;
    sources: HistorySource[];
    film?: boolean;
};

export const HISTORY_EVENTS: HistoryEvent[] = [
    {
        id: "discovery", date: "1952", shortTitle: "Discovery", title: "Two rolls in Cave 3",
        event: "The Copper Scroll was found on 20 March 1952 during the Qumran caves expedition. Reed’s report places Cave 3 about two kilometres north of Khirbet Qumran.",
        interpretation: "The expedition was surveying caves for manuscripts and antiquities. The copper document had not yet been opened and read.",
        connection: "Cave 3 is the document’s find-spot. That fact does not identify the places or deposits listed in its text.",
        sources: [
            { title: "W. L. Reed, expedition report", detail: "BASOR 135 (1954), pp. 8–13; discovery p. 10, map Fig. 2.", url: "https://www.jstor.org/stable/1355541" },
            { title: "Contemporary discovery report", detail: "New York Times, 12 April 1952, p. 13.", url: "https://www.nytimes.com/1952/04/12/archives/scrolls-of-bronze-in-dead-sea-cave-2-tightly-rolled-sheets-with.html" },
        ],
    },
    {
        id: "opening", date: "1955", shortTitle: "Opening", title: "The moment the roll becomes accessible", film: true,
        event: "H. Wright Baker first opened the scroll in Manchester on 1 October 1955. DQCAAS dates John Allegro’s film to 3 October, at the time of a second cut.",
        interpretation: "The film records the physical opening. The diagrams and captions in this player explain that process; they are project annotations.",
        connection: "Opening exposed the document for reading. The footage does not resolve individual disputed letters or locate a listed deposit.",
        sources: [
            { title: "DQCAAS film archive", detail: "Provenance, filming date, digitisation and copyright information.", url: FILM_ARCHIVE_URL },
            { title: "Opening the Copper Scroll", detail: "J. A. Brown, in John Marco Allegro: The Maverick of the Dead Sea Scrolls (2005), pp. 60–75; cited by DQCAAS.", url: FILM_ARCHIVE_URL },
        ],
    },
    {
        id: "searches", date: "1959–63", shortTitle: "Early searches", title: "A text taken into the landscape",
        event: "Albright’s October 1960 review reports an unsuccessful Allegro treasure hunt. A Reuters dispatch of 28 December 1961 reports a further Allegro-led excavation beginning in the Dead Sea area.",
        interpretation: "The project’s search ledger retains the reports’ different dates and purposes. The contemporary items do not name the excavated sites or give trench plans and depths.",
        connection: "These reports document expeditions. Their missing footprints prevent an entry-by-entry judgment about which predicted targets were searched.",
        sources: [
            { title: "W. F. Albright, ‘Visions of Gold’", detail: "New York Times Book Review, 9 October 1960, p. 51.", url: "https://www.nytimes.com/1960/10/09/archives/visions-of-gold-the-treasure-of-the-copper-scroll-by-john-marco.html" },
            { title: "Reuters, ‘More Dead Sea Scrolls Sought’", detail: "New York Times, 29 December 1961, p. 11; dispatch dated 28 December.", url: "https://www.proquest.com/hnpnewyorktimes/docview/115312608" },
            { title: "Project search ledger, S03–S05", detail: "Source comparison, date conflicts and coverage limits.", url: `${HISTORY_REPO_URL}README.md#the-search-ledger` },
        ],
    },
    {
        id: "edition", date: "1962", shortTitle: "An edition", title: "The physical object becomes an edited text",
        event: "Milik’s edition appeared in Les Petites Grottes de Qumrân, the third volume of Discoveries in the Judaean Desert.",
        interpretation: "An edition transcribes, restores and interprets the damaged text. Later editors can disagree over a letter, a word, an entry boundary or a unit.",
        connection: "The reading page keeps edition-based readings attached to their sources. A geographical candidate should carry the reading on which it depends.",
        sources: [
            { title: "Baillet, Milik and de Vaux, DJD III", detail: "Les Petites Grottes de Qumrân (1962); library catalogue and source index.", url: "https://github.com/quadrin/CopperScroll/blob/main/research/sources/drive_index.md" },
            { title: "Project reading apparatus", detail: "Edition citations and retained textual alternatives.", url: "https://github.com/quadrin/CopperScroll/blob/main/text/readings.json" },
        ],
    },
    {
        id: "juglet", date: "1988–89", shortTitle: "A juglet", title: "A discovery, an analysis, and a claim",
        event: "Patrich and Arubas report a juglet found in Pit B of a cave near Qumran during February–April 1988. Their 1989 publication includes a plan, section and analysis of its non-olive plant oil.",
        interpretation: "The excavators considered balsam oil as a possibility. Jones’s identification with Temple anointing oil was a separate claim. The 1989 newspaper report and excavation report also differ over the find date.",
        connection: "The juglet is a documented archaeological find. Its association with a particular Copper Scroll deposit has not been demonstrated.",
        sources: [
            { title: "Patrich and Arubas, excavation report", detail: "IEJ 39 (1989), pp. 43–59; find p. 49, plan and section Fig. 2, analysis pp. 50–59.", url: "https://www.jstor.org/stable/27926136" },
            { title: "J. Brinkley, contemporary report", detail: "New York Times, 16 February 1989; reported find and competing interpretations.", url: "https://www.nytimes.com/1989/02/16/world/balsam-oil-of-israelite-kings-found-in-cave-near-dead-sea.html" },
            { title: "Project search ledger, S13", detail: "Find context, source differences and the unestablished scroll connection.", url: `${HISTORY_REPO_URL}README.md#conflicts-kept-open` },
        ],
    },
    {
        id: "readings", date: "2000–15", shortTitle: "New readings", title: "The reading remains an argument",
        event: "Lefkovits’s re-evaluation (2000), the Brizemeure, Lacoudre and Puech volume (2006), and Puech’s revisiting of the scroll (2015) bring further editions and discussions into the source library.",
        interpretation: "Better documentation can sharpen a reading without removing every uncertainty. The atlas distinguishes the photographed surface, editorial restorations and geographical interpretations.",
        connection: "Compare readings in the reader, then follow their consequences for a place or feature. A more detailed image alone does not raise identification confidence.",
        sources: [
            { title: "Edition library index", detail: "Lefkovits 2000; Brizemeure, Lacoudre and Puech 2006; Puech 2015.", url: "https://github.com/quadrin/CopperScroll/blob/main/research/sources/drive_index.md" },
            { title: "Original-photo reading audit", detail: "What the project could and could not establish from available original photographs.", url: "https://github.com/quadrin/CopperScroll/blob/main/research/text/plate_check.md" },
        ],
    },
];
