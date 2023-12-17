import logging

log = logging.getLogger(__name__)


class EscapeDelimiter:
    PLACEHOLDER = "<ESCAPED_DELIMITER>"

    def _escape_delimiter(self, s: str, delimiter: str = "|") -> str:
        count = s.count(delimiter)
        if count > 0:
            log.warning(
                f"{delimiter=} replacement.", extra={"count": s.count(delimiter)}
            )
        return s.replace(delimiter, self.PLACEHOLDER)

    def combine_strings(self, str1: str, str2: str, delimiter: str = "|") -> str:
        str1_escaped = self._escape_delimiter(str1, delimiter)
        str2_escaped = self._escape_delimiter(str2, delimiter)
        return f"{str1_escaped}{delimiter}{str2_escaped}"

    def _unescape_delimiter(self, s: str, delimiter: str = "|") -> str:
        return s.replace(self.PLACEHOLDER, delimiter)

    def separate_strings(self, combined_str: str, delimiter: str) -> tuple[str, ...]:
        split_str = combined_str.split(delimiter)
        assert len(split_str) <= 2, f"Expected 2 elements, got {len(split_str)}"
        return tuple(self._unescape_delimiter(s) for s in split_str)
