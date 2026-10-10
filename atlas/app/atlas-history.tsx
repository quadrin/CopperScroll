"use client";

import { useEffect, useRef, useState, type ChangeEvent, type CSSProperties } from "react";
import { BookOpen, Captions, ExternalLink, Film, Maximize, Pause, Play, RotateCcw, Upload, X } from "lucide-react";
import { chapterAt, FILM_ARCHIVE_URL, FILM_CHAPTERS, FILM_DURATION, filmTime, HISTORY_EVENTS, HISTORY_REPO_URL, type FilmChapter } from "./atlas-history-data";
import "./atlas-history.css";

const assetBase = import.meta.env?.BASE_URL ?? "/";

type AtlasHistoryProps = {
    onRead?: () => void;
    onEntry?: (id: string) => void;
    /** Optional authorised or locally served media. No film is bundled by default. */
    filmSrc?: string;
};

function ProcessDiagram({ chapter, progress }: { chapter: FilmChapter; progress: number }) {
    const cutting = chapter.id === "cut";
    const separated = chapter.id === "separate";
    return <div className="history-diagram" aria-hidden="true">
        <svg viewBox="0 0 220 136" fill="none">
            <defs><linearGradient id="history-copper" x1="12" y1="20" x2="192" y2="120" gradientUnits="userSpaceOnUse"><stop stopColor="#f4d5a8"/><stop offset=".5" stopColor="#b17b51"/><stop offset="1" stopColor="#6b4a35"/></linearGradient></defs>
            <g className={`history-roll-diagram ${separated ? "is-separated" : ""}`}>
                <path d="M51 39L172 22C193 24 200 36 198 53L187 91L58 114" fill="url(#history-copper)" fillOpacity=".13" stroke="#ceaa7d" strokeWidth="1.1"/>
                <ellipse cx="52" cy="77" rx="27" ry="38" stroke="#e5c399" strokeWidth="1.5"/>
                <path d="M51 46C22 47 27 109 52 109C75 108 70 51 50 54C35 57 35 99 51 101C65 99 62 63 49 63C40 65 40 91 51 93" stroke="#c08f5f" strokeWidth="1.2"/>
                {[0, 1, 2, 3, 4].map(index => <path key={index} d={`M${78 + index * 21} ${36 - index * 3}L${72 + index * 21} ${109 - index * 4}`} stroke="#a68769" strokeOpacity=".5" strokeDasharray="2 5"/>)}
            </g>
            {cutting && <g className="history-cut-marker" style={{ transform: `translateX(${progress * 14}px)` }}>
                <path d="M106 11L103 111" stroke="#f0d1a3" strokeWidth="1.5" strokeDasharray="5 5"/>
                <circle cx="107" cy="14" r="8" stroke="#f0d1a3"/>
                <path d="M107 4V24M97 14H117" stroke="#f0d1a3" strokeWidth="1"/>
            </g>}
            {separated && <g className="history-open-diagram">
                <path d="M43 75L156 63L181 98L71 116Z" fill="#c2926220" stroke="#ecc89b"/>
                {[0, 1, 2, 3].map(index => <path key={index} d={`M${66 + index * 26} ${75 - index * 3}L${84 + index * 26} ${107 - index * 3}`} stroke="#d1ad84" strokeDasharray="3 5"/>)}
            </g>}
        </svg>
        <small>{chapter.diagramLabel}</small>
    </div>;
}

