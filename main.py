import SingingSynthesizer
import utils


if __name__ == "__main__":
    syllableDict = {}
    MID_FILE = "inputs\\happysong.mid"      #旋律midi文件
    LYRICS_FILE = "inputs\\happysong.txt"   #歌词文件

    VOICE_ROOT = "voices\\geping"       #人声音源

    BGM_PATH = "inputs\\piano.wav"          #伴奏

    RESULT_PATH= "outputs\\happysong_geping.wav"  #歌声合成结果
    RESULT_BLEND_PATH = "outputs\\happysong_geping_bgm.wav" #歌声合成加上伴奏


    lyrics = utils.readLyrics(LYRICS_FILE)
    song = utils.getSong(MID_FILE)
    fs=44100  #采样率

    synthesizer = SingingSynthesizer.SingingSynthesizer(VOICE_ROOT,fs)
    synthesizer.voiceSynthesis(lyrics,song)
    synthesizer.saveVoice(RESULT_PATH)

    utils.blendWithBGM(RESULT_PATH,BGM_PATH,fs,RESULT_BLEND_PATH)
