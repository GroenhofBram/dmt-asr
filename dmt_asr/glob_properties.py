from pathlib import Path

from dmt_asr.participantfile import ParticipantFile

def create_participant_file(full_file_path: str, input: str):
    file_path_from_base = full_file_path.replace(input, "")
    pts = Path(file_path_from_base).parts
    file_name = str(pts[1])
    arr = file_name.replace(".wav", "").split("_")
    return ParticipantFile(
        full_file_path=full_file_path,
        word_list=arr[1],
        participant_id=arr[0],
        file_name=file_name,
    )

def generate_file_properties(files_glob: list[str], base_dir: str) -> list[ParticipantFile]:
    participant_files: map[ParticipantFile] = map(lambda file_path: create_participant_file(file_path, base_dir), files_glob)
    # print(list(f_repl)[-1])
    return list(participant_files)