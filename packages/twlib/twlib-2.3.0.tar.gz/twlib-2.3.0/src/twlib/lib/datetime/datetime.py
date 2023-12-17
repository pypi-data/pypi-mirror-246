from datetime import datetime, timezone

import pytz


def is_naive(dt: datetime) -> bool:
    """Return True if datetime object is naive, False otherwise"""
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None


def test_is_naive():
    naive_dt = datetime.now()
    aware_dt = datetime.now(timezone.utc)
    assert is_naive(naive_dt)
    assert not is_naive(aware_dt)


def list_tz(region: str = None) -> list:
    if region is None:
        return pytz.all_timezones
    return [tz for tz in pytz.all_timezones if tz.startswith(region)]


def test_list_tz_with_region():
    region = "Europe"
    result = list_tz(region)
    assert all(
        tz.startswith(region) for tz in result
    ), "Not all timezones start with the specified region"
    assert len(result) > 0, "No timezones found for the specified region"


def test_list_tz_with_non_existing_region():
    region = "NonExistingRegion"
    result = list_tz(region)
    assert len(result) == 0, "Timezones found for a non-existing region"


def test_list_tz_without_region():
    result = list_tz()
    assert len(result) == len(
        pytz.all_timezones
    ), "Not all timezones returned when no region is specified"
