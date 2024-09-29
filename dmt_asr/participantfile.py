from dataclasses import dataclass
from os.path import basename, dirname, join
from glob import glob

@dataclass
class ParticipantFile:
    full_file_path: str
    word_list: str
    participant_id: str
    file_name: str

    def base_path(self):
        return basename(self.full_file_path)

    def wav_participant_full(self):
        return self.file_name.replace(".wav", "")