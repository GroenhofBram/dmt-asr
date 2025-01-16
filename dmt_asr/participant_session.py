from dataclasses import dataclass

from dmt_asr.participantfile import ParticipantFile

@dataclass
class ParticipantSession:
    textgrid_participant_file: ParticipantFile
    wav_participant_file: ParticipantFile
    participant_audio_id: str

@dataclass
class ProcessedParticipantSession:
    base_session_folder: str


