from twlib.lib.string.escape_delimiter import EscapeDelimiter


class TestEscaping:
    import pytest

    @pytest.mark.parametrize(
        "input_str, delimiter, expected",
        [
            ("hello|world", "|", f"hello{EscapeDelimiter.PLACEHOLDER}world"),
            (
                "test||string",
                "|",
                f"test{EscapeDelimiter.PLACEHOLDER}{EscapeDelimiter.PLACEHOLDER}string",
            ),
            ("no|delimiter", "/", "no|delimiter"),
            (
                "multiple|delimiters|here",
                "|",
                f"multiple{EscapeDelimiter.PLACEHOLDER}delimiters{EscapeDelimiter.PLACEHOLDER}here",
            ),
        ],
    )
    def test_escape_delimiter(self, input_str, delimiter, expected):
        assert EscapeDelimiter()._escape_delimiter(input_str, delimiter) == expected

    @pytest.mark.parametrize(
        "str1, str2, delimiter, expected",
        [
            ("hello", "world", "|", "hello|world"),
            ("test", "string", "|", "test|string"),
            (
                "str|with|delimiter",
                "another|string",
                "|",
                f"str{EscapeDelimiter.PLACEHOLDER}with{EscapeDelimiter.PLACEHOLDER}delimiter|another{EscapeDelimiter.PLACEHOLDER}string",
            ),
            ("str1", "str2", "/", "str1/str2"),
        ],
    )
    def test_combine_strings(self, str1, str2, delimiter, expected):
        assert EscapeDelimiter().combine_strings(str1, str2, delimiter) == expected

    @pytest.mark.parametrize(
        "input_str, delimiter, expected",
        [
            (f"hello{EscapeDelimiter.PLACEHOLDER}world", "|", "hello|world"),
            ("no||delimiter", "/", "no||delimiter"),
            (
                f"multiple{EscapeDelimiter.PLACEHOLDER}delimiters{EscapeDelimiter.PLACEHOLDER}here",
                "|",
                "multiple|delimiters|here",
            ),
        ],
    )
    def test_unescape_delimiter(self, input_str, delimiter, expected):
        assert EscapeDelimiter()._unescape_delimiter(input_str, delimiter) == expected

    @pytest.mark.parametrize(
        "combined_str, delimiter, expected",
        [
            ("hello|world", "|", ("hello", "world")),
            ("test|string", "|", ("test", "string")),
            (
                f"str{EscapeDelimiter.PLACEHOLDER}with{EscapeDelimiter.PLACEHOLDER}delimiter|another{EscapeDelimiter.PLACEHOLDER}string",
                "|",
                ("str|with|delimiter", "another|string"),
            ),
            ("str1/str2", "/", ("str1", "str2")),
            (f"hello{EscapeDelimiter.PLACEHOLDER}world", "|", ("hello|world",)),
            (
                f"hello|{EscapeDelimiter.PLACEHOLDER}world",
                "|",
                (
                    "hello",
                    "|world",
                ),
            ),  # TODO: ("hello", "|world",)
            (
                f"hello{EscapeDelimiter.PLACEHOLDER}|world",
                "|",
                (
                    "hello|",
                    "world",
                ),
            ),  # TODO: ("hello", "|world",)
        ],
    )
    def test_separate_strings(self, combined_str, delimiter, expected):
        assert EscapeDelimiter().separate_strings(combined_str, delimiter) == expected

    @pytest.mark.parametrize(
        "input, delimiter, expected",
        [
            (
                ("hello|", "world"),
                "|",
                (
                    "hello|",
                    "world",
                ),
            ),  # TODO: ("hello", "|world",)
            (
                ("hello", "|world"),
                "|",
                (
                    "hello",
                    "|world",
                ),
            ),  # TODO: ("hello", "|world",)
        ],
    )
    def test_escape_unescape(self, input, delimiter, expected):
        combined = EscapeDelimiter().combine_strings(input[0], input[1], delimiter)
        separated = EscapeDelimiter().separate_strings(combined, delimiter)
        assert separated == expected
