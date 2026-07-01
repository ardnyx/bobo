"""Allow running bobo as a module: python -m bobo <script>"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())