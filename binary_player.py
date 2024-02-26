from pydub import AudioSegment
from pydub.generators import Sine
import simpleaudio as sa
import io
import time
import sys
import argparse
import os
import math

START_ASCII = 19
END_ASCII = 127

g_major_notes = [
    'G0', 'A0', 'B0', 'C1', 'D1', 'E1', 'F#1',
    'G1', 'A1', 'B1', 'C2', 'D2', 'E2', 'F#2',
    'G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F#3',
    'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F#4',
    'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F#5',
    'G5', 'A5', 'B5', 'C6', 'D6', 'E6', 'F#6',
    'G6', 'A6', 'B6', 'C7', 'D7', 'E7', 'F#7',
    'G7', 'A7', 'B7', 'C8', 'D8', 'E8', 'F#8'
]

g_minor_notes = [
    'G0', 'A0', 'Bb0', 'C1', 'D1', 'Eb1', 'F1',
    'G1', 'A1', 'Bb1', 'C2', 'D2', 'Eb2', 'F2',
    'G2', 'A2', 'Bb2', 'C3', 'D3', 'Eb3', 'F3',
    'G3', 'A3', 'Bb3', 'C4', 'D4', 'Eb4', 'F4',
    'G4', 'A4', 'Bb4', 'C5', 'D5', 'Eb5', 'F5',
    'G5', 'A5', 'Bb5', 'C6', 'D6', 'Eb6', 'F6',
    'G6', 'A6', 'Bb6', 'C7', 'D7', 'Eb7', 'F7',
    'G7', 'A7', 'Bb7', 'C8', 'D8', 'Eb8', 'F8'
]

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

c_minor_notes = [
    'C0', 'D0', 'Eb0', 'F0', 'G0', 'Ab0', 'Bb0',
    'C1', 'D1', 'Eb1', 'F1', 'G1', 'Ab1', 'Bb1',
    'C2', 'D2', 'Eb2', 'F2', 'G2', 'Ab2', 'Bb2',
    'C3', 'D3', 'Eb3', 'F3', 'G3', 'Ab3', 'Bb3',
    'C4', 'D4', 'Eb4', 'F4', 'G4', 'Ab4', 'Bb4',
    'C5', 'D5', 'Eb5', 'F5', 'G5', 'Ab5', 'Bb5',
    'C6', 'D6', 'Eb6', 'F6', 'G6', 'Ab6', 'Bb6',
    'C7', 'D7', 'Eb7', 'F7', 'G7', 'Ab7', 'Bb7',
    'C8', 'D8', 'Eb8', 'F8', 'G8', 'Ab8', 'Bb8'
]

c_sharp_major_notes = [
    'C#0', 'D#0', 'E#0/F0', 'F#0', 'G#0', 'A#0', 'B#0/C1',
    'C#1', 'D#1', 'E#1/F1', 'F#1', 'G#1', 'A#1', 'B#1/C2',
    'C#2', 'D#2', 'E#2/F2', 'F#2', 'G#2', 'A#2', 'B#2/C3',
    'C#3', 'D#3', 'E#3/F3', 'F#3', 'G#3', 'A#3', 'B#3/C4',
    'C#4', 'D#4', 'E#4/F4', 'F#4', 'G#4', 'A#4', 'B#4/C5',
    'C#5', 'D#5', 'E#5/F5', 'F#5', 'G#5', 'A#5', 'B#5/C6',
    'C#6', 'D#6', 'E#6/F6', 'F#6', 'G#6', 'A#6', 'B#6/C7',
    'C#7', 'D#7', 'E#7/F7', 'F#7', 'G#7', 'A#7', 'B#7/C8',
    'C#8', 'D#8', 'E#8/F8', 'F#8', 'G#8', 'A#8', 'B#8/C9'
]

c_sharp_minor_notes = [
    'C#0', 'D#0', 'E0', 'F#0', 'G#0', 'A0', 'B0',
    'C#1', 'D#1', 'E1', 'F#1', 'G#1', 'A1', 'B1',
    'C#2', 'D#2', 'E2', 'F#2', 'G#2', 'A2', 'B2',
    'C#3', 'D#3', 'E3', 'F#3', 'G#3', 'A3', 'B3',
    'C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A4', 'B4',
    'C#5', 'D#5', 'E5', 'F#5', 'G#5', 'A5', 'B5',
    'C#6', 'D#6', 'E6', 'F#6', 'G#6', 'A6', 'B6',
    'C#7', 'D#7', 'E7', 'F#7', 'G#7', 'A7', 'B7',
    'C#8', 'D#8', 'E8', 'F#8', 'G#8', 'A8', 'B8'
]

