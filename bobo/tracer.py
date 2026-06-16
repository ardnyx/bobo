import sys
import os
import copy
from .detector import is_grid, auto_map, compute_cell_width

class BoboTracer:
    def __init__(self, visualizer, target_file, var_filter=None):
        self.visualizer = visualizer
        self.target_file = os.path.normcase(os.path.abspath(target_file))
        self.var_filter = var_filter
        self._snapshots = {}
        self._mapped_values = set()
        self._rendering = False

    def run(self, code_obj, global_ns):
        sys.settrace(self._trace)
        try:
            exec(code_obj, global_ns)
        finally:
            sys.settrace(None)
    def _trace(self, frame, event, arg):
        if self._rendering:
            return None

        frame_file = os.path.normcase(os.path.abspath(frame.f_code.co_filename))
        if frame_file != self.target_file:
            return None
        if event in ('line', 'return'):
            self._check_grids(frame)

        return self._trace
    def _check_grids(self, frame):
        variables = dict(frame.f_globals)
        variables.update(frame.f_locals)

        for name, value in variables.items():
            if name.startswith('_'):
                continue
            if not isinstance(value, list):
                continue
            if self.var_filter and name != self.var_filter:
                continue
            if not is_grid(value):
                continue
            prev = self._snapshots.get(name)
            if prev is not None and prev == value:
                continue

            changed_cells = self._diff_cells(prev, value) if prev is not None else []
            self._snapshots[name] = copy.deepcopy(value)
            self._ensure_mapped(value)
            func_name = frame.f_code.co_name
            line_no = frame.f_lineno

            if func_name == '<module>':
                message = f"'{name}' changed  (line {line_no})"
            else:
                message = f"'{name}' changed in {func_name}()  (line {line_no})"

            self._rendering = True
            try:
                self.visualizer.show(value, message=message, highlights=changed_cells)
            finally:
                self._rendering = False
    @staticmethod
    def _diff_cells(old, new):
        changed = []
        old_rows, new_rows = len(old), len(new)
        shared_rows = min(old_rows, new_rows)

        for r in range(shared_rows):
            old_cols = len(old[r])
            new_cols = len(new[r])
            shared_cols = min(old_cols, new_cols)

            for c in range(shared_cols):
                if old[r][c] != new[r][c]:
                    changed.append((r, c))
            for c in range(shared_cols, new_cols):
                changed.append((r, c))
        for r in range(shared_rows, new_rows):
            for c in range(len(new[r])):
                changed.append((r, c))

        return changed
    def _ensure_mapped(self, grid):
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
