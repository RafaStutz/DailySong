from mido import MidiFile, MidiTrack, Message, MetaMessage
import random
from styles.config import JazzConfig

class JazzPianoStyle:
    def __init__(self, state, config: JazzConfig = JazzConfig()):
        self.config = config
        self.bpm = random.choice(self.config.bpms)
        self.root = random.choice(self.config.roots)
        template = random.choice(self.config.chord_templates)
        self.progressions = [
            [self.root + interval for interval in chord]
            for chord in template
        ]

    def next_song(self, measures: int) -> MidiFile:
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # tempo defined via MetaMessage
        tempo = int(60_000_000 / self.bpm)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        track.append(Message('program_change', program=0, channel=0, time=0))  # Piano

        ticks = mid.ticks_per_beat
        long_tick = int((2 / 3) * ticks)
        short_tick = ticks - long_tick

        for i in range(measures):
            chord = self.progressions[i % len(self.progressions)]
            for note in chord:
                vel = random.randint(50, 70)
                track.append(Message('note_on', note=note, velocity=vel, channel=0, time=0))
                track.append(Message('note_off', note=note, velocity=vel, channel=0, time=long_tick))
                track.append(Message('note_on', note=note, velocity=0, channel=0, time=short_tick))

        return mid