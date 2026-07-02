"""
Runtime tracer — watches a script's execution and visualises grid changes,
auxiliary coordinate structures, cursor movement, and backtracking.
"""

import sys
import os
import copy

from .detector import (
    is_grid, auto_map, compute_cell_width,
    detect_coord_collections, detect_cursors, classify_changes,
)


class BoboTracer:
    """Automatic grid-change tracer using ``sys.settrace``.

    On every line of the target script the tracer:
    1. Scans locals + globals for 2-D list variables (grids).
    2. For each grid, detects auxiliary coordinate collections
       (``visited``, ``queue``, etc.) and cursor-pair variables.
    3. Compares the combined state against the previous snapshot.
    4. If anything visual changed, renders through the visualiser.
    """

    def __init__(self, visualizer, target_file, var_filter=None):
        self.visualizer = visualizer
        self.target_file = os.path.normcase(os.path.abspath(target_file))
        self.var_filter = var_filter

        # Per-grid-name tracking:
        self._grid_snapshots = {}          # name -> deep-copied grid
        self._aux_state = {}               # name -> {aux_name: length}
        self._cursor_state = {}            # name -> [(r, c), ...]
        self._mapped_values = set()        # all values seen so far
        self._rendering = False            # re-entrancy guard
        self._prev_depth = {}              # name -> last recursion depth

    # -- Public API -----------------------------------------------------------

    def run(self, code_obj, global_ns):
        """Execute *code_obj* with tracing enabled."""
        sys.settrace(self._trace)
        try:
            exec(code_obj, global_ns)
        finally:
            sys.settrace(None)

    # -- Trace callback -------------------------------------------------------

    def _trace(self, frame, event, arg):
        if self._rendering:
            return None

        frame_file = os.path.normcase(os.path.abspath(frame.f_code.co_filename))
        if frame_file != self.target_file:
            return None

        if event in ('line', 'return'):
            self._check_state(frame)

        return self._trace

    # -- Core state check -----------------------------------------------------

    def _check_state(self, frame):
        """Scan all variables for grids, overlays, and cursors."""
        variables = dict(frame.f_globals)
        variables.update(frame.f_locals)

        # 1. Find all grids
        grids = {}
        for name, value in variables.items():
            if name.startswith('_'):
                continue
            if not isinstance(value, list):
                continue
            if self.var_filter and name != self.var_filter:
                continue
            if is_grid(value):
                grids[name] = value

        if not grids:
            return

        # 2. For each grid, detect overlays + cursors and check for changes
        for grid_name, grid_value in grids.items():
            max_rows = len(grid_value)
            max_cols = len(grid_value[0])

            # Detect auxiliary coordinate collections
            exclude = set(grids.keys())
            aux = detect_coord_collections(variables, max_rows, max_cols, exclude)

            # Detect cursor pairs
            cursors = detect_cursors(variables, max_rows, max_cols)

            # -- Quick change detection --
            prev_grid = self._grid_snapshots.get(grid_name)
            grid_changed = prev_grid is None or prev_grid != grid_value

            aux_lens = {k: len(v) for k, v in aux.items()}
            aux_changed = aux_lens != self._aux_state.get(grid_name, {})

            cursor_pos = [(rv, cv) for _, _, rv, cv in cursors]
            cursor_changed = cursor_pos != self._cursor_state.get(grid_name, [])

            if not grid_changed and not aux_changed and not cursor_changed:
                continue   # nothing visual changed

            # -- Something changed — update snapshots --

            fwd, bwd, other = [], [], []
            if grid_changed:
                if prev_grid is not None:
                    fwd, bwd, other = classify_changes(prev_grid, grid_value)
                self._grid_snapshots[grid_name] = copy.deepcopy(grid_value)
                self._ensure_mapped(grid_value)

            self._aux_state[grid_name] = aux_lens
            self._cursor_state[grid_name] = cursor_pos

            # Recursion depth
            depth = self._get_depth(frame)
            prev_depth = self._prev_depth.get(grid_name, 1)
            self._prev_depth[grid_name] = depth

            # Build message
            func_name = frame.f_code.co_name
            line_no = frame.f_lineno
            if func_name == '<module>':
                msg = f"'{grid_name}'  (line {line_no})"
            else:
                msg = f"'{grid_name}' in {func_name}()  (line {line_no})"

            # -- Render --
            self._rendering = True
            try:
                self.visualizer.show(
                    grid_value,
                    message=msg,
                    aux_overlays=aux,
                    cursors=cursors,
                    forward_cells=fwd,
                    backward_cells=bwd,
                    changed_cells=other,
                    recursion_depth=depth,
                )
            finally:
                self._rendering = False

    # -- Helpers --------------------------------------------------------------

    def _get_depth(self, frame):
        """Count how many target-file frames are on the call stack."""
        depth = 0
        f = frame
        while f is not None:
            if os.path.normcase(os.path.abspath(f.f_code.co_filename)) == self.target_file:
                depth += 1
            f = f.f_back
        return depth

    def _ensure_mapped(self, grid):
        """Auto-map any new cell values that we haven't seen before."""
        needs_remap = False
        for row in grid:
            for cell in row:
                if cell not in self._mapped_values:
                    needs_remap = True
                    self._mapped_values.add(cell)
        if needs_remap:
            new_mapping = auto_map(grid)
            cell_width = compute_cell_width(new_mapping)
            self.visualizer.configure(mapping=new_mapping, cell_width=cell_width)
