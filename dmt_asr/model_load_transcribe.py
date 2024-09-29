from re import sub as regex_sub
from transformers import pipeline
from faster_whisper import WhisperModel

from dmt_asr.participantfile import ParticipantFile
from dmt_asr.cuda import DEVICE

def load_model(MODEL: str):
    if MODEL == "GroNLP/wav2vec2-dutch-large-ft-cgn":
        MODEL_LOADED = pipeline(model=MODEL, device=DEVICE)
    elif MODEL == "Systran/faster-whisper-large-v2":
        MODEL_LOADED = WhisperModel("large-v2", device = DEVICE)      
    
    return MODEL_LOADED


def transcribe_ASR(input_participant_wav_file: ParticipantFile, MODEL: str, MODEL_LOADED) -> str:\
    # CHOREC: Tier 4 = prompts, Tier 1 = orthographic transcription
    file_path = input_participant_wav_file.full_file_path

    if MODEL == "GroNLP/wav2vec2-dutch-large-ft-cgn":
        output = MODEL_LOADED(file_path, chunk_length_s=10, stride_length_s=(4, 2))
        ASR_transcription = regex_sub(r'\s+', ' ', output['text'])
        ASR_transcription = regex_sub(r'[?.!,]', '', ASR_transcription)
    
    elif MODEL == "Systran/faster-whisper-large-v2":
        segments, info = MODEL_LOADED.transcribe(file_path)
        ASR_transcription = ""

        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            ASR_transcription = ASR_transcription + segment.text



    return ASR_transcription