from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts.t25_verify import main

if __name__ == "__main__":
    raise SystemExit(main())
