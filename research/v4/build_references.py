"""Generate IEEE reference entries from the verified primary-source metadata."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
METADATA = {x["doi"]: x for x in json.loads((HERE.parent / "literature/DOI_METADATA.json").read_text())}
ENTRIES = [
    ("guelman", "10.1109/TAES.2004.1386877", 2004),
    ("cai", "10.1016/j.ifacol.2020.12.1519", 2020),
    ("mai", "10.1016/j.optcom.2022.128963", 2023),
    ("cheong", "10.1109/ACC.2014.6859400", 2014),
    ("palmer", "10.1016/j.isatra.2019.02.034", 2019),
    ("guo", "10.1016/j.automatica.2023.111194", 2023),
    ("massa", "10.1016/j.conengprac.2024.106118", 2024),
    ("safees", "10.1109/TAC.2024.3469785", 2025),
    ("yan", "10.1016/j.optcom.2026.133342", 2026),
    ("es", "10.1016/S0005-1098(99)00183-1", 2000),
    ("cao", "10.1109/TCYB.2023.3331971", 2024),
    ("kalman", "10.1115/1.3662552", 1960),
    ("baeck", "10.1016/j.optcom.2024.130419", 2024),
    ("actuators", "10.3390/aerospace11010005", 2024),
]


def tex(s):
    for a, b in (("&", r"\&"), ("_", r"\_"), ("%", r"\%"), ("#", r"\#")):
        s = s.replace(a, b)
    return s


def entry(key, doi, year):
    m = METADATA[doi]
    assert m["status"].startswith("verified"), doi
    authors = []
    for a in m.get("authors", []):
        initials = " ".join(x[0] + "." for x in a.get("given", "").split() if x)
        authors.append(initials + " " + a["family"])
    who = ", ".join(authors[:4]) + (r" \emph{et al.}" if len(authors) > 4 else "")
    if key == "guelman":
        who = r"M. Guelman \emph{et al.}"
    title = tex(m["title"][0]);venue = tex(m["journal"][0])
    parts = [who + ", ``" + title + ",'', "]
    parts = [who + ", ``" + title + ",'' " + r"\emph{" + venue + "}"]
    if m.get("volume"):
        parts.append("vol. " + str(m["volume"]))
    if m.get("issue"):
        parts.append("no. " + str(m["issue"]))
    if m.get("page"):
        p = str(m["page"])
        parts.append(("pp. " if "-" in p else "Art. no. ") + p.replace("-", "--"))
    parts.append(str(year))
    parts.append(r"doi: \href{https://doi.org/" + doi + r"}{\nolinkurl{" + doi + "}}")
    return r"\bibitem{" + key + "} " + ", ".join(parts) + "."


out = [r"\begin{thebibliography}{99}"]
for key, doi, year in ENTRIES:
    if key == "kalman":
        out.append(r"\bibitem{source} Satellite-Optical-Fault-Recovery, source terminal model and V2 implementation, local archived snapshot \texttt{0bc453ffa0ad}. \href{https://github.com/kaushalrog/Satellite-Optical-Fault-Recovery}{Source repository}; accessed Oct. 23, 2026.")
    out.append(entry(key, doi, year))
out += [
    r"\bibitem{nasa} NASA Small Spacecraft Systems Virtual Institute, ``State-of-the-art small spacecraft technology: Communications.'' \href{https://www.nasa.gov/smallsat-institute/sst-soa/soa-communications/}{NASA communications overview}; accessed Oct. 23, 2026.",
    r"\bibitem{aipolicy} IEEE Author Center, ``Submission and peer review policies: Use of AI by authors.'' \href{https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/}{IEEE policy}; accessed Oct. 23, 2026.",
    r"\end{thebibliography}",
]
(HERE / "references.tex").write_text("\n".join(out) + "\n")
print("Generated 17 references; 14 DOI entries verified against recorded metadata.")