b_major_notes = [
    'B0', 'C#1', 'D#1', 'E1', 'F#1', 'G#1', 'A#1',
    'B1', 'C#2', 'D#2', 'E2', 'F#2', 'G#2', 'A#2',
    'B2', 'C#3', 'D#3', 'E3', 'F#3', 'G#3', 'A#3',
    'B3', 'C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A#4',
    'B4', 'C#5', 'D#5', 'E5', 'F#5', 'G#5', 'A#5',
    'B5', 'C#6', 'D#6', 'E6', 'F#6', 'G#6', 'A#6',
    'B6', 'C#7', 'D#7', 'E7', 'F#7', 'G#7', 'A#7',
    'B7', 'C#8', 'D#8', 'E8', 'F#8', 'G#8', 'A#8'
]

b_minor_notes = [
    'B0', 'C#1', 'D1', 'E1', 'F#1', 'G1', 'A1',
    'B1', 'C#2', 'D2', 'E2', 'F#2', 'G2', 'A2',
    'B2', 'C#3', 'D3', 'E3', 'F#3', 'G3', 'A3',
    'B3', 'C#4', 'D4', 'E4', 'F#4', 'G4', 'A4',
    'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5',
    'B5', 'C#6', 'D6', 'E6', 'F#6', 'G6', 'A6',
    'B6', 'C#7', 'D7', 'E7', 'F#7', 'G7', 'A7',
    'B7', 'C#8', 'D8', 'E8', 'F#8', 'G8', 'A8'
]

bb_major_notes = [
    'Bb0/A#0', 'C1', 'D1', 'Eb1/D#1', 'F1', 'G1', 'A1',
    'Bb1/A#1', 'C2', 'D2', 'Eb2/D#2', 'F2', 'G2', 'A2',
    'Bb2/A#2', 'C3', 'D3', 'Eb3/D#3', 'F3', 'G3', 'A3',
    'Bb3/A#3', 'C4', 'D4', 'Eb4/D#4', 'F4', 'G4', 'A4',
    'Bb4/A#4', 'C5', 'D5', 'Eb5/D#5', 'F5', 'G5', 'A5',
    'Bb5/A#5', 'C6', 'D6', 'Eb6/D#6', 'F6', 'G6', 'A6',
    'Bb6/A#6', 'C7', 'D7', 'Eb7/D#7', 'F7', 'G7', 'A7',
    'Bb7/A#7', 'C8', 'D8', 'Eb8/D#8', 'F8', 'G8', 'A8'
]

bb_minor_notes = [
    'Bb0/A#0', 'C1', 'Db1/C#1', 'Eb1/D#1', 'F1', 'Gb1/F#1', 'Ab1/G#1',
    'Bb1/A#1', 'C2', 'Db2/C#2', 'Eb2/D#2', 'F2', 'Gb2/F#2', 'Ab2/G#2',
    'Bb2/A#2', 'C3', 'Db3/C#3', 'Eb3/D#3', 'F3', 'Gb3/F#3', 'Ab3/G#3',
    'Bb3/A#3', 'C4', 'Db4/C#4', 'Eb4/D#4', 'F4', 'Gb4/F#4', 'Ab4/G#4',
    'Bb4/A#4', 'C5', 'Db5/C#5', 'Eb5/D#5', 'F5', 'Gb5/F#5', 'Ab5/G#5',
    'Bb5/A#5', 'C6', 'Db6/C#6', 'Eb6/D#6', 'F6', 'Gb6/F#6', 'Ab6/G#6',
    'Bb6/A#6', 'C7', 'Db7/C#7', 'Eb7/D#7', 'F7', 'Gb7/F#7', 'Ab7/G#7',
    'Bb7/A#7', 'C8', 'Db8/C#8', 'Eb8/D#8', 'F8', 'Gb8/F#8', 'Ab8/G#8'
]

