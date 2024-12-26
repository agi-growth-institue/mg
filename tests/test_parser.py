from mg.parser import create_exercise_dict, fill_none_with_previous, parser


def test_parser():
    data = """
    2024-11-25
    S 4,5,6
    K 4 4,5 6,6
    """
    result = parser.parse(data)

    expected = (
        "2024-11-25",
        [
            ("S", [(None, 4), (None, 5), (None, 6)]),
            ("K", [(4, 4), (5, 6), (None, 6)]),
        ],
    )
    assert result == expected


def test_fill_none_with_previous():
    assert fill_none_with_previous([(None, 4), (None, 5), (None, 6)]) == [
        (0, 4),
        (0, 5),
        (0, 6),
    ]
    assert fill_none_with_previous([(4, 4), (5, 6), (None, 6)]) == [
        (4, 4),
        (5, 6),
        (5, 6),
    ]
    assert fill_none_with_previous([(None, 4), (5, 6), (None, 6)]) == [
        (0, 4),
        (5, 6),
        (5, 6),
    ]
    assert fill_none_with_previous([(4, 4), (None, 6), (None, 6)]) == [
        (4, 4),
        (4, 6),
        (4, 6),
    ]


def test_create_exercise_dict():
    exercises = [
        ("S", [(None, 5), (None, 5), (None, 8)]),
        ("Ht", [(70, 12), (70, 12), (70, 12)]),
        ("Pu", [(None, 8), (None, 6), (None, 6)]),
        ("Incbp", [(16, 12), (18, 12), (18, 12)]),
    ]
    expected_result = {
        "S": {"reps": [5, 5, 8], "intensity": [0, 0, 0]},
        "Ht": {"reps": [12, 12, 12], "intensity": [70, 70, 70]},
        "Pu": {"reps": [8, 6, 6], "intensity": [0, 0, 0]},
        "Incbp": {"reps": [12, 12, 12], "intensity": [16, 18, 18]},
    }
    assert create_exercise_dict(exercises) == expected_result
