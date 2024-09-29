from glob import glob
from os import makedirs
import os
from generalisedbasedir import get_base_dir_for_generalised_path
from participantsession import get_participant_sessions_with_textgrids
from pathing import get_base_dir_folder_path
from glob_properties import generate_file_properties


def main():
    MODEL = "GroNLP/wav2vec2-dutch-large-ft-cgn"
    input(f"-----------------------------------------------------------\nProvided model\t: {MODEL}.\nPress any key to continue...\n-----------------------------------------------------------\t")


    base_dir = get_base_dir_for_generalised_path()
    base_output_dir_in_repo = get_base_dir_folder_path("output", MODEL)
    print(f"\nBase Dir\t:{base_dir}\nBase Output Dir\t:{base_output_dir_in_repo}")

    makedirs(base_output_dir_in_repo, exist_ok=True)
    print(f"Directory {base_output_dir_in_repo} has been created")

    wav_files = glob(f"{base_dir}/**/*.wav", recursive=True)
    input(f"Found {len(wav_files)} .wav files in {base_dir}\n Press any key to continue\t")

    wav_files_with_properties = generate_file_properties(wav_files, base_dir)
    participant_sessions = get_participant_sessions_with_textgrids(wav_files_with_properties, base_dir)

    print(f"{participant_sessions}\n")
    print(f"--------------------------------------------\nWav Files with properties\t: {len(wav_files_with_properties)}")
    print(f"Found sessions\t: {len(participant_sessions)}\n--------------------------------------------")

    existing_output_dirs = os.listdir(base_output_dir_in_repo)
    print("\n- - - EXISTING DIRECTORIES AT START OF PROCESS, THESE WILL BE SKIPPED - - -")
    print(f"{existing_output_dirs}")
    print(f"\n- - - TOTAL SKIPPED:\t{len(existing_output_dirs)}- - -")
    input("\n\tIF THIS IS CORRECT PRESS ANY KEY TO START ASR-TRANSCRIPTION GENERATION!\n\t")



