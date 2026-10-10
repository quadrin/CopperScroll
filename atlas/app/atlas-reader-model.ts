import photo from "./atlas-photo-data.json";
import type { TextData } from "./atlas-text";

export const PHOTO_COLUMN = 6;
export const PHOTO_EXAMPLE_ENTRY = "30";

export function isPhotographHash(hash: string) {
  return /^#(?:entry-[\da]+\/)?scroll\/photo$/.test(hash);
}

/** Resolve the entry that owns a word, including entries sharing one line. */
export function wordOwner(data: TextData, line: string, word: number): string | undefined {
  return Object.entries(data.entries).find(([, lines]) => lines.some(l => l.ref === line && word >= l.from && word < l.to))?.[0];
}

export function mappedWordsForEntry(data: TextData, entryId: string) {
  return photo.words.map((word, index) => ({ ...word, index })).filter(word => wordOwner(data, word.line, word.word) === entryId);
}

/** An unavailable entry opens the explicitly labelled VII example, never stale context. */
export function photoTarget(data: TextData, entryId: string) {
  const mapped = mappedWordsForEntry(data, entryId);
  const fallback = mappedWordsForEntry(data, PHOTO_EXAMPLE_ENTRY);
  const word = mapped[0] ?? fallback[0] ?? { ...photo.words[0], index: 0 };
  return { index: word.index, entryId: wordOwner(data, word.line, word.word) ?? PHOTO_EXAMPLE_ENTRY, line: word.line, word: word.word };
}
