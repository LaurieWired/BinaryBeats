from pydub import AudioSegment
from pydub.generators import Sine
import simpleaudio as sa
import io
import time

c_major_notes = [
    'C0', 'D0', 'E0', 'F0', 'G0', 'A0', 'B0',
    'C1', 'D1', 'E1', 'F1', 'G1', 'A1', 'B1',
    'C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2',
    'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3',
    'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
    'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
    'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
    'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
    'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8'
]

b_minor_notes = [
    'B0', 'C#1/Db1', 'D1', 'E1', 'F#1/Gb1', 'G1', 'A1',
    'B1', 'C#2/Db2', 'D2', 'E2', 'F#2/Gb2', 'G2', 'A2',
    'B2', 'C#3/Db3', 'D3', 'E3', 'F#3/Gb3', 'G3', 'A3',
    'B3', 'C#4/Db4', 'D4', 'E4', 'F#4/Gb4', 'G4', 'A4',
    'B4', 'C#5/Db5', 'D5', 'E5', 'F#5/Gb5', 'G5', 'A5',
    'B5', 'C#6/Db6', 'D6', 'E6', 'F#6/Gb6', 'G6', 'A6',
    'B6', 'C#7/Db7', 'D7', 'E7', 'F#7/Gb7', 'G7', 'A7',
    'B7', 'C#8/Db8', 'D8', 'E8', 'F#8/Gb8', 'G8', 'A8'
]

note_frequencies = {
    'C0': 16.35, 'C#0/Db0': 17.32, 'D0': 18.35, 'D#0/Eb0': 19.45, 'E0': 20.60, 'F0': 21.83, 'F#0/Gb0': 23.12,
    'G0': 24.50, 'G#0/Ab0': 25.96, 'A0': 27.50, 'A#0/Bb0': 29.14, 'B0': 30.87, 
    'C1': 32.70, 'C#1/Db1': 34.65, 'D1': 36.71, 'D#1/Eb1': 38.89, 'E1': 41.20, 'F1': 43.65, 'F#1/Gb1': 46.25,
    'G1': 49.00, 'G#1/Ab1': 51.91, 'A1': 55.00, 'A#1/Bb1': 58.27, 'B1': 61.74, 
    'C2': 65.41, 'C#2/Db2': 69.30, 'D2': 73.42, 'D#2/Eb2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2/Gb2': 92.50,
    'G2': 98.00, 'G#2/Ab2': 103.83, 'A2': 110.00, 'A#2/Bb2': 116.54, 'B2': 123.47,
    'C3': 130.81, 'C#3/Db3': 138.59, 'D3': 146.83, 'D#3/Eb3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3/Gb3': 185.00,
    'G3': 196.00, 'G#3/Ab3': 207.65, 'A3': 220.00, 'A#3/Bb3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4/Db4': 277.18, 'D4': 293.66, 'D#4/Eb4': 311.13, 'E4': 329.63, 'F4': 349.23, 'F#4/Gb4': 369.99,
    'G4': 392.00, 'G#4/Ab4': 415.30, 'A4': 440.00, 'A#4/Bb4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5/Db5': 554.37, 'D5': 587.33, 'D#5/Eb5': 622.25, 'E5': 659.25, 'F5': 698.46, 'F#5/Gb5': 739.99,
    'G5': 783.99, 'G#5/Ab5': 830.61, 'A5': 880.00, 'A#5/Bb5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'C#6/Db6': 1108.73, 'D6': 1174.66, 'D#6/Eb6': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'F#6/Gb6': 1479.98,
    'G6': 1567.98, 'G#6/Ab6': 1661.22, 'A6': 1760.00, 'A#6/Bb6': 1864.66, 'B6': 1975.53,
    'C7': 2093.00, 'C#7/Db7': 2217.46, 'D7': 2349.32, 'D#7/Eb7': 2489.02, 'E7': 2637.02, 'F7': 2793.83, 'F#7/Gb7': 2959.96,
    'G7': 3135.96, 'G#7/Ab7': 3322.44, 'A7': 3520.00, 'A#7/Bb7': 3729.31, 'B7': 3951.07,
    'C8': 4186.01, 'C#8/Db8': 4434.92, 'D8': 4698.63, 'D#8/Eb8': 4978.03, 'E8': 5274.04, 'F8': 5587.65, 'F#8/Gb8': 5919.91,
    'G8': 6271.93, 'G#8/Ab8': 6644.88, 'A8': 7040.00, 'A#8/Bb8': 7458.62, 'B8': 7902.13
}
start_ascii = 19
end_ascii = 127
note_names = list(note_frequencies.keys())
file_notes = []
bpm = 120
beat_duration_ms = int((60 / bpm) * 1000)  # Duration of each beat in milliseconds

def get_note_name_from_ascii(ascii_char):
    return note_names[ascii_char - 19] # Simple mapping of the last ascii characters in the table

def read_file_bytes(file_path):
    with open(file_path, 'rb') as file:
        while byte := file.read(1):
            if byte:
                ascii_value = byte[0]
                if ascii_value >= start_ascii and ascii_value < end_ascii:
                    note_name = get_note_name_from_ascii(ascii_value)
                    if list(note_frequencies.keys()).index(note_name) >= list(note_frequencies.keys()).index('C3') and list(note_frequencies.keys()).index(note_name) <= list(note_frequencies.keys()).index('C5'):
                        file_notes.append(get_note_name_from_ascii(ascii_value))
                    
def play_frequency(frequency, duration=100):
    """
    Play a tone for the specified frequency.

    Args:
    frequency (float): The frequency of the tone in Hertz.
    duration (int, optional): The duration of the tone in milliseconds. Default is 100ms
    """
    # Generate a tone for the given frequency
    tone = Sine(frequency).to_audio_segment(duration=duration)

    # Play the tone
    wave_obj = sa.WaveObject(io.BytesIO(tone.raw_data).read(), num_channels=tone.channels, bytes_per_sample=tone.sample_width, sample_rate=tone.frame_rate)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    

file_path = 'ControlFlowFlattening.ipa'
read_file_bytes(file_path)

for note in file_notes:
    if note in c_major_notes:
        play_frequency(note_frequencies[note], beat_duration_ms)
        #time.sleep(beat_duration_ms / 1000)  # Convert milliseconds back to seconds for sleep