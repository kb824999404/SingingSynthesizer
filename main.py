import SingingSynthesizer
import utils
import argparse,os


ap = argparse.ArgumentParser()

ap.add_argument("-l", "--lyrics", required=True,    #歌词文件
help="Path to txt file containing the lyrics")
ap.add_argument("-m", "--midi", required=True,      #旋律midi文件
   help="Path to midi file")
ap.add_argument("-v","--voice", required=True,      #人声音源
   help="Path to voice source library")
ap.add_argument("-o", "--output", required=True,    #歌声合成结果
   help="Path to synthesis result")

ap.add_argument("-b", "--bgm", required=False,     #伴奏
   help="Path to bgm wav file")
ap.add_argument("-bo", "--bgm_output", required=False,     #歌声合成加上伴奏
   help="Path to result with bgm")

args = ap.parse_args()


def create_dir_not_exist(path):
    for length in range(1, len(path.split(os.path.sep))-1):
        check_path = os.path.sep.join(path.split(os.path.sep)[:(length+1)])
        if not os.path.exists(check_path):
            os.mkdir(check_path)
            print(f'Created Dir: {check_path}')


if __name__ == "__main__":
    MID_FILE = args.midi      #旋律midi文件
    LYRICS_FILE = args.lyrics   #歌词文件

    VOICE_ROOT = args.voice       #人声音源

    BGM_PATH = args.bgm          #伴奏

    RESULT_PATH= args.output  #歌声合成结果
    RESULT_BLEND_PATH = args.bgm_output #歌声合成加上伴奏

    create_dir_not_exist(RESULT_PATH)

    lyrics = utils.readLyrics(LYRICS_FILE)
    song = utils.getSong(MID_FILE)
    fs=44100  #采样率

    synthesizer = SingingSynthesizer.SingingSynthesizer(VOICE_ROOT,fs)
    synthesizer.voiceSynthesis(lyrics,song)
    synthesizer.saveVoice(RESULT_PATH)

    if BGM_PATH:
        create_dir_not_exist(RESULT_BLEND_PATH)
        utils.blendWithBGM(RESULT_PATH,BGM_PATH,fs,RESULT_BLEND_PATH)
