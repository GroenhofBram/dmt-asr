from glob import glob
from os.path import join, exists
from os import makedirs
import os
from dmt_asr.combine_judgement_files import combine_judgement_files, export_combined_judgement_df
from dmt_asr.generalisedbasedir import get_base_dir_for_generalised_path
from dmt_asr.model_load_transcribe import load_model, transcribe_ASR
from dmt_asr.participantsession import get_participant_sessions_with_textgrids
from dmt_asr.pathing import get_base_dir_folder_path
from dmt_asr.glob_properties import generate_file_properties
import pandas as pd

from dmt_asr.process_confmatrix import fill_assessor_judgements, process_conf_matrix
from dmt_asr.textgrid import use_text_grids

def main():
    MODEL = "GroNLP/wav2vec2-dutch-large-ft-cgn"
    #MODEL = "Systran/faster-whisper-large-v2"
    
    input(f"-----------------------------------------------------------\nProvided model\t: {MODEL}.\nPress any key to continue...\n-----------------------------------------------------------\t")
    VAD_decision = input("\n\n- - - - - Type 'y' for VAD, type anything else for no VAD - - - - - \n\n")

    base_dir = get_base_dir_for_generalised_path()
    base_output_dir_in_repo = get_base_dir_folder_path("output", MODEL, VAD_decision)
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
    input("\n\tIf correct, press any key to continue\n\t")


    failed_runs = []
    
    MODEL_LOADED, model_name = load_model(MODEL, VAD_decision)

    transcriptions_DF = pd.DataFrame(columns=["participant", "word_list_id", model_name])

    existing_dfs = glob(f"{base_output_dir_in_repo}/*/*.csv", recursive=True)
    print(f"\n\n----- Found {len(existing_dfs)} existing DFs for this model, adding them-----\n\n")

    for df in existing_dfs:
        curr_df = pd.read_csv(df)  # Read the current CSV file
        transcriptions_DF = pd.concat([transcriptions_DF, curr_df], ignore_index=True)
    
    print(transcriptions_DF)
    input("- - - - - This is what the DF looks like (empty if new model). press any key to continue and start ASR-transcription generation- - - - - \t")

    total_sessions = len(participant_sessions)

# TODO: Regenerate evrything 
    for i, sesh in enumerate(participant_sessions, start=1):
        if sesh.participant_audio_id in existing_output_dirs:
            print(f"\nSKIPPING: {sesh.participant_audio_id} BECAUSE IT ALREADY EXISTS\n")
        else:
            print("\n\t ====================================================================")
            print(f"\nCURRENTLY PROCESSING {sesh} (Session {i} of {total_sessions})")
            print("\n\t ====================================================================")
            try:
                base_session_folder = join(base_output_dir_in_repo, sesh.participant_audio_id)
                makedirs(base_session_folder, exist_ok=True)

                tgt_df_repr = use_text_grids(
                    sesh.textgrid_participant_file.full_file_path,
                    sesh.textgrid_participant_file.participant_id,
                    sesh.textgrid_participant_file.word_list
                )
                #print(tgt_df_repr)
                #print(f"^^^ALIGNED ORTHOGRAPHIC TRANSCRIPTION FOR\t {sesh.participant_audio_id}^^^") # Store in similar way as transcriptins
                
                ASR_transcription = transcribe_ASR(sesh.wav_participant_file, MODEL, MODEL_LOADED, VAD_decision)

                print(f"\n ASR TRANSCRIPTION FOR {sesh.participant_audio_id}")
                print(f"\t{ASR_transcription}")
                print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")

                # print(f"\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~ ASR_transcription\t:{ASR_transcription}\npart_audio_id\t:{sesh.participant_audio_id}\nbase_folde:\t{base_session_folder}\ntgt_df_repr\t:{tgt_df_repr} ~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n")


                print(f"+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\nProcessing ConfMat for\t:{sesh.participant_audio_id}+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
                process_conf_matrix(
                    asr_transcriptions=ASR_transcription, 
                    participant_audio_id=sesh.participant_audio_id, 
                    base_session_folder=base_session_folder,
                    ortho_df=tgt_df_repr,
                )                

                new_row = pd.DataFrame([{
                    "participant": sesh.textgrid_participant_file.participant_id,
                    "word_list_id": sesh.textgrid_participant_file.word_list,
                    model_name: ASR_transcription 
                }])
                print(f"\nNEW ROW: \t{new_row}\n")
                transcriptions_DF = pd.concat([transcriptions_DF, new_row], ignore_index=True)

                row_csv_filename = f"{sesh.participant_audio_id}.csv"
                row_csv_filepath = join(base_session_folder, row_csv_filename)

                # Check if CSV already exists and append if it does
                if exists(row_csv_filepath):
                    new_row.to_csv(row_csv_filepath, mode='a', header=False, index=False)
                    print(f"Appended new row to existing CSV at {row_csv_filepath}")
                else:
                    new_row.to_csv(row_csv_filepath, index=False)
                    print(f"Exported new row to {row_csv_filepath}")

            except Exception as e:
                msg = e
                if hasattr(e, 'message'):
                    msg = e.message

                failed_runs.append({
                    'id': sesh.participant_audio_id,
                    'ex': msg
                })

    if len(failed_runs) > 0:  
        print(failed_runs)
    
    

    transcript_filepath = os.path.join("output", model_name + "_transcriptions.csv")
    print(f"Saving Transcription DF to...:\n\t{transcript_filepath}")
    transcriptions_DF.to_csv(transcript_filepath, index=False)


    existing_judgement_filepaths = glob(f"{base_output_dir_in_repo}/**/all_data/*.csv", recursive=True)
    combined_judgements_df = combine_judgement_files(existing_judgement_filepaths)

    


    # Use all data to generate confusion matrices
    combined_judgements_df_filled = fill_assessor_judgements(combined_judgements_df)
    combined_judgements_output_filepath = os.path.join("output", model_name + "_judgements.csv")
    print(combined_judgements_df_filled[27:50])
    print(f"Saving Judgements DF to...:\n\t{combined_judgements_output_filepath}")   
    export_combined_judgement_df(combined_judgements_df_filled, combined_judgements_output_filepath)

