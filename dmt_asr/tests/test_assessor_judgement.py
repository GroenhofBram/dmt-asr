import pytest

from dmt_asr.process_confmatrix import calculate_assessor_judgement

@pytest.mark.parametrize("prompt,assessor", [
    ('koe', 'koe'),
    ('koe', 'koo-koe-koo'),
    ('stiefzus', 'stief-z-u-s'),
    ("pin", "bin"),
    ("speelgoed", "zbeelkoed"),
    ("zager", "s-z-zager"),
    ("zager", "zager-s"),
    ("klok", "g-log"),
    ("zoen", "zoen zoen"),
    ("ren", "ren ruin "),
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
    ("rug", "terug")
])
@pytest.mark.unit
def test_assessor_judgement_returns_1_if_transcription_not_in_prompt(prompt, assessor):
    judgement = calculate_assessor_judgement(prompt, assessor)
    assert judgement == 1


@pytest.mark.parametrize("prompt,assessor", [
    ("pin", "bin"),
    ("pink", "bing"),
    ("speelgoed", "zbeelkoed"),
    ("dkdkktktkktskzk", "dgdkktktkktzkzk")
])
@pytest.mark.unit
def test_2(prompt, assessor):
    judgement = calculate_assessor_judgement(prompt, assessor)
    assert judgement == 0