import pytest

import jaccs


def test_dots_access(json_obj):
    dots = jaccs.Dots(json_obj)

    assert dots._ == json_obj
    assert dots.key == json_obj['key']
    assert dots.sequence == jaccs.Dots(json_obj['sequence'])
    assert dots.sequence._ == json_obj['sequence']
    assert dots.sequence[0] == json_obj['sequence'][0]
    assert dots.mapping == jaccs.Dots(json_obj['mapping'])
    assert dots.mapping._ == json_obj['mapping']
    assert dots.mapping.key == json_obj['mapping']['key']
    assert dots.mapping.sequence[-1] == json_obj['mapping']['sequence'][-1]


def test_dots_raises(json_obj):
    dots = jaccs.Dots(json_obj)

    with pytest.raises(KeyError):
        dots.nope

    with pytest.raises(IndexError):
        dots.sequence[99]

    with pytest.raises(TypeError):
        dots.sequence.nope
