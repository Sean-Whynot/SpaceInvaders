import numpy as np
from scipy.io.wavfile import write

def generate_explosion_sound(filename="sounds/explosion.wav", duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Generate white noise
    noise = np.random.uniform(-1, 1, len(t))
    
    # Apply an exponential decay envelope
    envelope = np.exp(-5 * t / duration)  # Adjust the '5' for faster/slower decay
    
    waveform = noise * envelope
    
    # Add a low-frequency thump for more impact
    thump_frequency = 50  # Hz
    thump = 0.5 * np.sin(2 * np.pi * thump_frequency * t) * envelope
    waveform += thump
    
    # Normalize to -1 to 1
    waveform = waveform / np.max(np.abs(waveform))
    
    # Convert to 16-bit PCM format
    scaled_waveform = np.int16(waveform * 32767)
    
    write(filename, sample_rate, scaled_waveform)

if __name__ == "__main__":
    generate_explosion_sound()
    print("Generated explosion sound: sounds/explosion.wav")
