import librosa
import soundfile as sf
import numpy as np
from scipy import interpolate 
import pyworld as pw
import sys,os


class SingingSynthesizer:
    def __init__(self,voiceRoot,fs=44100):
        self.syllableDict = {}
        self.fs = fs #采样率
        self.voiceRoot = voiceRoot
    
    #歌声合成
    def voiceSynthesis(self,lyrics,song):  
        print("Lyrics Length:{}\tSong Length:{}".format(len(lyrics),len(song)))
        print("Begin to synthesis...") 
        result = None
        i_lyrics = i_note = 0
        while i_lyrics < len(lyrics) and i_note < len(song):
            word = lyrics[i_lyrics]
            note = song[i_note]
            if note[0] == 0:    #休止符
                syllable = None
            else:
                syllable = self.getSyllable(word)
                i_lyrics += 1
            data_new = self.generateSingingSyllable(note,syllable)
            if i_note==0:
                result=data_new
            else:
                result=np.concatenate((result,data_new),axis=0) 
            i_note += 1
            print("Note {}".format(i_note))
        self.synthesisResult = result
        print("Synthesis Successfully!") 

    #保存结果
    def saveVoice(self,result_path):     
        sf.write(result_path, self.synthesisResult, self.fs)
        print("Save Synthesis Result Successfully!")


    #获取音节的音频数据
    def getSyllableAudio(self,syllable_name):
        data, fs = librosa.load(os.path.join(self.voiceRoot,syllable_name+".wav"),self.fs)
        return data,fs

    #获取音节数据，如果没读取过就读取文件并将其放进字典中，否则直接从字典中获取
    def getSyllable(self,syllable_name):
        if syllable_name in self.syllableDict:
            return self.syllableDict[syllable_name]
        else:
            data, fs = self.getSyllableAudio(syllable_name)
            data_clip = clipAudio(data,50)
            duration= librosa.get_duration(data,self.fs)
            duration_clip = librosa.get_duration(data_clip,self.fs)
            syllable = (data,duration,data_clip,duration_clip)
            self.syllableDict[syllable_name] = syllable
            return syllable

    #改变音调
    def changeFreq(self,data,freq_target):
        data= data.astype(np.float)
        f0, sp, ap = pw.wav2world(data, self.fs)
        f0_positive = np.array([f for f in f0 if f>0])
        if len(f0_positive)==0:
            return data
        f0_mean = np.mean(f0_positive)
        f0_new = f0 *freq_target/f0_mean
        synthesized = pw.synthesize(f0_new, sp, ap, self.fs, pw.default_frame_period)
        return synthesized

    #语音音节转歌声
    def generateSingingSyllable(self,note,syllable):
        freq,duration_new = note
        if freq == 0:
            data_new = getRest(self.fs,duration_new)
        else:
            data,duration,data_clip,duration_clip = syllable
            if duration_new/duration<0.3:       #缩放系数太大要用较短的音频
                data_new = audioResize(data_clip,duration_clip,duration_new)
            else:
                data_new = audioResize(data,duration,duration_new)
        data_new = self.changeFreq(data_new,freq)

        return data_new


 
#改变音频长度
def audioResize(data,t_origin,t_new,kind="cubic"):
    len_origin=len(data)
    len_new=int(len_origin*t_new/t_origin)
    if len_origin>len_new:
        x=np.arange(len_origin)
        f=interpolate.interp1d(x,data,kind=kind)
        x_new=np.linspace(0,len_origin-1,len_new)
        data_new=f(x_new)
    else:
        data_new = np.pad(data,int((len_new-len_origin)/2))
    return data_new

#截取有声音频
def clipAudio(data,padding=10,minwidth=10):
    start =minwidth
    end = len(data)-minwidth
    clip_start , clip_end = start ,end
    for i in range(start,end):
        if data[i] == 0 and not data[i+1] ==0:
            if all(data[i-minwidth:i]) == 0:
                clip_start = i
    for i in range(end,start,-1):
        if data[i] == 0 and not data[i-1] ==0:
            if all(data[i:i+minwidth]) == 0:
                clip_end = i
    data_clip = np.array(data[clip_start:clip_end])
    data_clip = np.pad(data_clip,pad_width=padding)
    return data_clip


#生成一段无声音频
def getRest(fs,t):
    return np.zeros(int(fs*t))







