import numpy as np
from scipy.io.wavfile import write

def generate_laser_sound(filename="sounds/laser.wav", duration=0.1, frequency=440, decay_factor=0.99, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Generate a decaying sine wave
    amplitude = np.exp(-decay_factor * t * 50)  # Exponential decay
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Add a higher frequency component for a 'zap' effect
    waveform += 0.2 * amplitude * np.sin(2 * np.pi * frequency * 4 * t)
    
    # Normalize to -1 to 1
    waveform = waveform / np.max(np.abs(waveform))
    
    # Convert to 16-bit PCM format
    scaled_waveform = np.int16(waveform * 32767)
    
    write(filename, sample_rate, scaled_waveform)

if __name__ == "__main__":
    generate_laser_sound()
    print("Generated laser sound: sounds/laser.wav")