d_major_notes = [
    'D0', 'E0', 'F#0', 'G0', 'A0', 'B0', 'C#1',
    'D1', 'E1', 'F#1', 'G1', 'A1', 'B1', 'C#2',
    'D2', 'E2', 'F#2', 'G2', 'A2', 'B2', 'C#3',
    'D3', 'E3', 'F#3', 'G3', 'A3', 'B3', 'C#4',
    'D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5',
    'D5', 'E5', 'F#5', 'G5', 'A5', 'B5', 'C#6',
    'D6', 'E6', 'F#6', 'G6', 'A6', 'B6', 'C#7',
    'D7', 'E7', 'F#7', 'G7', 'A7', 'B7', 'C#8'
]

d_minor_notes = [
    'D0', 'E0', 'F0', 'G0', 'A0', 'Bb0', 'C1',
    'D1', 'E1', 'F1', 'G1', 'A1', 'Bb1', 'C2',
    'D2', 'E2', 'F2', 'G2', 'A2', 'Bb2', 'C3',
    'D3', 'E3', 'F3', 'G3', 'A3', 'Bb3', 'C4',
    'D4', 'E4', 'F4', 'G4', 'A4', 'Bb4', 'C5',
    'D5', 'E5', 'F5', 'G5', 'A5', 'Bb5', 'C6',
    'D6', 'E6', 'F6', 'G6', 'A6', 'Bb6', 'C7',
    'D7', 'E7', 'F7', 'G7', 'A7', 'Bb7', 'C8',
    'D8', 'E8', 'F8', 'G8', 'A8', 'Bb8', 'C9'
]

db_minor_notes = [
    'Db0/C#0', 'Eb0/D#0', 'E0', 'F0', 'Gb0/F#0', 'Ab0/G#0', 'A0',
    'Db1/C#1', 'Eb1/D#1', 'E1', 'F1', 'Gb1/F#1', 'Ab1/G#1', 'A1',
    'Db2/C#2', 'Eb2/D#2', 'E2', 'F2', 'Gb2/F#2', 'Ab2/G#2', 'A2',
    'Db3/C#3', 'Eb3/D#3', 'E3', 'F3', 'Gb3/F#3', 'Ab3/G#3', 'A3',
    'Db4/C#4', 'Eb4/D#4', 'E4', 'F4', 'Gb4/F#4', 'Ab4/G#4', 'A4',
    'Db5/C#5', 'Eb5/D#5', 'E5', 'F5', 'Gb5/F#5', 'Ab5/G#5', 'A5',
    'Db6/C#6', 'Eb6/D#6', 'E6', 'F6', 'Gb6/F#6', 'Ab6/G#6', 'A6',
    'Db7/C#7', 'Eb7/D#7', 'E7', 'F7', 'Gb7/F#7', 'Ab7/G#7', 'A7',
    'Db8/C#8', 'Eb8/D#8', 'E8', 'F8', 'Gb8/F#8', 'Ab8/G#8', 'A8'
]

eb_major_notes = [
    'Eb0/D#0', 'F0', 'G0', 'Ab0/G#0', 'Bb0/A#0', 'C1', 'D1',
    'Eb1/D#1', 'F1', 'G1', 'Ab1/G#1', 'Bb1/A#1', 'C2', 'D2',
    'Eb2/D#2', 'F2', 'G2', 'Ab2/G#2', 'Bb2/A#2', 'C3', 'D3',
    'Eb3/D#3', 'F3', 'G3', 'Ab3/G#3', 'Bb3/A#3', 'C4', 'D4',
    'Eb4/D#4', 'F4', 'G4', 'Ab4/G#4', 'Bb4/A#4', 'C5', 'D5',
    'Eb5/D#5', 'F5', 'G5', 'Ab5/G#5', 'Bb5/A#5', 'C6', 'D6',
    'Eb6/D#6', 'F6', 'G6', 'Ab6/G#6', 'Bb6/A#6', 'C7', 'D7',
    'Eb7/D#7', 'F7', 'G7', 'Ab7/G#7', 'Bb7/A#7', 'C8', 'D8',
    'Eb8/D#8', 'F8', 'G8', 'Ab8/G#8', 'Bb8/A#8'
]

