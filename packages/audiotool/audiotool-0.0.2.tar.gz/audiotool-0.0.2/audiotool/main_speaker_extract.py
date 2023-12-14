import argparse
import shutil
import time
import os
import numpy as np
from collections import OrderedDict
from audiotool.get_audio_timestamp import extract_audio_to_file
from pydub import AudioSegment
from .pipeline_annote import get_annote_result
from .pipeline_ms import get_result_ms
# import torchaudio.lib.libtorchaudio
from pprint import pprint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default=None)
    parser.add_argument("-m", "--model", type=str, default="annote")
    parser.add_argument("-t", "--target", type=str, default=None, help="target folder")
    args = parser.parse_args()

    if args.model == 'annote':
        speakers = get_annote_result(args.file)
    else:
        speakers = get_result_ms(args.file)
    pprint(speakers)

    name = os.path.basename(args.file).split(".")[0]
    # save the most speaker into a folder by the length
    speakers_lens_gather = OrderedDict()
    for sp in speakers:
        # print(sp["speaker"])
        if sp["speaker"] in speakers_lens_gather.keys():
            speakers_lens_gather[sp["speaker"]] += sp["unit_len"]
        else:
            speakers_lens_gather[sp["speaker"]] = sp["unit_len"]
    print(speakers_lens_gather)

    most_speaker = np.argmax(speakers_lens_gather.values())
    most_speaker = list(speakers_lens_gather.keys())[most_speaker]
    print("most speaker: ", most_speaker)
    target_folder = f"results/{name}"
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    os.makedirs(target_folder, exist_ok=True)
    for i, sp in enumerate(speakers):
        if sp["speaker"] == most_speaker:
            s = sp["start"]
            e = sp["end"]
            extract_audio_to_file(s, e, args.file, f"{target_folder}/{i}.mp3")

    # concate all mp3 files into one
    mp3_files = [f for f in os.listdir(target_folder) if f.endswith(".mp3")]
    mp3_files.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    # Initialize an empty audio segment
    combined = AudioSegment.empty()
    for mp3_file in mp3_files:
        sound = AudioSegment.from_mp3(os.path.join(target_folder, mp3_file))
        combined += sound
    combined.export(f"{target_folder}/final_concat.mp3", format="mp3")


if __name__ == "__main__":
    main()
