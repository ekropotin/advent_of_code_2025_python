from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Set, Tuple


Coord = Tuple[int, int]


@dataclass(frozen=True)
class Shape:
    index: int
    cells: Set[Coord]

    def get_all_placements(self, width: int, height: int) -> List[int]:
        """
        Get all unique ways this shape can be placed on a width x height board.
        Returns placements as bitmasks (each bit represents a cell on the board).
        """
        placements = set()

        # Try all 8 transformations (4 rotations × 2 flips)
        for flip_x in [False, True]:
            for rotations in range(4):
                variant = self._transform_shape(flip_x, rotations)
                placements.update(self._place_variant(variant, width, height))

        return sorted(placements)

    def _transform_shape(self, flip_x: bool, rotations: int) -> Set[Coord]:
        """Apply flip and rotation transformations, then normalize to (0,0)."""
        transformed = set()

        for x, y in self.cells:
            # Flip horizontally if needed
            if flip_x:
                x = -x
            # Rotate 90 degrees clockwise `rotations` times
            for _ in range(rotations):
                x, y = -y, x
            transformed.add((x, y))

        # Normalize to start at (0, 0)
        min_x = min(x for x, y in transformed)
        min_y = min(y for x, y in transformed)
        return {(x - min_x, y - min_y) for x, y in transformed}

    def _place_variant(self, variant: Set[Coord], width: int, height: int) -> Set[int]:
        """Generate all valid positions for a shape variant as bitmasks."""
        placements = set()

        # Find variant bounds
        max_x = max(x for x, y in variant)
        max_y = max(y for x, y in variant)

        # Try all positions where the shape fits
        for offset_y in range(height - max_y):
            for offset_x in range(width - max_x):
                # Convert this placement to a bitmask
                mask = 0
                for x, y in variant:
                    cell_index = (offset_y + y) * width + (offset_x + x)
                    mask |= 1 << cell_index
                placements.add(mask)

        return placements


def parse_input(text: str) -> Tuple[List[Shape], List[Tuple[int, int, List[int]]]]:
    """Parse shapes and region requirements from input text."""
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]

    shapes = []
    regions = []
    i = 0

    # Parse shapes section (until we hit a line with "WxH:")
    while i < len(lines):
        line = lines[i]

        # Check if we've reached the regions section
        if "x" in line and ":" in line:
            parts = line.split(":")[0].strip()
            if "x" in parts and all(p.isdigit() for p in parts.split("x")):
                break

        # Parse shape header (e.g., "0:")
        if ":" in line and line.split(":")[0].strip().isdigit():
            shape_idx = int(line.split(":")[0])
            i += 1

            # Collect shape grid lines
            shape_lines = []
            while i < len(lines):
                next_line = lines[i]
                # Stop if we hit another shape header or region line
                if ":" in next_line and (
                    next_line.split(":")[0].strip().isdigit()
                    or "x" in next_line.split(":")[0]
                ):
                    break
                shape_lines.append(next_line)
                i += 1

            # Extract cells marked with '#'
            cells = {
                (x, y)
                for y, row in enumerate(shape_lines)
                for x, char in enumerate(row)
                if char == "#"
            }
            shapes.append(Shape(shape_idx, cells))
        else:
            i += 1

    # Parse regions section
    while i < len(lines):
        line = lines[i]
        i += 1

        if ":" in line:
            size_part, counts_part = line.split(":", 1)
            width, height = map(int, size_part.strip().split("x"))
            counts = list(map(int, counts_part.split()))
            regions.append((width, height, counts))

    return shapes, regions


def can_fit_presents(
    width: int, height: int, shapes: List[Shape], counts: List[int]
) -> bool:
    """
    Determine if all required presents can fit in the region using backtracking.
    Uses "most constrained first" heuristic for efficiency.
    """

    # Quick rejection: check total area
    total_area = sum(count * len(shape.cells) for count, shape in zip(counts, shapes))
    if total_area > width * height:
        return False

    # Empty case
    if sum(counts) == 0:
        return True

    # Precompute all possible placements for each shape
    all_placements = [shape.get_all_placements(width, height) for shape in shapes]

    # Convert to tuple for hashing in memoization
    all_placements_tuple = tuple(tuple(p) for p in all_placements)

    @lru_cache(maxsize=None)
    def backtrack(occupied: int, remaining: Tuple[int, ...]) -> bool:
        """
        Try to place all remaining presents using backtracking.

        Args:
            occupied: Bitmask of occupied cells on the board
            remaining: Tuple of remaining count for each shape type

        Returns:
            True if all remaining presents can be placed
        """
        # Base case: all presents placed
        if all(count == 0 for count in remaining):
            return True

        # Choose shape with fewest valid placements (most constrained first)
        best_shape_idx = None
        best_valid_placements = None

        for shape_idx, count in enumerate(remaining):
            if count == 0:
                continue

            # Find placements that don't overlap with occupied cells
            valid_placements = [
                placement
                for placement in all_placements_tuple[shape_idx]
                if not (placement & occupied)  # No overlap
            ]

            # Pruning: if any required shape has no valid placements, fail
            if not valid_placements:
                return False

            # Track the most constrained shape
            if best_valid_placements is None or len(valid_placements) < len(
                best_valid_placements
            ):
                best_valid_placements = valid_placements
                best_shape_idx = shape_idx

        # Try each valid placement for the most constrained shape
        new_remaining = list(remaining)
        new_remaining[best_shape_idx] -= 1

        for placement in best_valid_placements:
            if backtrack(occupied | placement, tuple(new_remaining)):
                return True

        return False

    return backtrack(0, tuple(counts))


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    shapes, regions = parse_input(input_path.read_text())

    res = 0
    for width, height, counts in regions:
        if can_fit_presents(width, height, shapes, counts):
            res += 1

    return res


if __name__ == "__main__":
    main()
