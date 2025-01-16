def calculate_asr_baseline_judgement(prompt: str, hypothesis: str, hypothesis_rev: str) -> int:
    prompt = str(prompt)
    hypothesis = str(hypothesis)
    hypothesis_rev = str(hypothesis_rev)


    if prompt == hypothesis or prompt == hypothesis_rev:
        return 0
    elif prompt in hypothesis.split() or prompt in hypothesis_rev.split():
        return 0
    else:
        return 1