// Static entry for GitHub Pages: renders the same Atlas component as app/page.tsx,
// without the Next.js/vinext server shell used by the ChatGPT-hosted Site.
import "../app/globals.css";
import { createRoot } from "react-dom/client";
import AtlasHome from "../app/atlas-home";

createRoot(document.getElementById("root")!).render(<AtlasHome />);
