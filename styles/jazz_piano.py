from mido import MidiFile, MidiTrack, Message, MetaMessage
import random
from styles.config import JazzConfig

class JazzPianoStyle:
    def __init__(self, state, config: JazzConfig = JazzConfig()):
        self.config = config
        self.bpm = random.choice(self.config.bpms)
        self.root = random.choice(self.config.roots)
        template = random.choice(self.config.chord_templates)

        # Randomly assign chord qualities
        qualities = random.choices(list(self.config.chord_intervals.keys()), k=len(template))

        # Generate progression using voiced chords
        self.progressions = [
            self.voice_chord(self.root + chord[0], quality=qualities[i], config=self.config)
            for i, chord in enumerate(template)
        ]

    def voice_chord(self, root, quality="maj7", inversion=0, octave_shift=0, config=None):
        """
        Return a voiced chord (list of MIDI note numbers) based on root and chord quality.
        """
        chord_intervals = (config or self.config).chord_intervals
        intervals = chord_intervals.get(quality, chord_intervals["maj7"])
        notes = [root + i for i in intervals]

        # Apply inversion
        for _ in range(inversion):
            notes = notes[1:] + [notes[0] + 12]

        # Apply octave shift
        notes = [n + octave_shift for n in notes]
        return notes

    def play_chord(self, track, chord, ticks, measure_index):
        delay = random.choice([0, int(ticks / 8), int(ticks / 4)])
        time_accum = delay

        velocities = [
            random.randint(60, 90) if measure_index % 2 == 0 else random.randint(45, 70)
            for _ in chord
        ]

        for i, note in enumerate(chord):
            track.append(Message('note_on', note=note, velocity=velocities[i], channel=0, time=time_accum if i == 0 else 0))
            time_accum = 0

        duration = random.choice([ticks, int(ticks * 1.5)])
        track.append(Message('note_off', note=chord[0], velocity=64, channel=0, time=duration))
        for note in chord[1:]:
            track.append(Message('note_off', note=note, velocity=64, channel=0, time=0))
    

    def next_song(self, measures: int) -> MidiFile:
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        tempo = int(60_000_000 / self.bpm)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        track.append(Message('program_change', program=0, channel=0, time=0))

        ticks = mid.ticks_per_beat

        for i in range(measures):
            chord = self.progressions[i % len(self.progressions)]
            track.append(Message('control_change', control=64, value=127, time=0))  # pedal down
            self.play_chord(track, chord, ticks, i)
            track.append(Message('control_change', control=64, value=0, time=ticks))  # pedal up

        return mid