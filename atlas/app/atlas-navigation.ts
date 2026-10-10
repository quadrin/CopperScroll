export const atlasModes = ["2d", "3d", "ground", "scene", "scroll", "landscape", "dossier", "history"] as const;
export type AtlasMode = (typeof atlasModes)[number];
const validEntryId = /^(?:[1-9]|[1-5]\d|60|12a)$/;
const modeAliases: Record<string, AtlasMode | undefined> = {
  "2d": "2d", "3d": "3d", ground: "ground", photo: "ground", scene: "scene",
  scroll: "scroll", landscape: "landscape", dossier: "dossier", history: "history",
};
export function entryHash(id: string, mode: string) {
  const suffix = mode === "2d" ? "" : mode === "ground" ? "/photo" : `/${mode}`;
  return `#entry-${id}${suffix}`;
}
export function parseAtlasHash(hash: string) {
  const workbench = hash.match(/^#workbench(?:\/(relationships|inventory|states|coverage|decisions))?$/);
  if (workbench) return {workbench: workbench[1] ?? "relationships", entryId: null, mode: null};
  if (!hash.startsWith("#") || hash.length < 2) return null;
  const parts = hash.slice(1).split("/");
  let entryId: string | null = null;
  if (parts[0].startsWith("entry-")) {
    entryId = parts.shift()!.slice("entry-".length);
    if (!validEntryId.test(entryId)) return null;
    if (!parts.length) return {workbench: null, entryId, mode: "2d" as AtlasMode};
  }
  const mode = Object.hasOwn(modeAliases, parts[0]) ? modeAliases[parts[0]] : undefined;
  if (!mode) return null;
  // Only the scroll reader has a photograph subview. Extra suffixes must not
  // silently become a different valid view (for example, history/photo).
  if (parts.length > 1 && !(mode === "scroll" && parts.length === 2 && parts[1] === "photo")) return null;
  return {workbench: null, entryId, mode};
}