eb_minor_notes = [
    'Eb0/D#0', 'F0', 'Gb0/F#0', 'Ab0/G#0', 'Bb0/A#0', 'Cb1/B0', 'Db1/C#1',
    'Eb1/D#1', 'F1', 'Gb1/F#1', 'Ab1/G#1', 'Bb1/A#1', 'Cb2/B1', 'Db2/C#2',
    'Eb2/D#2', 'F2', 'Gb2/F#2', 'Ab2/G#2', 'Bb2/A#2', 'Cb3/B2', 'Db3/C#3',
    'Eb3/D#3', 'F3', 'Gb3/F#3', 'Ab3/G#3', 'Bb3/A#3', 'Cb4/B3', 'Db4/C#4',
    'Eb4/D#4', 'F4', 'Gb4/F#4', 'Ab4/G#4', 'Bb4/A#4', 'Cb5/B4', 'Db5/C#5',
    'Eb5/D#5', 'F5', 'Gb5/F#5', 'Ab5/G#5', 'Bb5/A#5', 'Cb6/B5', 'Db6/C#6',
    'Eb6/D#6', 'F6', 'Gb6/F#6', 'Ab6/G#6', 'Bb6/A#6', 'Cb7/B6', 'Db7/C#7',
    'Eb7/D#7', 'F7', 'Gb7/F#7', 'Ab7/G#7', 'Bb7/A#7', 'Cb8/B7', 'Db8/C#8',
    'Eb8/D#8', 'F8', 'Gb8/F#8', 'Ab8/G#8', 'Bb8/A#8'
]

e_major_notes = [
    'E0', 'F#0', 'G#0', 'A0', 'B0', 'C#1', 'D#1',
    'E1', 'F#1', 'G#1', 'A1', 'B1', 'C#2', 'D#2',
    'E2', 'F#2', 'G#2', 'A2', 'B2', 'C#3', 'D#3',
    'E3', 'F#3', 'G#3', 'A3', 'B3', 'C#4', 'D#4',
    'E4', 'F#4', 'G#4', 'A4', 'B4', 'C#5', 'D#5',
    'E5', 'F#5', 'G#5', 'A5', 'B5', 'C#6', 'D#6',
    'E6', 'F#6', 'G#6', 'A6', 'B6', 'C#7', 'D#7',
    'E7', 'F#7', 'G#7', 'A7', 'B7', 'C#8', 'D#8'
]

e_minor_notes = [
    'E0', 'F#0', 'G0', 'A0', 'B0', 'C1', 'D1',
    'E1', 'F#1', 'G1', 'A1', 'B1', 'C2', 'D2',
    'E2', 'F#2', 'G2', 'A2', 'B2', 'C3', 'D3',
    'E3', 'F#3', 'G3', 'A3', 'B3', 'C4', 'D4',
    'E4', 'F#4', 'G4', 'A4', 'B4', 'C5', 'D5',
    'E5', 'F#5', 'G5', 'A5', 'B5', 'C6', 'D6',
    'E6', 'F#6', 'G6', 'A6', 'B6', 'C7', 'D7',
    'E7', 'F#7', 'G7', 'A7', 'B7', 'C8', 'D8'
]

f_major_notes = [
    'F0', 'G0', 'A0', 'Bb0', 'C1', 'D1', 'E1',
    'F1', 'G1', 'A1', 'Bb1', 'C2', 'D2', 'E2',
    'F2', 'G2', 'A2', 'Bb2', 'C3', 'D3', 'E3',
    'F3', 'G3', 'A3', 'Bb3', 'C4', 'D4', 'E4',
    'F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5',
    'F5', 'G5', 'A5', 'Bb5', 'C6', 'D6', 'E6',
    'F6', 'G6', 'A6', 'Bb6', 'C7', 'D7', 'E7',
    'F7', 'G7', 'A7', 'Bb7', 'C8', 'D8', 'E8'
]

f_minor_notes = [
    'F0', 'G0', 'Ab0', 'Bb0', 'C1', 'Db1', 'Eb1',
    'F1', 'G1', 'Ab1', 'Bb1', 'C2', 'Db2', 'Eb2',
    'F2', 'G2', 'Ab2', 'Bb2', 'C3', 'Db3', 'Eb3',
    'F3', 'G3', 'Ab3', 'Bb3', 'C4', 'Db4', 'Eb4',
    'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'Db5', 'Eb5',
    'F5', 'G5', 'Ab5', 'Bb5', 'C6', 'Db6', 'Eb6',
    'F6', 'G6', 'Ab6', 'Bb6', 'C7', 'Db7', 'Eb7',
    'F7', 'G7', 'Ab7', 'Bb7', 'C8', 'Db8', 'Eb8'
]

