from dataclasses import dataclass, field

@dataclass(frozen=True)
class JazzConfig:
    """
    Static configuration,
    includes BPMs, roots, chord progressions, and chord voicing intervals.
    """
    bpms: list[int] = field(default_factory=lambda: [60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110])
    roots: list[int] = field(default_factory=lambda: [60, 62, 65, 67, 69, 72])  # C, D, F, G, A, C'
    chord_templates: list[list[list[int]]] = field(default_factory=lambda: [
         # Extended II–V–I in major
        [[2, 5, 9, 12], [7, 11, 14, 17], [0, 4, 7, 11], [5, 9, 12, 16], [0, 4, 7, 11]],

        # I – vi – ii – V loop (classic jazz)
        [[0, 4, 7, 11], [9, 12, 16, 19], [2, 5, 9, 12], [7, 11, 14, 17],
         [0, 4, 7, 11], [9, 12, 16, 19], [2, 5, 9, 12], [7, 11, 14, 17]],

        # Modal jazz loop (e.g., So What)
        [[0, 3, 7, 10], [2, 5, 9, 12], [5, 8, 12, 15], [7, 10, 14, 17]],

        # Tritone subs
        [[2, 5, 9, 12], [6, 10, 13, 16], [0, 4, 7, 11], [6, 10, 14, 17]],

        # Descending chromatic root motion
        [[0, 4, 7, 11], [-1, 3, 6, 10], [-2, 2, 5, 9], [-3, 1, 4, 8],
         [-4, 0, 3, 7], [-5, 11, 2, 6]],

        # Circle of fifths
        [[0, 4, 7, 10], [5, 9, 0, 2], [10, 2, 5, 7], [3, 7, 10, 0], [8, 0, 3, 5]],

        # Minor turnaround with chromaticism
        [[0, 3, 7, 10], [11, 2, 6, 9], [10, 1, 5, 8], [9, 0, 4, 7]]
    ])
    chord_intervals: dict[str, list[int]] = field(default_factory=lambda: {
        "maj7":  [0, 4, 7, 11],        
        "m7":    [0, 3, 7, 10],        
        "7":     [0, 4, 7, 10],       
        "m7b5":  [0, 3, 6, 10],        
        "dim7":  [0, 3, 6, 9],
        "min6":  [0, 3, 7, 9],  
        "maj6":  [0, 4, 7, 9],       
        "sus4":  [0, 5, 7, 10],       
        "add9":  [0, 4, 7, 14],        
    })
