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
