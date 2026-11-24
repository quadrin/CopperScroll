export const siloamReadings = ["outlet-siloam", "displayed-baths", "water-closet-jehu"] as const;
export type SiloamReading = typeof siloamReadings[number];
export const siloamSubjects = ["tunnel-mouth", "stepped-basin", "receiver", "conduit"] as const;
export type SiloamSubject = typeof siloamSubjects[number];

export function isSiloamReading(value: unknown): value is SiloamReading {
  return siloamReadings.some(id => id === value);
}
export function isSiloamSubject(value: unknown): value is SiloamSubject {
  return siloamSubjects.some(id => id === value);
}
export const defaultSubject: Record<SiloamReading, SiloamSubject> = {
  "outlet-siloam": "tunnel-mouth",
  "displayed-baths": "stepped-basin",
  "water-closet-jehu": "receiver",
};
export const subjectFeature: Record<SiloamSubject, string | null> = {
  "tunnel-mouth": null, "stepped-basin": null, receiver: "L102", conduit: "L103",
};
