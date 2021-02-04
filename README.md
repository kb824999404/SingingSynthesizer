# Singing Synthesizer

The script is used to synthesize songs according to a melody MIDI file and lyrics file

## Requirements

* music21：It's used to read the melody for MIDI file and get the duration and frequency of notes in the melody
* librosa：It's used to synthesis singing voice. The detailed principle is to change the duration and the  frequency of a piece of human voice audio
* pyworld：It's used to extract the fundamental frequency, spectral envelope and aperiodic index of audio, change the fundamental frequency as to change the tone of a syllable and resynthesis the audio from these features
* soundfile：It's used to write the synthesis result to a WAV file

## Usage

You need a melody MIDI file, a lyrics file and a voice source library to synthesis a song. In addition, a bgm WAV file also can be uesd to blend with the synthesis result.

* melody MIDI file：It can only contain a melody, not chords, such as `inputs/happysong.mid`
* lyrics file：Each line contains a syllable corresponding to the file name of the voice source library, such as `inputs/happysong.txt`
* voice source library：Each syllable exists as a individual WAV file, such as `voices/geping` and `voices/google_girl`

### Usage example

```python
python main.py -l inputs\\happysong.txt -m inputs\\happysong.mid -v voices\\geping -o outputs\\happysong_geping.wav -b inputs\\piano.wav -bo outputs\\happysong_geping_bgm.wav
```

