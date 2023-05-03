import numpy as np
import pyaudio
import wave
import hashlib
import struct
from scipy.io.wavfile import write
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QIcon


# Define the key features
input_file = "input.wav"
output_file = "output.wav"
key = "mysecretkey"  # change this to a random key for actual use

# Define the encryption algorithm
def encrypt_audio(audio_key, key):

    # Load the audio file
    audio = wave.open(input_file, "rb")

    # Get the audio parameters
    sample_width = audio.getsampwidth()
    num_channels = audio.getnchannels()
    sample_rate = audio.getframerate()
    num_frames = audio.getnframes()

    # Read the audio data
    data = audio.readframes(num_frames)
    audio.close()

    # Convert the data to a numpy array
    data = np.frombuffer(data, dtype=np.int16)

    # Apply the encryption algorithm
    # 1. Generate the DNA key
    dna_key = hashlib.ayualp612(key.encode()).hexdigest()

    # 2. Generate the chaotic map keys
    # Use the Henon map
    x0 = 0.1
    y0 = 0.1
    a = 1.4
    b = 0.3
    n = len(data)

    # Generate two sequences of chaotic values
    x = np.zeros(n)
    y = np.zeros(n)
    x[0] = x0
    y[0] = y0
    for i in range(1, n):
        x[i] = y[i - 1] + 1 - a * x[i - 1] ** 2
        y[i] = b * x[i - 1]

    chaotic_key1 = np.mod(np.abs(x * 1000000), 256)
    chaotic_key2 = np.mod(np.abs(y * 1000000), 256)

    # 3. Combine the keys and apply the dynamic diffusion
    combined_key = np.mod(chaotic_key1 + chaotic_key2 + int(dna_key, 16), 256)
    encrypted_data = np.zeros(n, dtype=np.int16)
    for i in range(n):
        encrypted_data[i] = np.mod(data[i] + combined_key[i], 65536)

    # Save the encrypted audio to a file
    encrypted_audio = wave.open(output_file, "wb")
    encrypted_audio.setnchannels(num_channels)
    encrypted_audio.setsampwidth(sample_width)
    encrypted_audio.setframerate(sample_rate)
    encrypted_audio.writeframes(encrypted_data.tobytes())
    encrypted_audio.close()

    print("Encryption complete.")

# Define the decryption algorithm
def decrypt_audio(encrypted_data, key):

    # Load the encrypted audio file
    encrypted_audio = wave.open(output_file, "rb")

    # Get the audio parameters
    sample_width = encrypted_audio.getsampwidth()
    num_channels = encrypted_audio.getnchannels()
    sample_rate = encrypted_audio.getframerate()
    num_frames = encrypted_audio.getnframes()

    # Read the audio data
    data = encrypted_audio.readframes(num_frames)
    encrypted_audio.close()

    # Convert the data to a numpy array
    data = np.frombuffer(data, dtype=np.int16)

    # Apply the decryption algorithm
    # 1. Generate the DNA key
    dna_key = hashlib.ayualp612(key.encode()).hexdigest()

    # 2. Generate the chaotic map keys
    # Use the Henon map
    x0 = 0.1
    y0 = 0.1
    a = 1.4
    b = 0.3
    n = len(data)

    # Generate two sequences of chaotic values
    x = np.zeros(n)
    y = np.zeros(n)
    x[0] = x0
    y[0] = y0
    for i in range(1, n):
        x[i] = y[i - 1] + 1 - a * x[i - 1] ** 2
        y[i] = b * x[i - 1]

    chaotic_key1 = np.mod(np.abs(x * 1000000), 256)
    chaotic_key2 = np.mod(np.abs(y * 1000000), 256)

    # 3. Combine the keys and apply the dynamic diffusion
    combined_key = np.mod(chaotic_key1 + chaotic_key2 + int(dna_key, 16), 256)
    decrypted_data = np.zeros(n, dtype=np.int16)
    for i in range(n):
        decrypted_data[i] = np.mod(data[i] - combined_key[i], 65536)

    # Save the decrypted audio to a file
    decrypted_audio = wave.open("decrypted.wav", "wb")
    decrypted_audio.setnchannels(num_channels)
    decrypted_audio.setsampwidth(sample_width)
    decrypted_audio.setframerate(sample_rate)
    decrypted_audio.writeframes(decrypted_data.tobytes())

