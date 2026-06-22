import argparse
import os
import sys

from .visualizer import BoboVisualizer
from .tracer import BoboTracer

_SPEED_PRESETS = {
    "slow":   1.0,
    "normal": 0.5,
    "fast":   0.1,
    "turbo":  0.01,
}

def _build_parser():
    parser = argparse.ArgumentParser(
        prog="bobo",
        description=(
            "Visualize grid-based algorithms automatically. "
        ),
        epilog="Example:  bobo bfs.py --speed fast",
    )

    parser.add_argument(
        "script",
        help="Path to the Python script to visualize.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=None,
        help="Seconds to pause between frames (default: 0.5). "
             "Overrides --speed if both are given.",
    )

    parser.add_argument(
        "--speed",
        choices=list(_SPEED_PRESETS.keys()),
        default="normal",
        help="Preset animation speed (default: normal). "
             "slow=1s, normal=0.5s, fast=0.1s, turbo=0.01s.",
    )

    parser.add_argument(
        "--var",
        default=None,
        metavar="NAME",
        help="Only track a specific variable name (e.g., --var dp). "
             "By default, all detected grid variables are tracked.",
    )

    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Don't clear the terminal between frames. "
             "Useful for scrollback inspection.",
    )

    return parser

def main(argv=None):
    """CLI entry point. Called by ``bobo`` console script or ``python -m bobo``."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    script_path = os.path.abspath(args.script)
    if not os.path.isfile(script_path):
        parser.error(f"Script not found: {args.script}")

    if args.delay is not None:
        delay = args.delay
    else:
        delay = _SPEED_PRESETS[args.speed]

    viz = BoboVisualizer()
    viz.configure(
        delay=delay,
        clear_screen=not args.no_clear,
    )

    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()

    code = compile(source, script_path, "exec")

    script_dir = os.path.dirname(script_path)
    sys.path.insert(0, script_dir)

    original_argv = sys.argv
    sys.argv = [script_path]

    global_ns = {
        "__name__": "__main__",
        "__file__": script_path,
        "__builtins__": __builtins__,
    }

    tracer = BoboTracer(viz, target_file=script_path, var_filter=args.var)

    try:
        tracer.run(code, global_ns)
    except KeyboardInterrupt:
        print(f"\n\033[1;33m[bobo]\033[0m Visualization stopped.")
    except SystemExit:
        pass  
    finally:
        sys.argv = original_argv
        if script_dir in sys.path:
            sys.path.remove(script_dir)
