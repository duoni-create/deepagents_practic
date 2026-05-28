from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from ecommerce.project import main
else:
    from .project import main


if __name__ == "__main__":
    main()
