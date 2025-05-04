import json
import datetime
import math
from mido import MidiFile
from styles import JazzPianoStyle, JazzConfig

try:
    with open('state.json') as f:
        state = json.load(f)
except FileNotFoundError:
    state = {"min_duration_s": 120}

config = JazzConfig()
style = JazzPianoStyle(state, config)

beats_per_measure = 4
measures = math.ceil((state['min_duration_s'] * style.bpm) / (60 * beats_per_measure))

mid = style.next_song(measures)

today = datetime.date.today().isoformat()
filename = f"music/song_{today}_{style.bpm}bpm.mid"
mid.save(filename)