f_sharp_major_notes = [
    'F#0', 'G#0', 'A#0', 'B0', 'C#1', 'D#1', 'E#1/F1',
    'F#1', 'G#1', 'A#1', 'B1', 'C#2', 'D#2', 'E#2/F2',
    'F#2', 'G#2', 'A#2', 'B2', 'C#3', 'D#3', 'E#3/F3',
    'F#3', 'G#3', 'A#3', 'B3', 'C#4', 'D#4', 'E#4/F4',
    'F#4', 'G#4', 'A#4', 'B4', 'C#5', 'D#5', 'E#5/F5',
    'F#5', 'G#5', 'A#5', 'B5', 'C#6', 'D#6', 'E#6/F6',
    'F#6', 'G#6', 'A#6', 'B6', 'C#7', 'D#7', 'E#7/F7',
    'F#7', 'G#7', 'A#7', 'B7', 'C#8', 'D#8', 'E#8/F8'
]

f_sharp_minor_notes = [
    'F#0', 'G#0', 'A0', 'B0', 'C#1', 'D1', 'E1',
    'F#1', 'G#1', 'A1', 'B1', 'C#2', 'D2', 'E2',
    'F#2', 'G#2', 'A2', 'B2', 'C#3', 'D3', 'E3',
    'F#3', 'G#3', 'A3', 'B3', 'C#4', 'D4', 'E4',
    'F#4', 'G#4', 'A4', 'B4', 'C#5', 'D5', 'E5',
    'F#5', 'G#5', 'A5', 'B5', 'C#6', 'D6', 'E6',
    'F#6', 'G#6', 'A6', 'B6', 'C#7', 'D7', 'E7',
    'F#7', 'G#7', 'A7', 'B7', 'C#8', 'D8', 'E8'
]

a_major_notes = [
    'A0', 'B0', 'C#1', 'D1', 'E1', 'F#1', 'G#1',
    'A1', 'B1', 'C#2', 'D2', 'E2', 'F#2', 'G#2',
    'A2', 'B2', 'C#3', 'D3', 'E3', 'F#3', 'G#3',
    'A3', 'B3', 'C#4', 'D4', 'E4', 'F#4', 'G#4',
    'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G#5',
    'A5', 'B5', 'C#6', 'D6', 'E6', 'F#6', 'G#6',
    'A6', 'B6', 'C#7', 'D7', 'E7', 'F#7', 'G#7',
    'A7', 'B7', 'C#8', 'D8', 'E8', 'F#8', 'G#8'
]

a_minor_notes = [
    'A0', 'B0', 'C1', 'D1', 'E1', 'F1', 'G1',
    'A1', 'B1', 'C2', 'D2', 'E2', 'F2', 'G2',
    'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3',
    'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4',
    'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5',
    'A5', 'B5', 'C6', 'D6', 'E6', 'F6', 'G6',
    'A6', 'B6', 'C7', 'D7', 'E7', 'F7', 'G7',
    'A7', 'B7', 'C8', 'D8', 'E8', 'F8', 'G8'
]

ab_major_notes = [
    'Ab0/G#0', 'Bb0/A#0', 'C1', 'Db1/C#1', 'Eb1/D#1', 'F1', 'G1',
    'Ab1/G#1', 'Bb1/A#1', 'C2', 'Db2/C#2', 'Eb2/D#2', 'F2', 'G2',
    'Ab2/G#2', 'Bb2/A#2', 'C3', 'Db3/C#3', 'Eb3/D#3', 'F3', 'G3',
    'Ab3/G#3', 'Bb3/A#3', 'C4', 'Db4/C#4', 'Eb4/D#4', 'F4', 'G4',
    'Ab4/G#4', 'Bb4/A#4', 'C5', 'Db5/C#5', 'Eb5/D#5', 'F5', 'G5',
    'Ab5/G#5', 'Bb5/A#5', 'C6', 'Db6/C#6', 'Eb6/D#6', 'F6', 'G6',
    'Ab6/G#6', 'Bb6/A#6', 'C7', 'Db7/C#7', 'Eb7/D#7', 'F7', 'G7',
    'Ab7/G#7', 'Bb7/A#7', 'C8', 'Db8/C#8', 'Eb8/D#8', 'F8', 'G8'
]

