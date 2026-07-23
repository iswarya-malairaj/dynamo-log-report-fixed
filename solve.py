import struct
import wave
import numpy as np

def recover_i2s_audio(input_file='corrupted_i2s.bin', output_file='recovered_audio.wav'):
    # Read the corrupted I2S data
    with open(input_file, 'rb') as f:
        # Read header (sample rate)
        sample_rate = struct.unpack('<I', f.read(4))[0]
        # Skip padding (60 bytes)
        f.read(60)
        
        # Read all audio data
        data = f.read()
    
    # Parse as 16-bit samples (interleaved: right_channel_shifted, left_channel_shifted)
    samples = np.frombuffer(data, dtype=np.int16)
    
    # Since we have pairs of samples: [right<<1, left<<1, right<<1, left<<1, ...]
    # Extract right and left channels by shifting back
    right_shifted = samples[0::2]
    left_shifted = samples[1::2]
    
    # Recover original by shifting right (invertible since we shifted left)
    right = (right_shifted >> 1).astype(np.int16)
    left = (left_shifted >> 1).astype(np.int16)
    
    # Interleave for WAV output (left, right order)
    interleaved = np.empty(len(left) + len(right), dtype=np.int16)
    interleaved[0::2] = left
    interleaved[1::2] = right
    
    # Write WAV file
    with wave.open(output_file, 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)  # 16-bit = 2 bytes
        wav.setframerate(sample_rate)
        wav.writeframes(interleaved.tobytes())
    
    print(f"Recovered audio saved to {output_file}")

if __name__ == "__main__":
    recover_i2s_audio()