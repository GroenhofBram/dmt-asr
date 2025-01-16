from os.path import dirname, join
from glob import glob
import re
from dmt_asr.glob_properties import create_participant_file

from dmt_asr.participantfile import ParticipantFile
from dmt_asr.participant_session import ParticipantSession


def get_textgrid_files_matching_wav(wav_participant_file: ParticipantFile, participant_audio_id: str):
    dir_name = dirname(wav_participant_file.full_file_path)
    glob_path = join(dir_name, f"{participant_audio_id}_checked.TextGrid")
    globs = glob(glob_path)
    # filtered_globs = filter(
    #     lambda pth: re.match(pattern=r"*_checked.TextGrid", string=pth, flags=re.IGNORECASE) != None, 
    #     globs
    # )
    # print(globs)
    return list(globs)

def get_participant_sessions_with_textgrids(
    wav_files: list[ParticipantFile],
    glob_search_base_dir: str,
) -> list[ParticipantSession]:
    participant_sessions: list[ParticipantSession] = []
    for wav_participant_file in wav_files:
        
        participant_audio_id = wav_participant_file.wav_participant_full()
        matching_textgrid_globs = get_textgrid_files_matching_wav(wav_participant_file=wav_participant_file, participant_audio_id=participant_audio_id)
        
        #print(matching_textgrid_globs)

        if len(matching_textgrid_globs) == 0:
            continue
        elif len(matching_textgrid_globs) == 1:
            textgrid_file = create_participant_file(matching_textgrid_globs[0], glob_search_base_dir)
            
            p_sesh = ParticipantSession(
                wav_participant_file=wav_participant_file,
                textgrid_participant_file=textgrid_file,
                participant_audio_id=participant_audio_id
            )
            participant_sessions.append(p_sesh)
        else:
            continue
    return participant_sessions