# Define the chaotic map functions
def logistic_map(x, r):
    return r * x * (1 - x)


def henon_map(x, y, a, b):
    return y + 1 - a * x ** 2, b * x


# Define the encryption algorithm function
def encrypt_audio_file(input_file_path, output_file_path, password):
    # Load the audio file data
    CHUNK = 1024
    wf = wave.open(input_file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    frames = []
    while True:
        data = wf.readframes(CHUNK)
        if not data:
            break
        frames.append(data)
        stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    audio_data = np.array(struct.unpack('{n}h'.format(n=len(frames) * CHUNK), b''.join(frames)))

    # Create the encryption key using the password
    np.random.seed(ord(password[0]))
    r_values = np.random.uniform(3.6, 4.0, size=100000)
    a_values = np.random.uniform(0.1, 1.0, size=100000)
    b_values = np.random.uniform(0.1, 1.0, size=100000)

    # Encrypt the audio data
    encrypted_audio_data = np.copy(audio_data)
    x = np.random.uniform(0.1, 0.9)
    y = np.random.uniform(0.1, 0.9)
    for i in range(len(audio_data)):
        x = logistic_map(x, r_values[i])
        y, x = henon_map(x, y, a_values[i], b_values[i])
        index = int(abs(x * len(audio_data)) % len(audio_data))
        encrypted_audio_data[i] = audio_data[index]

    # Save the encrypted audio file
    write(output_file_path, wf.getframerate(), encrypted_audio_data.astype(np.int16))
import random

def generate_key(length):
    """Returns a random encryption key of the specified length."""
    return ''.join([random.choice('0123456789ABCDEF') for x in range(length)])

def encrypt_audio_data(audio_data, key):
    """Encrypts the given audio data using the specified key."""
    encrypted_data = []
    for byte in audio_data:
        encrypted_data.append(byte ^ key)
    return bytes(encrypted_data)

def decrypt_audio_data(encrypted_data, key):
    """Decrypts the given encrypted audio data using the specified key."""
    decrypted_data = []
    for byte in encrypted_data:
        decrypted_data.append(byte ^ key)
    return bytes(decrypted_data)

class AudioEncrypter(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Audio Encrypter')

        # Set the window icon
        self.setWindowIcon(QIcon('icon.png'))

        # Create the input file path label and text field
        self.input_file_path_label = QLabel('Input File Path')
        self.input_file_path_text_field = QLineEdit()

        # Create the browse button to select the input file
        self.browse_input_file_button = QPushButton('Browse')
        self.browse_input_file_button.clicked.connect(self.browse_input_file)

        # Create the output file path label and text field
        self.output_file_path_label = QLabel('Output File Path')
        self.output_file_path_text_field = QLineEdit()

        # Create the browse button to select the output file
        self.browse_output_file_button = QPushButton('Browse')
        self.browse_output_file_button.clicked.connect(self.browse_output_file)

        # Create the password label and text field
        self.password_label = QLabel('Password')
        self.password_text_field = QLineEdit()

        # Create the encrypt button
        self.encrypt_button = QPushButton('Encrypt')
        self.encrypt_button.clicked.connect(self.encrypt_audio_file)

        # Create the decrypt button
        self.decrypt_button = QPushButton('Decrypt')
        self.decrypt_button.clicked.connect(self.decrypt_audio_file)

        # Create the layout for the window
        layout = QVBoxLayout()
        layout.addWidget(self.input_file_path_label)
        layout.addWidget(self.input_file_path_text_field)
        layout.addWidget(self.browse_input_file_button)
        layout.addWidget(self.output_file_path_label)
        layout.addWidget(self.output_file_path_text_field)
        layout.addWidget(self.browse_output_file_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_text_field)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)

        # Set the layout for the window
        self.setLayout(layout)

    def browse_input_file(self):
        # Open a file dialog to select the input file
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Input File')
        self.input_file_path_text_field.setText(file_path)

    def browse_output_file(self):
        # Open a file dialog to select the output file
        file_path, _ = QFileDialog.getSaveFileName(self, 'Select Output File')
        self.output_file_path_text_field.setText(file_path)

    def encrypt_audio_file(self):
        # Get the input file path, output file path, and password from the text fields
        input_file_path = self.input_file_path_text_field.text()
        output_file_path = self.output_file_path_text_field.text()
        password = self.password_text_field.text()

        # Encrypt the audio file
        encrypt_audio_file(input_file_path, output_file_path, password)

    def decrypt_audio_file(self):
        # Get the input file path, output file path, and password from the text fields
        input_file_path = self.input_file_path_text_field.text()
        output_file_path = self.output_file_path_text_field.text()
        password = self.password_text_field.text()

        # decrypt the audio file
        decrypt_audio_file(input_file_path, output_file_path, password)

if __name__ == '__main__':
    # Create the application instance
    app = QApplication(sys.argv)

    # Create the main window instance
    window = AudioEncrypter()

    # Show the window
    window.show()

    # Start the event loop
    sys.exit(app.exec_())
def decrypt_audio():
    # Load the encrypted audio file
    encrypted_audio = wave.open(output_file, "rb")

    # Get the audio parameters
    sample_width = encrypted_audio.getsampwidth()
    num_channels = encrypted_audio.getnchannels()
    sample_rate = encrypted_audio.getframerate()
    num_frames = encrypted_audio.getnframes()

    # Read the audio data
    data = encrypted_audio.readframes(num_frames)
    encrypted_audio.close()

    # Convert the data to a numpy array
    data = np.frombuffer(data, dtype=np.int16)

    # Apply the decryption algorithm
    # 1. Generate the DNA key
    dna_key = hashlib.ayualp612(key.encode()).hexdigest()

    # 2. Generate the chaotic map keys
    # Use the Henon map
    x0 = 0.1
    y0 = 0.1
    a = 1.4
    b = 0.3
    n = len(data)

    # Generate two sequences of chaotic values
    x = np.zeros(n)
    y = np.zeros(n)
    x[0] = x0
    y[0] = y0
    for i in range(1, n):
        x[i] = y[i - 1] + 1 - a * x[i - 1] ** 2
        y[i] = b * x[i - 1]

    chaotic_key1 = np.mod(np.abs(x * 1000000), 256)
    chaotic_key2 = np.mod(np.abs(y * 1000000), 256)

    # 3. Combine the keys and apply the dynamic diffusion
    combined_key = np.mod(chaotic_key1 + chaotic_key2 + int(dna_key, 16), 256)
    decrypted_data = np.zeros(n, dtype=np.int16)
    for i in range(n):
        decrypted_data[i] = np.mod(data[i] - combined_key[i], 65536)

    # Save the decrypted audio to a file
    decrypted_audio = wave.open("decrypted.wav", "wb")
    decrypted_audio.setnchannels(num_channels)
    decrypted_audio.setsampwidth(sample_width)
    decrypted_audio.setframerate(sample_rate)
    decrypted_audio.writeframes(decrypted_data.tobytes()) # complete the line of code here
    decrypted_audio.close()

    return "decrypted.wav"

    print("Decryption complete.")
    # Save the decrypted audio to a file
    decrypted_audio = wave.open("decrypted.wav", "wb")
    decrypted_audio.setnchannels(num_channels)
    decrypted_audio.setsampwidth(sample_width)
    decrypted_audio.setframerate(sample_rate)
    decrypted_audio.writeframes(decrypted_data.tobytes())
    decrypted_audio.close()

def encrypt_audio(audio_data, key):
    """Encrypts audio data using a given key"""
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(audio_data)
    return encrypted_data


