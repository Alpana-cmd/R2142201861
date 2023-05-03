# Import necessary libraries
import numpy as np
import wave
import struct
import random

# Define chaotic maps
def henon_map(x, y, a, b):
    x_next = 1 - a * x**2 + y
    y_next = b * x
    return x_next, y_next

def lsc_map(x, r):
    return np.cos(np.pi * (4 * r * x * (1 - x) + (1 - r) * np.sin(np.pi * x) - 0.5))

# Load audio file
audio_file = wave.open("C:\Users\Hp\OneDrive\Desktop\My audio wav\1f7f8b00-cae4-11ed-ad44-db82a9e50521.wav "rb")
nframes = audio_file.getnframes()
sample_rate = audio_file.getframerate()
channels = audio_file.getnchannels()

# Convert audio data to numerical format
raw_audio = audio_file.readframes(nframes)
audio_array = np.array(struct.unpack("<" + "h"*nframes*channels, raw_audio))
audio_array = audio_array.reshape((nframes, channels))

# Generate encryption key using chaotic maps
key_length = nframes // 100
x, y = random.uniform(0, 1), random.uniform(0, 1)
a, b = random.uniform(1, 1.5), random.uniform(0.2, 0.5)
r = random.uniform(0, 1)
key1 = np.zeros(key_length)
key2 = np.zeros(key_length)
for i in range(key_length):
    x, y = henon_map(x, y, a, b)
    key1[i] = x
    r = lsc_map(r, x)
    key2[i] = r

# Encrypt audio data using chaotic maps and XOR operation
encrypted_audio = np.zeros((nframes, channels))
for i in range(nframes):
    encrypted_audio[i] = audio_array[i] ^ int(key1[i % key_length] * key2[i % key_length] * 1000)

# Save encrypted audio file
encrypted_audio_file = wave.open("encrypted.wav", "wb")
encrypted_audio_file.setparams(audio_file.getparams())
encrypted_audio_file.writeframes(struct.pack("<" + "h" * nframes * channels, *encrypted_audio.reshape((nframes * channels,))))
encrypted_audio_file.close()

# Decrypt audio file using the same key
decrypted_audio = np.zeros((nframes, channels))
for i in range(nframes):
    decrypted_audio[i] = encrypted_audio[i] ^ int(key1[i % key_length] * key2[i % key_length] * 1000)

# Save decrypted audio file
decrypted_audio_file = wave.open("decrypted.wav", "wb")
decrypted_audio_file.setparams(audio_file.getparams())
decrypted_audio_file.writeframes(struct.pack("<" + "h" * nframes * channels, *decrypted_audio.reshape((nframes * channels,))))
decrypted_audio_file.close()

# Close audio file
audio_file.close()