ab_minor_notes = [
    'Ab0/G#0', 'Bb0/A#0', 'B0', 'Db1/C#1', 'Eb1/D#1', 'E1', 'Gb1/F#1',
    'Ab1/G#1', 'Bb1/A#1', 'B1', 'Db2/C#2', 'Eb2/D#2', 'E2', 'Gb2/F#2',
    'Ab2/G#2', 'Bb2/A#2', 'B2', 'Db3/C#3', 'Eb3/D#3', 'E3', 'Gb3/F#3',
    'Ab3/G#3', 'Bb3/A#3', 'B3', 'Db4/C#4', 'Eb4/D#4', 'E4', 'Gb4/F#4',
    'Ab4/G#4', 'Bb4/A#4', 'B4', 'Db5/C#5', 'Eb5/D#5', 'E5', 'Gb5/F#5',
    'Ab5/G#5', 'Bb5/A#5', 'B5', 'Db6/C#6', 'Eb6/D#6', 'E6', 'Gb6/F#6',
    'Ab6/G#6', 'Bb6/A#6', 'B6', 'Db7/C#7', 'Eb7/D#7', 'E7', 'Gb7/F#7',
    'Ab7/G#7', 'Bb7/A#7', 'B7', 'Db8/C#8', 'Eb8/D#8', 'E8', 'Gb8/F#8'
]

"""
Summary

    All 12 major scales:
        C Major
        G Major
        D Major
        A Major
        E Major
        B Major
        F# (Gb) Major
        Db (C#) Major
        Ab (G#) Major
        Eb (D#) Major
        Bb (A#) Major
        F Major

    All 12 natural minor scales:
        A Minor
        E Minor
        B Minor
        F# (Gb) Minor
        C# (Db) Minor
        G# (Ab) Minor
        Eb (D#) Minor
        Bb (A#) Minor
        F Minor
        C Minor
        G Minor
        D Minor
"""

note_frequencies = {
    'C0': 16.35, 'C#0': 17.32, 'D0': 18.35, 'D#0': 19.45, 'E0': 20.60, 'F0': 21.83, 'F#0': 23.12,
    'G0': 24.50, 'G#0': 25.96, 'A0': 27.50, 'A#0': 29.14, 'B0': 30.87, 
    'C1': 32.70, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.20, 'F1': 43.65, 'F#1': 46.25,
    'G1': 49.00, 'G#1': 51.91, 'A1': 55.00, 'A#1': 58.27, 'B1': 61.74, 
    'C2': 65.41, 'C#2': 69.30, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2': 92.50,
    'G2': 98.00, 'G#2': 103.83, 'A2': 110.00, 'A#2': 116.54, 'B2': 123.47,
    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3': 185.00,
    'G3': 196.00, 'G#3': 207.65, 'A3': 220.00, 'A#3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63, 'F4': 349.23, 'F#4': 369.99,
    'G4': 392.00, 'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25, 'F5': 698.46, 'F#5': 739.99,
    'G5': 783.99, 'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'C#6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'F#6': 1479.98,
    'G6': 1567.98, 'G#6': 1661.22, 'A6': 1760.00, 'A#6': 1864.66, 'B6': 1975.53,
    'C7': 2093.00, 'C#7': 2217.46, 'D7': 2349.32, 'D#7': 2489.02, 'E7': 2637.02, 'F7': 2793.83, 'F#7': 2959.96,
    'G7': 3135.96, 'G#7': 3322.44, 'A7': 3520.00, 'A#7': 3729.31, 'B7': 3951.07,
    'C8': 4186.01, 'C#8': 4434.92, 'D8': 4698.63, 'D#8': 4978.03, 'E8': 5274.04, 'F8': 5587.65, 'F#8': 5919.91,
    'G8': 6271.93, 'G#8': 6644.88, 'A8': 7040.00, 'A#8': 7458.62, 'B8': 7902.13
}

