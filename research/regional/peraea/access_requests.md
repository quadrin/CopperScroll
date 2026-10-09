# Access to MEGA-Jordan and EAMENA: how to request it, and draft requests

Prepared 9 October 2026 UTC. Nothing was sent and no account was created. No login page or form was used. The drafts below are for the owner to review and send himself if he wishes. Both databases would supply the unit inventory that a count east of the Jordan needs ([PREREG_DRAFT_R3.md](PREREG_DRAFT_R3.md) §5).

## MEGA-Jordan (Department of Antiquities of Jordan)

What it is (EVIDENCE):
- The national GIS inventory of Jordan's archaeological sites, built by the Getty Conservation Institute and World Monuments Fund for the Department of Antiquities (DoA), launched in April 2011. It holds the legacy JADIS data on over 10,400 sites plus newer records (Myers and Dalgity 2012, p. 49; article PDF at https://media.getty.edu/Text/94b3d9e2-4d29-55f3-b15a-2375e1d99868.pdf, SHA-256 `eaa4ee4c6dac09da07a9a22dc4da2cffc51b612f92841ebb5ddd5fd6ff591c1a`).
- "The system allows the DoA to assign various levels of access" by role; some users may only search and view (same, p. 41).
- Day-to-day management, "including managing user access", lies with the MEGA-Jordan Unit under the DoA's Studies and Publication Directorate (same, p. 49).
- The same article says that in 2011 the DoA made the system "fully viewable on the Internet by the general public" (p. 49).

What the web site shows (EVIDENCE, 9 October 2026):
- http://megajordan.org/ opens over plain HTTP. It shows a single "Guest Access" button rendered by JavaScript, with tutorials. I did not press it: it is a login control. The HTTPS address (https://megajordan.org/) failed with "connection reset by peer".
- The DoA web site lists MEGA JORDAN among "databases useful to researchers" (https://www.doa.gov.jo/Ar/List/قواعد_البيانات), with no account procedure stated.
- DoA contact page (https://www.doa.gov.jo/Ar/Pages/اتصل_بنا): Jabal Amman, Third Circle, ʿAbd al-Munʿim al-Rifaʿi Street, building 21; P.O. Box 88, Amman 11118; telephone +962 6 464 4336; fax +962 6 461 5848; the page gives a general e-mail address (Info-DoA at doa.gov.jo).

How a researcher requests access (INFERENCE from the above): write to the DoA, addressed to the MEGA-Jordan Unit, Studies and Publication Directorate, through the general contact address, and ask for a read-only research account. Conditions are not published. The article says accounts are role-based and that the DoA coordinates data with academic institutions; expect to state affiliation, purpose and region, and to cite the DoA in any output. A person with a browser could also check whether "Guest Access" gives a public read-only view without an account (the 2012 article implies it does); that is a decision for the owner, because it is a login control.

Draft (for the owner; edit freely):

> Subject: Request for read-only research access to MEGA-Jordan
>
> Dear colleagues of the MEGA-Jordan Unit, Studies and Publication Directorate,
>
> I am an independent researcher working on the topography of the Copper Scroll from Qumran (3Q15). I am compiling a list of settlements of the Hellenistic and Early Roman periods east of the Jordan, from the Yarmuk to Wadi al-Mujib, within about 40 km of the river, and their recorded water installations and tombs. The work is desk-based and non-commercial; I will not publish precise coordinates of unprotected sites.
>
> Could the Department grant me read-only access to MEGA-Jordan for this region, or tell me how to apply? I would be glad to follow any conditions and to cite the Department and MEGA-Jordan in all results.
>
> With thanks and best regards,
> Alex Kesin

## EAMENA (Endangered Archaeology in the Middle East and North Africa)

Access levels (EVIDENCE, https://eamena.org/open-access-policy, read 9 October 2026):
- **Public Access**: self-registration with a password gives immediate access, "but without coordinates, the zoom function on the map, or to site condition data".
- **Research Access**: a registration form that asks about the planned research and institutional affiliation; EAMENA checks only "that the applicant has a genuine research interest".
- **Contributor Access**: for adding data; by e-mail to the project.

How to apply for Research Access (EVIDENCE, https://eamena.org/database-registration-form and https://eamena.org/eamenamarea-database-registration-form-0):
- Fill in the EAMENA/MarEA Database Registration Form. Required fields: first name, surname, e-mail address, institutional affiliation ("to confirm your research status"), research planned ("cultural periods, geographical regions, or topics"), and agreement to the General Terms and Conditions.
- Terms (summary): the user must contact the relevant Department of Antiquities before using or publishing EAMENA data; Researcher Access is view-only; acknowledgement of EAMENA or MarEA is required in every output; data are under CC BY 4.0; access can be withdrawn if the terms are broken; publications should be reported to EAMENA.
- Questions go to the project e-mail given on the form page (eamena at arch.ox.ac.uk).
- The database itself is at https://database.eamena.org (Arches 7). I did not open it.

Draft answers for the form (for the owner):

> Institutional affiliation: Independent researcher (Copper Scroll research project, quadrin/CopperScroll on GitHub).
>
> Research planned: Hellenistic and Early Roman (about 150 BCE - 135 CE) settlements in Jordan between the Yarmuk and Wadi al-Mujib, within about 40 km east of the Jordan river and the Dead Sea. I need site records with periods, water installations (pools, cisterns, channels), caves and tombs, and their positions, to test how common a combination of features described in the Copper Scroll (3Q15) is in that region. Desk-based, non-commercial. I will contact the Department of Antiquities of Jordan before publishing, cite EAMENA as required, and not publish precise coordinates.

## Notes

- Myers, D. and Dalgity, A. 2012. "The Middle Eastern Geodatabase for Antiquities (MEGA): An Open Source GIS-Based Heritage Site Inventory and Management System." Journal article, printed pp. 32-57, PDF hosted by the Getty (URL and SHA-256 above). It was read only for the access question, so it is not in sources.csv.
- Neither database was logged into, and no form was submitted.
