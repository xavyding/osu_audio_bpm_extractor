import os
import json


OSU_DIR = r"path to your osu! folder"


#########################################################################################################
def data_extractor(Osu_dir = OSU_DIR, save=True):
    song_dir = Osu_dir +  "/Songs"
    song_folders = os.listdir(song_dir)
    
    dict = {}
    for song in song_folders:
        song = song_dir + r'/' + song

        for file in os.listdir(song):
            Audio = None
            Bpm = None
            Offset = None
            
            if file.endswith(".osu") and (Audio is None) and (Bpm is None):
                filename = song+r'/'+file
                with open(filename, 'r', encoding="utf8") as f:
                    lines = f.read().split('\n')
                    checktiming = False
                    try:
                        for i,line in enumerate(lines):
                            if checktiming == True and (Bpm is None) and (Offset is None):
                                decode = line.split(',')
                                if float(decode[1]) > 0:
                                    Offset = float(decode[0])
                                    Bpm= 1000.0/float(decode[1])*60.0

                            if 'AudioFilename: ' in line:
                                Audio = line[len('AudioFilename: '):]
                            elif 'TimingPoints' in line:
                                checktiming = True

                            if Audio and Bpm and Offset:
                                break
                    except:
                        print('failed processing {}'.format(filename))

                if Audio and Bpm and Offset:
                    dict[song] = (Audio, Bpm, Offset)
    if save:
        with open("Osu_song_data_ABO.json", "w") as outfile: 
            json.dump(dict, outfile)

    
if __name__ == "__main__":
    data_extractor(Osu_dir = OSU_DIR, save=True)