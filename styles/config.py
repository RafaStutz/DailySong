from dataclasses import dataclass, field

@dataclass(frozen=True)
class JazzConfig:
    """
    Static configuration,
    includes BPMs, roots, simple progressions, and chord voicing intervals.
    """
    bpms: list[int] = field(default_factory=lambda: [60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110])
    roots: list[int] = field(default_factory=lambda: [60, 62, 65, 67, 69, 72])  # C, D, F, G, A, C'
    progressions: list[list[int]] = field(default_factory=lambda: [
        # I - IV - V - I
        [0, 5, 7, 0],

        # I - vi - IV - V
        [0, 9, 5, 7],

        # I - ii - IV - V
        [0, 2, 5, 7],

        # I - V - IV - I
        [0, 7, 5, 0],

        # i - III - IV - V (minor-leaning)
        [0, 3, 5, 7],
    ])
    qualities: list[str] = field(default_factory=lambda: ["maj7", "m7", "7"])
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
