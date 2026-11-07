"""Compile the supplied final paper, or a separate paper for a fresh run tag."""
import re
import subprocess
import sys
from pathlib import Path
here = Path(__file__).resolve().parent
tag = sys.argv[1] if len(sys.argv) > 1 else "final"
assert re.fullmatch(r"[A-Za-z0-9_-]+", tag), "Use a plain experiment tag"
subprocess.run([sys.executable, str(here / "build_references.py")], check=True)
target = here / "paper.tex"
if tag != "final":
    target = here / f"paper_{tag}.tex"
    target.write_text((here / "paper.tex").read_text().replace("results/final", f"results/{tag}"))
subprocess.run(["tectonic", "--keep-logs", target.name], cwd=here, check=True)
