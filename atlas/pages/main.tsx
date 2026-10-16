// Static entry for GitHub Pages: renders the same Atlas component as app/page.tsx,
// without the Next.js/vinext server shell used by the ChatGPT-hosted Site.
import "../app/globals.css";
import { createRoot } from "react-dom/client";
const root=createRoot(document.getElementById("root")!);
import("../app/atlas-home").then(({default:AtlasHome})=>root.render(<AtlasHome />)).catch(()=>{
  root.render(<main className="atlas-startup" role="alert"><p>The atlas could not load.</p><button onClick={()=>location.reload()}>Reload atlas</button></main>);
});
