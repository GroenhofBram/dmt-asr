from re import sub as regex_sub
from transformers import pipeline
from faster_whisper import WhisperModel

from dmt_asr.participantfile import ParticipantFile
from dmt_asr.cuda import DEVICE

def load_model(MODEL: str, VAD_decision: str):
    if MODEL == "GroNLP/wav2vec2-dutch-large-ft-cgn":
        MODEL_LOADED = pipeline(model=MODEL, device=DEVICE)
        model_name = "Wav2Vec2.0-CGN"
    elif MODEL == "Systran/faster-whisper-large-v2":
        MODEL_LOADED = WhisperModel("large-v2", device = DEVICE)
        if VAD_decision == "y":
            model_name = "Faster-Whisper-Large-v2_VAD"
        else:     
            model_name = "Faster-Whisper-Large-v2"    
    
    return MODEL_LOADED, model_name


def transcribe_ASR(input_participant_wav_file: ParticipantFile, MODEL: str, MODEL_LOADED, VAD_decision: str) -> str:\
    # Letterster: Tier 4 = prompts, Tier 1 = orthographic transcription
    file_path = input_participant_wav_file.full_file_path

    if MODEL == "GroNLP/wav2vec2-dutch-large-ft-cgn":
        output = MODEL_LOADED(file_path, chunk_length_s=10, stride_length_s=(4, 2))
        ASR_transcription = regex_sub(r'\s+', ' ', output['text'])
        ASR_transcription = regex_sub(r"[?.!,\"\'`:\-;]", "", ASR_transcription)
        ASR_transcription = ASR_transcription.lower()
    
    elif MODEL == "Systran/faster-whisper-large-v2":
        if VAD_decision == "y":
            segments, info = MODEL_LOADED.transcribe(file_path, vad_filter = True)
        else:     
            segments, info = MODEL_LOADED.transcribe(file_path)


        ASR_transcription = ""

        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            ASR_transcription = ASR_transcription + segment.text
            ASR_transcription = regex_sub(r'\s+', ' ', ASR_transcription)
            ASR_transcription = regex_sub(r"[?.!,\"\'`:\-;]", "", ASR_transcription)
            ASR_transcription = ASR_transcription.lower()



    return ASR_transcription