'''
Test helper functions to aid with the game.
'''
import pytest
from swag_helpers import sign

sign_cases = [(1, 1), (-1.0, -1), (-32, -1),
              (43, 1), (-2134, -1), (0, 1),
              (-0, 1), (-192420, -1), (1.1, 1)]


@pytest.mark.parametrize("number, sign_answer", sign_cases)
def test_sign(number, sign_answer):
    """
    Check that running the sign function returns a 1 with the correct sign,
    either - or +.
    Args:
        number: number of which to get the sign
        sign_answer: the sign of the input number
    """
    assert sign(number) == sign_answer
