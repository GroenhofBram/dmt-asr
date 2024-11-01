import pytest

def capital_case(s: str) -> str:
    return s.upper()

@pytest.mark.unit
def test_capital_case():
    assert capital_case('sema') == 'SEMA'

@pytest.mark.unit
def test_raises_exception_on_non_string_arguments():
    with pytest.raises(AttributeError):
        capital_case(9)

