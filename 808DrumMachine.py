import audioio
import touchio
import board
import neopixel
import time

from digitalio import DigitalInOut, Direction

bpm = 100
audioFiles = [
    'bass_hit_c.wav',
    'bd_tek.wav',
    'bd_zome.wav',
    'drum_cowbell.wav',
    'elec_blip2.wav',
    'elec_cymbal.wav',
    'elec_hi_snare.wav'
]
thresholds = (
    3750, #A1
    3500, #A2
    3750, #A3
    3250, #A4
    3250, #A5
    3750, #A6
    3750, #A7
)
colors = (
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 85, 0),
    (0, 255, 0),
    (255, 0, 255)
)
off = (0, 0, 0)

# Enable the speaker
spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = Direction.OUTPUT
spkrenable.value = True

# Analog audio output
a = audioio.AudioOut(board.A0)

# Enable capacitive touch pads on A1-7
capPins = (board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.A7)
touchPad = []
 
for i in range(7):
  touchPad.append(touchio.TouchIn(capPins[i]))
  touchPad[i].threshold = thresholds[i]

# Enable pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)


def play_file(filename):
    f = open(filename, "rb")
    wave = audioio.WaveFile(f)
    a.play(wave)
    time.sleep(bpm/960)  # sixteenthNote delay


while True:
    for i in range(7):
        if touchPad[i].value:
            play_file(audioFiles[i])
            pixels[i] = colors[i]
            pixels.show()
            time.sleep(0.05)
            pixels[i] = off
            pixels.show()