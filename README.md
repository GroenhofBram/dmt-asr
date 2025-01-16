# Setting up the Code
This code was written using Python 3.11 and [Poetry](https://python-poetry.org/), but you can use the requirements.txt.

It is aimed to use the LETTERSTER data. Please ensure that you use this data only. If you use different data, you will have to modify the code and adapt it so that it works with .TextGrid files that are structured differently.

For this script to work ensure that the .TextGrid files have the following 4 tiers: ORT-MAU, KAN-MAU, MAU, and Prompt. For this project All of the relevant .TextGrid files have a name ending in `_checked.TextGrid`.

Also ensure that you have access to the word lists used in this dataset too, and that they are stored in the `repo/files_static/kaart1A.txt`. A file should exist for `kaart1A.txt`, `kaart2A.txt`, `kaart3A.txt`, `kaart1B.txt`, `kaart2B.txt`, and `kaart3B.txt`. They should contain all words in the word list, with a space separating them. For example: `opa rekening stralend`. 

# Using the Code
The main script is found in dmt_asr/dmt-asr.py. This code is heavily commented. When running it, you will be prompted to ensure that the correct model is selected, the right number of files are present, etc.

# Current Working Models
This version of the code can run using 2 models: [Wav2Vec2.0-CGN](https://huggingface.co/GroNLP/wav2vec2-dutch-large-ft-cgn) and [Faster-Whisper-v2](https://huggingface.co/Systran/faster-whisper-large-v2)). 

Furthermore, the `VAD_decision` parameter in the code allows you to turn the VAD filter on or off, if it exists for the model.

# Known issues
The code succesfully generates transcriptions, aligned transcriptions with ADDAGT, and confusion matrix values (TN, TP, FN, FP) based on the transcriptions. These are stored in .csv files. However:
- Any transcription of any model using "kaart3A.txt" or "kaart3B.txt" seems to go wrong. The transcriptions are generated succesfully, but when aligning them all of the ASR's hypotheses are replaced by "*"s. 
