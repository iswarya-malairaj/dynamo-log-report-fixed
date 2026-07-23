import os
import hashlib
import wave
import pytest

def test_outputs():
    """Verify that the recovered audio matches the golden reference."""
    # Use current directory for local testing, but also support /app/ for Docker
    if os.path.exists('/app'):
        # Running in Docker/Linux environment
        base_path = '/app'
    else:
        # Running locally on Windows
        base_path = os.getcwd()
    
    # Check that output file exists
    output_path = os.path.join(base_path, 'recovered_audio.wav')
    assert os.path.exists(output_path), f"Output file {output_path} not found"
    
    # Read the recovered WAV
    with wave.open(output_path, 'rb') as wav:
        # Verify WAV format requirements from instruction
        assert wav.getframerate() == 44100, f"Expected 44100 Hz, got {wav.getframerate()}"
        assert wav.getnchannels() == 2, f"Expected 2 channels, got {wav.getnchannels()}"
        assert wav.getsampwidth() == 2, f"Expected 16-bit (2 bytes), got {wav.getsampwidth()}"
        
        # Read audio data
        frames = wav.readframes(wav.getnframes())
    
    # Compare against golden reference
    golden_path = os.path.join(base_path, 'golden_reference.wav')
    assert os.path.exists(golden_path), f"Golden reference {golden_path} not found"
    
    # Read the golden WAV
    with wave.open(golden_path, 'rb') as golden_wav:
        # Verify the audio parameters match
        assert golden_wav.getframerate() == wav.getframerate(), "Sample rate mismatch"
        assert golden_wav.getnchannels() == wav.getnchannels(), "Channel count mismatch"
        assert golden_wav.getsampwidth() == wav.getsampwidth(), "Sample width mismatch"
        assert golden_wav.getnframes() == wav.getnframes(), "Frame count mismatch"
        
        # Read golden audio data
        golden_frames = golden_wav.readframes(golden_wav.getnframes())
    
    # Compare the actual audio data
    assert frames == golden_frames, "Audio data does not match golden reference"
    
    # Also verify checksum as a secondary check
    checksum_path = os.path.join(base_path, 'expected_checksum.txt')
    if os.path.exists(checksum_path):
        with open(checksum_path, 'r') as f:
            expected_checksum = f.read().strip()
        
        with open(output_path, 'rb') as f:
            actual_checksum = hashlib.sha256(f.read()).hexdigest()
        
        assert actual_checksum == expected_checksum, f"Checksum mismatch: {actual_checksum} != {expected_checksum}"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_outputs()