file_type_mapping = {
    '.apk': g_major_notes,     # Android Package
    '.exe': c_major_notes,     # Executable File for Windows
    '.md': a_minor_notes,      # Markdown Text File
    '.ipa': e_minor_notes,     # iOS App Store Package
    '.elf': d_minor_notes,     # Executable and Linkable Format (Unix/Linux)
    '.txt': f_major_notes,     # Plain Text File
    '.macho': b_minor_notes,   # Mach Object (macOS)
    '.dll': g_minor_notes,     # Dynamic Link Library (Windows)
    '.so': ab_major_notes,     # Shared Object (Unix/Linux)
    '.dex': e_major_notes,     # Android Dalvik Executable
    '.asm': c_sharp_minor_notes, # Assembly Language Source Code File
    '.wasm': f_sharp_major_notes, # WebAssembly File
    '.py': a_major_notes,      # Python Script
    '.java': e_minor_notes,    # Java Source Code File
    '.html': c_minor_notes,    # HTML File
    '.css': d_major_notes,     # Cascading Style Sheets
    '.js': b_major_notes,      # JavaScript File
    '.json': db_minor_notes,   # JSON File
    '.xml': eb_major_notes,    # XML File
    '.csv': f_minor_notes,     # Comma Separated Values File
    '.mp3': ab_minor_notes,    # MP3 Audio File
    '.wav': bb_major_notes,    # WAV Audio File
    '.mp4': bb_minor_notes,    # MP4 Video File
    '.avi': eb_minor_notes,    # AVI Video File
    '.jpg': c_sharp_major_notes,    # JPEG Image File
    '.png': f_sharp_major_notes,    # PNG Image File
    '.gif': eb_major_notes,    # GIF Image File
    '.pdf': b_major_notes,     # Portable Document Format File
    '.docx': f_sharp_minor_notes,   # Microsoft Word Document
    '.pptx': ab_major_notes,   # Microsoft PowerPoint Presentation
    '.xlsx': db_minor_notes,   # Microsoft Excel Spreadsheet
}

note_names = list(note_frequencies.keys())
bpm = 120

# Duration of each beat in milliseconds
# Note: there can be longer notes if two of the same notes are next to each other
beat_duration_ms = int((60 / bpm) * 1000)

def get_note_name_from_ascii(ascii_char):
    return note_names[ascii_char - 19] # Simple mapping of the last ascii characters in the table
    
def get_note_index(note_name):
    return list(note_frequencies.keys()).index(note_name)
    
# Default note range
lowest_note = 'C3'
highest_note = 'C5'

def play_notes_from_file(file_path):
    print("Starting to play file...")

    previous_note = None
    num_repeated_notes = 1

    with open(file_path, 'rb') as file:
        while byte := file.read(1):
            if byte:
                ascii_value = byte[0]
                if START_ASCII <= ascii_value < END_ASCII:
                    note_name = get_note_name_from_ascii(ascii_value)
                    if note_name in note_frequencies.keys():
                        if note_name not in current_key:
                            # Rest or silence if the note is not in the current key
                            time.sleep((beat_duration_ms / 1000) / 2)  # Rest for half the beat duration
                        elif note_name == previous_note:
                            # Increment the duration if the current note is the same as the previous note
                            num_repeated_notes += 1
                        else:
                            if previous_note is not None:
                                note_to_play = previous_note
                                
                                # Shift note up or down an octave to fit into the note range
                                if get_note_index(note_to_play) < get_note_index(lowest_note):
                                    # Shift note up to be inside the accepted octaves
                                    # Dummy implementation shifting the note to be in the lowest octave
                                    # This could be improved but it will work
                                    note_letter = note_to_play[:-1]
                                    new_octave = int(lowest_note[-1])
                                    
                                    if get_note_index(note_to_play) < get_note_index(lowest_note):
                                        new_octave += 1
                                        
                                    note_to_play = note_letter + str(new_octave)
                                        
                                elif get_note_index(note_to_play) > get_note_index(highest_note):
                                    # Shift note down to be inside the accepted octaves
                                    note_letter = note_to_play[:-1]
                                    new_octave = int(highest_note[-1])
                                    
                                    if get_note_index(note_to_play) > get_note_index(highest_note):
                                        new_octave -= 1
                                        
                                    note_to_play = note_letter + str(new_octave)
                                
                                # Play the previous note with the accumulated duration
                                play_frequency(note_frequencies[note_to_play], num_repeated_notes * beat_duration_ms)
                            # Reset the repeated notes counter
                            num_repeated_notes = 1

                        previous_note = note_name

    # Play the last note
    if previous_note is not None and previous_note in current_key:
        play_frequency(note_frequencies[previous_note], num_repeated_notes * beat_duration_ms)

    print("Finished playing file.")
                        
