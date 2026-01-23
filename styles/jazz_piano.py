from mido import MidiFile, MidiTrack, Message, MetaMessage
import random
from styles.config import JazzConfig

class JazzPianoStyle:
    def __init__(self, config: JazzConfig = JazzConfig()):
        self.config = config
        self.bpm = random.choice(self.config.bpms)
        self.root = random.choice(self.config.roots)
        progression = random.choice(self.config.progressions)

        # Randomly assign chord qualities
        qualities = random.choices(self.config.qualities, k=len(progression))

        # Generate progression using voiced chords
        self.progression = [
            self.voice_chord(self.root + offset, quality=qualities[i])
            for i, offset in enumerate(progression)
        ]

    def voice_chord(self, root, quality="maj7"):
        """
        Return a voiced chord (list of MIDI note numbers) based on root and chord quality.
        """
        intervals = self.config.chord_intervals.get(quality, self.config.chord_intervals["maj7"])
        notes = [root + i for i in intervals]
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

    def play_melody(self, track, chord, ticks, beats_per_measure=4):
        note_duration = int(ticks * 0.75)
        rest = ticks - note_duration

        for beat in range(beats_per_measure):
            note = random.choice(chord) + 12
            velocity = random.randint(55, 85)
            track.append(Message('note_on', note=note, velocity=velocity, channel=1, time=0 if beat == 0 else rest))
            track.append(Message('note_off', note=note, velocity=64, channel=1, time=note_duration))
    

    def next_song(self, measures: int) -> MidiFile:
        mid = MidiFile()
        track = MidiTrack()
        melody = MidiTrack()
        mid.tracks.append(track)
        mid.tracks.append(melody)

        tempo = int(60_000_000 / self.bpm)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        track.append(Message('program_change', program=0, channel=0, time=0))
        melody.append(Message('program_change', program=0, channel=1, time=0))

        ticks = mid.ticks_per_beat

        for i in range(measures):
            chord = self.progression[i % len(self.progression)]
            track.append(Message('control_change', control=64, value=127, time=0))  # pedal down
            self.play_chord(track, chord, ticks, i)
            track.append(Message('control_change', control=64, value=0, time=ticks))  # pedal up
            self.play_melody(melody, chord, ticks)

        return mid
