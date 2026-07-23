# Recover I2S Audio

## Background
An audio recording was captured using an I2S digital microphone interface, but due to a configuration error, the data was stored incorrectly:

- **Channel order was swapped**: Left and right channels are reversed in the stored data
- **Bit alignment offset**: One channel's data is shifted by 1 bit

Your task is to recover the original stereo audio by identifying and correcting these corruption patterns.

## Input Data
The file `/app/corrupted_i2s.bin` contains:
- **Header**: First 4 bytes = sample rate (little-endian uint32, typically 44100 Hz)
- **Padding**: Next 60 bytes are padding (all zeros)
- **Audio Data**: Interleaved 16-bit PCM samples (each sample is a signed 16-bit integer)

The data was stored as two channels interleaved, but:
1. The channel order is swapped in the storage (right channel data appears where left channel should be, and vice versa)
2. One channel's sample values were bit-shifted before storage (invertible shift operation)

## Requirements
Your solution must:
1. Read the corrupted I2S data from `/app/corrupted_i2s.bin`
2. Detect and correct the channel ordering and bit alignment issues
3. Write the recovered stereo audio as a standard WAV file to `/app/recovered_audio.wav`
4. The output must be:
   - 44100 Hz sample rate
   - 2 channels (stereo)
   - 16-bit PCM format

## Evaluation
The verifier will:
- Check that the output WAV file exists and has correct format parameters
- Compare the recovered audio data against a golden reference
- Verify that the audio is successfully recovered to match the original

## Hints
- The corruption is deterministic and consistent throughout the file
- Focus on identifying the sample-level transformations that were applied
- The recovery process should be the inverse of the corruption
- All necessary Python libraries (numpy, wave) are available in the environment

## Time Limit
You have 600 seconds to complete this task.

Good luck!