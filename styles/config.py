from dataclasses import dataclass, field

@dataclass(frozen=True)
class JazzConfig:
    """
    Static configuration,
    includes BPMs, roots and chord progressions.
    """
    bpms: list[int] = field(default_factory=lambda: [60, 75, 90, 110, 120, 135, 150])
    roots: list[int] = field(default_factory=lambda: [60, 62, 65, 67, 69, 72])  # C, D, F, G, A, C'
    chord_templates: list[list[list[int]]] = field(default_factory=lambda: [
        # II-V-I
        [[2, 5, 9, 12], [7, 11, 14, 17], [0, 4, 7, 11]],
        # I-vi-ii-V
        [[0, 4, 7, 11], [9, 12, 16, 19], [2, 5, 9, 12], [7, 11, 14, 17]],
        # Blues
        [[0, 4, 7, 9], [5, 9, 12, 14], [0, 4, 7, 9], [7, 11, 14, 17]],
    ])