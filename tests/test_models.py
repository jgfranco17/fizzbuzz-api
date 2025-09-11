from typing import List

import pytest

from api.core.models import FizzBuzzSequence


@pytest.mark.parametrize(
    "sequence,fizz,buzz",
    [
        (["1"], 0, 0),
        (["1", "2", "Fizz", "4", "Buzz"], 1, 1),
        (["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz"], 3, 2),
    ],
)
def test_fizzbuzz_model(sequence: List[str], fizz: int, buzz: int):
    generated_model = FizzBuzzSequence.from_sequence(sequence)
    assert (
        generated_model.fizz == fizz
    ), f"Expected fizz count of {fizz} but got {generated_model.fizz}"
    assert (
        generated_model.buzz == buzz
    ), f"Expected buzz count of {buzz} but got {generated_model.buzz}"
    assert len(generated_model) == len(sequence)
