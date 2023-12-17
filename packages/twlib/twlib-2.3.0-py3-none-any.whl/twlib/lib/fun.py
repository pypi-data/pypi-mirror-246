import webbrowser  # noqa
from hashlib import md5
from typing import NewType

Url = NewType("Url", str)


def build_avatar_url(name: str, type_="monsterid") -> Url:
    """returns url for an Avatar

    :param name: e.g. email
    :param type_: [monsterid, wavatar, retro, robohash, identicon, mp, blank]
    :return:
    """
    digest = md5(str(name).encode("utf-8")).hexdigest()
    return Url(f"http://www.gravatar.com/avatar/{digest}?d={type_}")


def test_build_avatar_url():
    name = "test@example.com"
    type_ = "monsterid"
    digest = md5(name.encode("utf-8")).hexdigest()

    expected_url = Url(f"http://www.gravatar.com/avatar/{digest}?d={type_}")
    actual_url = build_avatar_url(name, type_)

    assert actual_url == expected_url
    # webbrowser.open(actual_url)
