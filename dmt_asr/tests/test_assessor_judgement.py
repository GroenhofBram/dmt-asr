import pytest

from dmt_asr.process_confmatrix import calculate_assessor_judgement

@pytest.mark.parametrize("prompt,assessor", [
    ('koe', 'koe'),
    ('koe', 'koo-koe'),
    ('stiefzus', 'stief-z-u-s'),
    ('mineraal', 'adjaskldjmineraalakdasljdl'),
    ("pin", "bin"),
    ("speelgoed", "zbeelkoed")
    # ("p","b")
    # ("k","g")
    # ("s","z")
    # speelgoed -> sbeelgoed [word options for new changes: speelgoed, sbeelgoed]
    # sbeelgoed-> sbeelkoed  [... , sbeelkoed]
    # sbeelgoed -> sbeelgoed
    # sbeelgoed -> zbeelgoed
])
@pytest.mark.unit
def test_assessor_judgement_returns_0_if_transcription_in_prompt(prompt, assessor):
    judgement = calculate_assessor_judgement(prompt, assessor)
    assert judgement == 0

@pytest.mark.parametrize("prompt,assessor", [
    ('koe', 'kopo'),
    ('koe', 'koo'),
    ('stiefzus', 'stiefzoes'),
    ('mineraal', 'mimeraam'),
    ("pin", "bins"),
])
@pytest.mark.unit
def test_assessor_judgement_returns_1_if_transcription_not_in_prompt(prompt, assessor):
    judgement = calculate_assessor_judgement(prompt, assessor)
    assert judgement == 1


@pytest.mark.parametrize("prompt,assessor", [
    # ("pin", "bin"),
    ("pink", "bing")
    # ("speelgoed", "zbeelkoed")
])
@pytest.mark.unit
def test_2(prompt, assessor):
    judgement = calculate_assessor_judgement(prompt, assessor)
    assert judgement == 1