def calculate_file_entropy(file_path, sample_size=1024*1024):  # Default sample size set to 1MB
    """
    Calculate the Shannon entropy of a file using a sample if the file is too big.

    Args:
    file_path (str): The path to the file whose entropy is to be calculated.
    sample_size (int): The size of the sample to read in bytes, default is 1MB.

    Returns:
    float: The calculated entropy of the file.
    """
    file_size = os.path.getsize(file_path)
    data = b''

    with open(file_path, 'rb') as file:
        # If the file is larger than twice the sample size, read a sample from the middle
        if file_size > 2 * sample_size:
            # Seek to the middle of the file minus half the sample size
            file.seek((file_size // 2) - (sample_size // 2))
            data = file.read(sample_size)
        else:
            data = file.read()  # Read the whole file if it's small enough

    print("Calculating entropy...")

    # If the file or sample is empty, return 0 as the entropy
    if not data:
        return 0

    # Initialize a frequency dictionary for all bytes [0-255]
    byte_counts = {byte: 0 for byte in range(256)}

    # Count the occurrence of each byte in the file or sample
    for byte in data:
        byte_counts[byte] += 1

    # Total number of bytes in the sample or file
    total_bytes = len(data)

    # Calculate the entropy
    entropy = 0
    for count in byte_counts.values():
        if count == 0:
            continue
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)

    return entropy
                    
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
    
parser = argparse.ArgumentParser(description='Process a file to play its bytes as musical notes.')
parser.add_argument('file_path', type=str, help='Path to the file to be processed')
args = parser.parse_args()
file_path = args.file_path

# Check extension of passed in file and change key accordingly
_, file_extension = os.path.splitext(file_path)
file_extension = file_extension.lower()
current_key = file_type_mapping.get(file_extension, c_major_notes)  # Default to C Major if not found

#print("Extension: " + file_extension)
print("Playing file " + file_path)

if current_key == g_major_notes:
    print("Key: G Major")
elif current_key == c_major_notes:
    print("Key: C Major")
elif current_key == a_minor_notes:
    print("Key: A Minor")
elif current_key == e_minor_notes:
    print("Key: E Minor")
elif current_key == g_minor_notes:
    print("Key: G Minor")
elif current_key == c_minor_notes:
    print("Key: C Minor")
elif current_key == c_sharp_major_notes:
    print("Key: C# Major / Db Major")
elif current_key == c_sharp_minor_notes:
    print("Key: C# Minor / Db Minor")
elif current_key == b_major_notes:
    print("Key: B Major")
elif current_key == b_minor_notes:
    print("Key: B Minor")
elif current_key == bb_major_notes:
    print("Key: Bb Major / A# Major")
elif current_key == bb_minor_notes:
    print("Key: Bb Minor / A# Minor")
elif current_key == d_major_notes:
    print("Key: D Major")
elif current_key == d_minor_notes:
    print("Key: D Minor")
elif current_key == db_minor_notes:
    print("Key: Db Minor / C# Minor")
elif current_key == eb_major_notes:
    print("Key: Eb Major / D# Major")
elif current_key == eb_minor_notes:
    print("Key: Eb Minor / D# Minor")
elif current_key == e_major_notes:
    print("Key: E Major")
elif current_key == e_minor_notes:
    print("Key: E Minor")
elif current_key == f_major_notes:
    print("Key: F Major")
elif current_key == f_minor_notes:
    print("Key: F Minor")
elif current_key == f_sharp_major_notes:
    print("Key: F# Major / Gb Major")
elif current_key == f_sharp_minor_notes:
    print("Key: F# Minor / Gb Minor")
elif current_key == a_major_notes:
    print("Key: A Major")
elif current_key == a_minor_notes:
    print("Key: A Minor")
elif current_key == ab_major_notes:
    print("Key: Ab Major / G# Major")
elif current_key == ab_minor_notes:
    print("Key: Ab Minor / G# Minor")
else:
    print("Key: Unknown or not set")

# Set the key range based on the entropy of the file
# Higher entropy means higher range
# Default to a max range of 2 octaves
file_entropy = calculate_file_entropy(file_path)
print("File entropy: " + str(file_entropy))

play_notes_from_file(file_path)    
    
# TODO: add output to midi + output sheet music (lilypond)

