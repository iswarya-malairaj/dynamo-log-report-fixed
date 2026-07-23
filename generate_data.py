import numpy as np
import struct
import hashlib

# Generate test audio
sample_rate = 44100
duration = 2  # seconds
num_samples = int(sample_rate * duration)

# Create left and right channels with different content
t = np.linspace(0, duration, num_samples, endpoint=False)
left = np.sin(2 * np.pi * 440 * t) * 16383  # Use lower amplitude to avoid overflow when shifting
right = np.sin(2 * np.pi * 880 * t) * 16383  # Use lower amplitude to avoid overflow when shifting

left = left.astype(np.int16)
right = right.astype(np.int16)

# Write golden reference (original stereo WAV)
with open('golden_reference.wav', 'wb') as f:
    # WAV header (simplified)
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + num_samples * 4))
    f.write(b'WAVEfmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))  # PCM
    f.write(struct.pack('<H', 2))  # stereo
    f.write(struct.pack('<I', sample_rate))
    f.write(struct.pack('<I', sample_rate * 4))
    f.write(struct.pack('<H', 4))  # block align
    f.write(struct.pack('<H', 16)) # bits per sample
    f.write(b'data')
    f.write(struct.pack('<I', num_samples * 4))
    
    # Write interleaved samples
    for i in range(num_samples):
        f.write(struct.pack('<h', int(left[i])))
        f.write(struct.pack('<h', int(right[i])))

# Simulate I2S corruption: swap channels AND shift left channel by 1 bit (invertible)
# Store: first sample = right shifted left, second sample = left shifted left (both invertible)
with open('corrupted_i2s.bin', 'wb') as f:
    # Header: sample rate (binary) + padding
    f.write(struct.pack('<I', sample_rate))
    f.write(b'\x00' * 60)
    
    # Corrupted data: right channel << 1, left channel << 1
    for i in range(num_samples):
        # Ensure values stay within int16 range when shifted
        right_val = int(right[i])
        left_val = int(left[i])
        
        # Shift left by 1, but ensure it doesn't overflow
        # Use a safe conversion: convert to int32, shift, then convert back to int16
        right_shifted = np.int16(np.int32(right_val) << 1)
        left_shifted = np.int16(np.int32(left_val) << 1)
        
        f.write(struct.pack('<h', right_shifted))
        f.write(struct.pack('<h', left_shifted))

# Calculate checksum for golden reference
with open('golden_reference.wav', 'rb') as f:
    checksum = hashlib.sha256(f.read()).hexdigest()
with open('expected_checksum.txt', 'w') as f:
    f.write(checksum)

print("Generated golden_reference.wav and corrupted_i2s.bin")
print(f"Sample rate: {sample_rate} Hz")
print(f"Duration: {duration} seconds")
print(f"Total samples: {num_samples}")