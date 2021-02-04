import music21
import librosa
import soundfile as sf
import numpy as np

#读取歌词
def readLyrics(lyrics_path):
    with open(lyrics_path, 'r') as text:
	    lyrics = text.readlines()
    lyrics = [word.split('\n')[0] for word in lyrics]
    return lyrics


#从midi文件读取乐谱
def getSong(mid_path):
    mid = music21.converter.parse(mid_path)
    # mid.show('text')

    BPM = 0
    for note in mid.recurse():
        if isinstance(note,music21.tempo.MetronomeMark):
            BPM = note.getQuarterBPM()
    print("BPM : {}".format(BPM))


    instruments = music21.instrument.partitionByInstrument(mid)

    for instrument_i in instruments.parts:
        notes_to_parse = instrument_i.recurse()
    

    notes_to_parse = list(filter(lambda element : isinstance(element, music21.note.Note) or 
    isinstance(element, music21.chord.Chord) or
    isinstance(element, music21.note.Rest), notes_to_parse))

    song=[]

    for note in notes_to_parse:
        t = 60.0/BPM *note.duration.quarterLength
        if isinstance(note,music21.note.Rest):
            # print(('Rest',note.duration.quarterLength,t))
            song.append((0,t))
        else:
            # print((note.nameWithOctave,note.duration.quarterLength,note.pitch.frequency,t))
            song.append((note.pitch.frequency,t))

    return song

#将歌声和伴奏混合
def blendWithBGM(voice_path,bgm_path,fs,result_path,factor=[0.5,0.5]):
    voice,_ = librosa.load(voice_path,sr=fs)
    bgm,_ = librosa.load(bgm_path,sr=fs)
    if len(voice) > len(bgm):
        bgm_new = np.zeros(len(voice))
        bgm_new[:len(bgm)] = bgm[:] 
        blend_result = factor[0]*voice + factor[1]*bgm_new
    else:
        voice_new = np.zeros(len(bgm))
        voice_new[:len(voice)] = voice[:]
        blend_result = factor[0]*voice_new + factor[1]*bgm

    sf.write(result_path, blend_result, fs)
    print("Blend Voice And BGM Successfully!")