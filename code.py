# non-repeating-pocket-yoda.py
import board, neopixel, time, random, digitalio, adafruit_lis3dh, busio
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.solid import Solid

# import lines needed to play sound files
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile

# COLOR, ANIMATION & NEOPIXEL SETUP
# You don't need all these colors - but I dump this code in most files where I work with NeoPixels so I have access to them if I want a color change.
from adafruit_led_animation.color import (
    AMBER, #(255, 100, 0)
    AQUA, # (50, 255, 255)
    BLACK, #OFF (0, 0, 0)
    BLUE, # (0, 0, 255)
    CYAN, # (0, 255, 255)
    GOLD, # (255, 222, 30)
    GREEN, # (0, 255, 0)
    JADE, # (0, 255, 40)
    MAGENTA, #(255, 0, 20)
    OLD_LACE, # (253, 245, 230)
    ORANGE, # (255, 40, 0)
    PINK, # (242, 90, 255)
    PURPLE, # (180, 0, 255)
    RED, # (255, 0, 0)
    TEAL, # (0, 255, 120)
    WHITE, # (255, 255, 255)
    YELLOW, # (255, 150, 0)
    RAINBOW # a list of colors to cycle through
    # RAINBOW is RED, ORANGE, YELLOW, GREEN, BLUE, and PURPLE ((255, 0, 0), (255, 40, 0), (255, 150, 0), (0, 255, 0), (0, 0, 255), (180, 0, 255))
)

pixels_pin = board.NEOPIXEL
lights_on_pixels = 10
pixels = neopixel.NeoPixel(pixels_pin, lights_on_pixels, brightness=0.5, auto_write=True)

comet = Comet(pixels, speed=0.1, color=GREEN, tail_length=10, bounce=True)
solid = Solid(pixels, color=BLACK)

# ACCELEROMATER SETUP
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)
accelerometer.range = adafruit_lis3dh.RANGE_8_G

# SOUND SETUP
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True
audio = AudioOut(board.SPEAKER)

# MAKE SURE you have the folder "yoda-sounds" on your CPB & it contains the wavs 0.wav through 8.wav
path = "yoda-sounds/"

last_sound_number = -1 # will hold the last sound # played. -1 will never happen so any sound can be the first sound

def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            comet.animate() # will swirl the CPB in green
        solid.animate() # clears the CPB, turning off all LEDs

while True:
    # Detect a shake
    if accelerometer.shake(shake_threshold=15):
        sound_number = random.randrange(9) # returns 0 - 9
        while sound_number == last_sound_number: # make sure last advice/sound isn't repeated
            sound_number = random.randrange(9)
        last_sound_number = sound_number # save the non-repeating sound as the last_sound played
        print(f"Playing sound #{sound_number}")
        play_sound(f"{sound_number}.wav")