export default function AtlasHistory({ onRead, filmSrc }: AtlasHistoryProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const stageRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);
    const localUrlRef = useRef<string | null>(null);
    const pendingSeekRef = useRef<number | null>(null);
    const [localSrc, setLocalSrc] = useState<string | null>(null);
    const [filename, setFilename] = useState("");
    const [time, setTime] = useState(0);
    const [duration, setDuration] = useState(FILM_DURATION);
    const [playing, setPlaying] = useState(false);
    const [loaded, setLoaded] = useState(false);
    const [overlay, setOverlay] = useState(true);
    const [fullscreenActive, setFullscreenActive] = useState(false);
    const [error, setError] = useState("");
    const [selectedEvent, setSelectedEvent] = useState("opening");
    const source = localSrc ?? filmSrc;
    const chapter = chapterAt(time);
    const event = HISTORY_EVENTS.find(item => item.id === selectedEvent) ?? HISTORY_EVENTS[1];
    const chapterProgress = Math.min(1, Math.max(0, (time - chapter.start) / (chapter.end - chapter.start)));

    useEffect(() => () => { if (localUrlRef.current) URL.revokeObjectURL(localUrlRef.current); }, []);

    useEffect(() => {
        const changed = () => setFullscreenActive(document.fullscreenElement === stageRef.current);
        document.addEventListener("fullscreenchange", changed);
        return () => document.removeEventListener("fullscreenchange", changed);
    }, []);

    useEffect(() => {
        if (!playing) return;
        let frame = 0;
        const tick = () => {
            const video = videoRef.current;
            if (video) setTime(previous => Math.abs(previous - video.currentTime) > .06 ? video.currentTime : previous);
            frame = requestAnimationFrame(tick);
        };
        frame = requestAnimationFrame(tick);
        return () => cancelAnimationFrame(frame);
    }, [playing]);

    async function togglePlay() {
        const video = videoRef.current;
        if (!video || !source) return;
        if (video.paused) {
            if (video.ended) video.currentTime = 0;
            try { await video.play(); } catch { setError("Playback could not start. Try opening the film file again."); }
        } else video.pause();
    }

    function seek(nextTime: number) {
        const target = Math.max(0, Math.min(duration, nextTime));
        if (videoRef.current && loaded) videoRef.current.currentTime = target;
        else pendingSeekRef.current = target;
        setTime(target);
    }

    function openFilm(event: ChangeEvent<HTMLInputElement>) {
        const file = event.target.files?.[0];
        if (!file) return;
        if (!(file.type.startsWith("video/") || /\.(mp4|m4v|mov|webm)$/i.test(file.name))) {
            setError("Choose a video file, such as the supplied MP4.");
            event.target.value = "";
            return;
        }
        videoRef.current?.pause();
        if (localUrlRef.current) URL.revokeObjectURL(localUrlRef.current);
        const objectUrl = URL.createObjectURL(file);
        localUrlRef.current = objectUrl;
        setLocalSrc(objectUrl);
        setFilename(file.name);
        setTime(0);
        setLoaded(false);
        setDuration(FILM_DURATION);
        setError("");
        pendingSeekRef.current = null;
        event.target.value = "";
    }

    function closeLocalFilm() {
        videoRef.current?.pause();
        if (localUrlRef.current) URL.revokeObjectURL(localUrlRef.current);
        localUrlRef.current = null;
        setLocalSrc(null);
        setFilename("");
        setTime(0);
        setLoaded(false);
        setPlaying(false);
        setError("");
    }

    async function fullscreen() {
        try { await stageRef.current?.requestFullscreen(); } catch { setError("Full screen is unavailable in this browser."); }
    }

    return <section className="atlas-history" aria-labelledby="history-title">
        <header className="history-heading">
            <div><span className="history-eyebrow">The scroll / its afterlife</span><h2 id="history-title">Opening the Copper Scroll</h2><p>An extraordinary film, and the history around it.</p></div>
            {onRead && <button className="history-read" onClick={onRead}><BookOpen size={17}/>Read the scroll</button>}
        </header>

        <div className="history-film-layout">
            <div className="history-player">
                <div className={`history-stage ${playing ? "is-playing" : ""} ${source ? "" : "needs-film"}`} ref={stageRef}>
                    {source ? <video key={source} ref={videoRef} src={source} className="history-video" playsInline controls={fullscreenActive} preload="metadata" aria-label="Silent film of the Copper Scroll being cut open in Manchester in 1955"
                        onLoadStart={() => { setLoaded(false); setPlaying(false); setError(""); }}
                        onLoadedMetadata={event => {
                            const video = event.currentTarget;
                            setLoaded(true);
                            if (Number.isFinite(video.duration) && video.duration > 0) setDuration(video.duration);
                            if (pendingSeekRef.current !== null) {
                                video.currentTime = Math.min(pendingSeekRef.current, video.duration || FILM_DURATION);
                                pendingSeekRef.current = null;
                            }
                        }}
                        onTimeUpdate={event => setTime(event.currentTarget.currentTime)}
                        onPlay={() => { setPlaying(true); setError(""); }} onPause={() => setPlaying(false)} onEnded={() => setPlaying(false)}
                        onError={() => { setLoaded(false); setPlaying(false); setError("The film could not be loaded. Open a playable MP4, MOV or WebM copy."); }}
                    /> : <div className="history-film-empty">
                        {/* The small original SVG needs no raster image optimisation. */}
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img src={`${assetBase}history/opening-diagram.svg`} alt="Project illustration of a rolled copper sheet becoming separate curved sections"/>
                        <span className="history-film-kicker">Manchester · October 1955</span>
                        <h3>A roll of metal.<br/>A document waiting to be read.</h3>
                        <p>Open your copy of the film to watch with timed captions and diagrams.</p>
                        <button onClick={() => inputRef.current?.click()}><Upload size={17}/>Open the film</button>
                        <small>The file plays on your device.</small>
                    </div>}

                    {source && !loaded && !error && <span className="history-loading" role="status">Loading the film…</span>}
                    {source && loaded && overlay && <div className="history-overlay" key={chapter.id}>
                        <div className="history-film-stamp"><span>3 October 1955</span><small>Filmed by John Allegro · silent</small></div>
                        <ProcessDiagram chapter={chapter} progress={chapterProgress}/>
                        <div className="history-caption"><span>{String(FILM_CHAPTERS.indexOf(chapter) + 1).padStart(2, "0")} / {chapter.title}</span><p>{chapter.caption}</p></div>
                    </div>}
                    {source && loaded && !playing && <button className="history-stage-play" onClick={togglePlay} aria-label={time >= duration ? "Replay the film" : "Play the film"}>{time >= duration ? <RotateCcw size={25}/> : <Play size={25}/>}</button>}
                </div>

                <div className="history-controls">
                    <button onClick={togglePlay} disabled={!source || !loaded} aria-label={playing ? "Pause the film" : "Play the film"}>{playing ? <Pause size={19}/> : <Play size={19}/>}</button>
                    <span className="history-clock">{filmTime(time)} <span>/ {filmTime(duration)}</span></span>
                    <input type="range" min={0} max={duration} step={.1} value={Math.min(time, duration)} disabled={!source || !loaded} onChange={event => seek(Number(event.target.value))} aria-label="Film position" aria-valuetext={`${filmTime(time)} of ${filmTime(duration)}`} style={{ "--history-progress": `${time / duration * 100}%` } as CSSProperties}/>
                    <button className="history-caption-control" onClick={() => setOverlay(!overlay)} aria-pressed={overlay} title="Toggle explanatory overlay"><Captions size={18}/><span>Overlay</span></button>
                    <button onClick={fullscreen} disabled={!source || !loaded} aria-label="Show the film full screen"><Maximize size={17}/></button>
                </div>
                <div className="history-chapters" aria-label="Film chapters">
                    {FILM_CHAPTERS.map((item, index) => <button key={item.id} aria-pressed={chapter.id === item.id} onClick={() => seek(item.start)} disabled={!source || !loaded}><span>{String(index + 1).padStart(2, "0")}</span><div><strong>{item.title}</strong><small>{filmTime(item.start)}</small></div></button>)}
                </div>
                <p className="history-caption-transcript" aria-live="polite"><span>{chapter.title}</span> {chapter.caption}</p>
                <div className="history-file-row"><input ref={inputRef} type="file" accept="video/*,.mp4,.m4v,.mov,.webm" onChange={openFilm} aria-label="Open a local film file" hidden/><button onClick={() => inputRef.current?.click()}><Upload size={14}/>{source ? "Change film" : "Open a film file"}</button>{filename && <><span title={filename}>{filename}</span><button onClick={closeLocalFilm} aria-label="Close local film"><X size={14}/></button></>}</div>
                {error && <p className="history-error" role="alert">{error}</p>}
                {loaded && Math.abs(duration - FILM_DURATION) > 2 && <p className="history-error" role="status">These annotations are timed to the 1:25 archive copy. A differently edited film may not align with them.</p>}
            </div>

            <aside className="history-film-note">
                <span className="history-eyebrow">An archival view</span><h3>Watch the object become readable.</h3>
                <p>John Allegro’s film gives us a close view of the opening in Manchester. The archive dates this footage to the second cut, on 3 October 1955.</p>
                <dl><div><dt>Film</dt><dd>John Allegro, 1955</dd></div><div><dt>Digital copy</dt><dd>1 min 25 sec · silent</dd></div><div><dt>Annotations</dt><dd>Project captions and explanatory diagrams</dd></div></dl>
                <a href={FILM_ARCHIVE_URL} target="_blank" rel="noreferrer"><Film size={16}/>View the archive and provenance<ExternalLink size={13}/></a>
                <p className="history-rights">Film copyright is retained by its rights holders. DQCAAS provides the viewing copy and requests permission for reuse. Public embedding awaits that permission.</p>
            </aside>
        </div>

        <section className="history-timeline" aria-labelledby="history-timeline-title">
            <div className="history-timeline-heading"><div><span className="history-eyebrow">Discovery, editions, searches</span><h3 id="history-timeline-title">Follow the evidence through time</h3></div><a href={`${HISTORY_REPO_URL}README.md`} target="_blank" rel="noreferrer">Source ledger<ExternalLink size={13}/></a></div>
            <div className="history-event-nav" aria-label="Historical events">{HISTORY_EVENTS.map(item => <button key={item.id} aria-pressed={selectedEvent === item.id} onClick={() => { setSelectedEvent(item.id); if (item.film && source && loaded) seek(0); }}><span>{item.date}</span><strong>{item.shortTitle}</strong><i aria-hidden="true"/></button>)}</div>
            <article className="history-event" key={event.id}>
                <div className="history-event-title"><span>{event.date}</span><h4>{event.title}</h4></div>
                <div className="history-evidence-columns"><section><h5>The event</h5><p>{event.event}</p></section><section><h5>The interpretation</h5><p>{event.interpretation}</p></section><section><h5>Connection to the scroll</h5><p>{event.connection}</p></section></div>
                <div className="history-sources"><span>Sources</span>{event.sources.map((item, index) => <a key={`${item.url}-${index}`} href={item.url} target="_blank" rel="noreferrer"><strong>{item.title}<ExternalLink size={12}/></strong><small>{item.detail}</small></a>)}</div>
                {event.id === "readings" && onRead && <button className="history-continue" onClick={onRead}>Compare the readings<BookOpen size={16}/></button>}
            </article>
        </section>
    </section>;
}
