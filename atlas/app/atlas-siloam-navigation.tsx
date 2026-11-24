"use client";
import { createContext, useContext, type ReactNode } from "react";
import type { ExplorerState } from "./atlas-explorer-model";
import { defaultSubject, subjectFeature, type SiloamReading, type SiloamSubject } from "./atlas-siloam-reading";

type SiloamState = {
  reading?: SiloamReading;
  subject?: SiloamSubject;
  mapHref: string; scrollHref: string;
  select: (reading: SiloamReading) => void;
  inspect: (subject?: SiloamSubject) => void;
  read: () => void;
};
const SiloamContext = createContext<SiloamState | null>(null);
export const useSiloamNavigation = () => useContext(SiloamContext);

export default function SiloamNavigation({state, navigate, children}: {
  state: ExplorerState;
  navigate: (patch: Partial<ExplorerState>, replace?: boolean) => void;
  children: ReactNode;
}) {
  const reading = state.siloamReading ?? "outlet-siloam";
  const subject = state.siloamSubject ?? defaultSubject[reading];
  const params = new URLSearchParams({reading, subject});
  const feature = state.featureId ?? subjectFeature[subject];
  const scrollParams = new URLSearchParams(params);
  if (state.featureId) scrollParams.set("feature", state.featureId);
  const context: SiloamState = {
    mapHref: `#entry-49/site/siloam-receiver/${feature ? feature + "/" : ""}source?${params}`,
    scrollHref: `#entry-49/scroll?${scrollParams}`,
    reading: state.siloamReading, subject,
    select(next) {
      if (next !== state.siloamReading) navigate({siloamReading: next, siloamSubject: defaultSubject[next], featureId: null}, true);
    },
    inspect(next = subject) {
      const unmodified = next === state.siloamSubject && state.featureId;
      navigate({mode: "site", entryId: "49", placeId: "jer_siloam", planId: "siloam-receiver", siteView: "plan", representation: "source",
        siloamReading: reading, siloamSubject: next, featureId: unmodified || subjectFeature[next],
        inspection: null, workbench: null, recordId: null, explicitPlace: false, scrollPhoto: false, scroll3d: false});
    },
    read() {
      navigate({mode: "scroll", entryId: "49", siloamReading: reading, siloamSubject: subject, scrollColumn: undefined,
        scrollPhoto: false, scroll3d: false, inspection: null, workbench: null, recordId: null});
    },
  };
  return <SiloamContext.Provider value={state.entryId === "49" ? context : null}>{children}</SiloamContext.Provider>;
}
