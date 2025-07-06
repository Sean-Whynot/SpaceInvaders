import numpy as np
from scipy.io.wavfile import write

def generate_music(filename="sounds/music.wav", duration=60, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Define a simple melody (frequencies in Hz)
    notes = [
        440.0,  # A4
        523.25, # C5
        659.25, # E5
        523.25, # C5
        440.0,  # A4
        392.0,  # G4
        329.63, # E4
        392.0,  # G4
    ]
    note_duration = 0.5 # seconds per note
    
    waveform = np.zeros_like(t)
    
    for i, note_freq in enumerate(notes * int(duration / (len(notes) * note_duration))):
        start_time = i * note_duration
        end_time = start_time + note_duration
        
        note_t = t[(t >= start_time) & (t < end_time)]
        
        # Simple sine wave for the note
        note_waveform = 0.3 * np.sin(2 * np.pi * note_freq * note_t)
        
        # Apply a simple attack/decay envelope to each note
        envelope = np.ones_like(note_t)
        attack_len = int(0.05 * sample_rate)
        decay_len = int(0.1 * sample_rate)
        
        if len(note_t) > attack_len:
            envelope[:attack_len] = np.linspace(0, 1, attack_len)
        if len(note_t) > decay_len:
            envelope[-decay_len:] = np.linspace(1, 0, decay_len)
            
        waveform[(t >= start_time) & (t < end_time)] += note_waveform * envelope

    # Normalize to -1 to 1
    waveform = waveform / np.max(np.abs(waveform))
    
    # Convert to 16-bit PCM format
    scaled_waveform = np.int16(waveform * 32767)
    
    write(filename, sample_rate, scaled_waveform)

if __name__ == "__main__":
    generate_music()
    print("Generated background music: sounds/music.wav")
