"""Allow running via ``python -m focusflow``."""

import sys

from .app import run

if __name__ == "__main__":
    sys.exit(run())
