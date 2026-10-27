# Item 1: read the large Drive PDFs on the owner's Mac

Status 27 Oct 2026 14:30 Asia/Shanghai: **waiting** — the Mac was not connected to the bridge (get_device_info: not connected).

The Google Drive connector cannot download files over ~10 MB, so several decisive pages are unread although the files are in the owner's Drive. When the Mac is linked (Claude desktop app open), split these PDFs on the Mac and read only the listed pages.

| Needed for | File (Drive) | Pages / plates |
|---|---|---|
| Run 12 (earthquake fissure) | de Vaux 1973 Schweich Lectures (Drive 11OzY_YIp2g6TNCPtsBwxqFjXuh_7nsS_, 28 MB) | Pl. XXXIX with legend; Pl. XVI |
| Run 12, branch C | Magen & Peleg 2018 full report (Drive 1tUEpS4RUHFboNL7JkC8tDWk0V-ar4JuO) | pp. 58–66 (eastern dump) |
| Runs 9, 11 | Netzer 2001 *Palaces* (1rfYz5Zj16UbaDcDrZy9B94l630-z8jND) | Herodium and Jerusalem chapters (pdf pp. > 98) |
| Run 11 | Netzer 2001 *Jericho Final Reports* I | folded Plans 1, 2, 9, 14, 24, 26 |
| Run 11 | Zertal & Bar 2019 MHCS 5 (1vcVnFMLwLEKJTmbY5DQj8RIBkFUvRS52) | Sites 47–161, esp. Site 139 (Villa ʿAujah) |
| Run 1 | Feldman 1974 (Hyrcania) | plan p. 330 |
| Run 10 | Humbert, Chambon & Młynarczyk 2016 III A (166AvFtZ7bZN26cZ8fdjbf9CdfelFA8JZ) | 7Q–10Q plans |

Method: device_bash on the Mac with `pdfseparate`/`pdftoppm` (or Python), write page images to a scratch subfolder of a connected folder, stage only those pages here. Plates are viewed for measurement only and are not committed. **Do not** open DJD III plates or any column XII image (reserved).
