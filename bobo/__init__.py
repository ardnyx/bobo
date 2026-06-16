"""
bobo — zero-config grid algorithm visualizer.

Quick start (CLI — no code changes needed)::

    $ bobo your_algorithm.py

Manual API (for fine-grained control)::

    from bobo import bobo

    bobo.configure(mapping={0: "\\033[90m · \\033[0m"}, delay=0.3)
    bobo.show(grid, message="Step info")
"""

from .visualizer import BoboVisualizer

# Singleton instance for backward-compatible manual API.
# Usage:  from bobo import bobo
bobo = BoboVisualizer()

__all__ = ["bobo", "BoboVisualizer"]
__version__ = "2.0.0"
