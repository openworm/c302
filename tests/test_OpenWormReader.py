import logging

import pytest

from c302.OpenWormReader import format_muscle_name


class TestFormatMuscleName:
    @pytest.mark.parametrize(
        "name, name_expected, log_count_expected, assert_msg",
        [
            ("ADER", "ADER", 1, "Unknown muscle name format was not logged."),
            ("MVL01", "MVL01", 0, "Known muscle name format was unexpectedly logged."),
        ],
    )
    def test_should_log_unknown_name_format(
        self,
        name: str,
        name_expected: str,
        log_count_expected: int,
        assert_msg: str,
        caplog,
    ) -> None:
        caplog.set_level(logging.DEBUG)

        format_muscle_name(name)

        assert (
            len(caplog.records) == log_count_expected
        ), f"The incorrect quantity of logs was recorded."

    @pytest.mark.parametrize(
        "name, name_expected, assert_msg",
        [
            ("ADER", "ADER", "Unknown muscle name format was incorrectly formatted"),
            ("MVL01", "MVL01", "Known muscle name format was incorrectly formatted"),
            (
                "VR01",
                "MVR01",
                "Known muscle name format missing 'M' was incorrectly formatted",
            ),
            ("MDL01", "MDL01", "Muscle name with 'DL' was incorrectly formatted"),
            ("MDR01", "MDR01", "Muscle name with 'DR' was incorrectly formatted"),
            (
                "MVD01",
                "MVD01",
                "Unknown muscle name format with 'VD' was incorrectly formatted",
            ),
        ],
    )
    def test_should_format_muscle_name(
        self, name: str, name_expected: str, assert_msg: str, caplog
    ) -> None:
        caplog.set_level(logging.DEBUG)
        name_formatted: str = format_muscle_name(name)
        assert name_formatted == name_expected, assert_msg
