import datetime

import pytest

from ulid2 import (
    generate_binary_ulid, generate_ulid_as_base32, generate_ulid_as_uuid,
    get_ulid_time, ulid_to_base32, ulid_to_binary, ulid_to_uuid
)


@pytest.mark.parametrize('generator', [
    generate_ulid_as_base32,
    generate_ulid_as_uuid,
])
def test_ulid_time_monotonic(generator):
    last = None
    for time in [
        '2002-08-14 10:10:10',
        '2008-01-01 08:24:40',
        '2013-12-01 10:10:10',
        '2016-07-07 14:12:10',
        '2016-07-07 14:13:10',
    ]:
        dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        ulid = generator(dt)
        if last:
            assert ulid > last
        last = ulid


def test_ulid_sanity():
    # https://github.com/RobThree/NUlid/blob/master/NUlid.Tests/UlidTests.cs#L14
    assert generate_ulid_as_base32(1469918176.385).startswith('01ARYZ6S41')


def test_ulid_base32_length():
    assert len(generate_ulid_as_base32()) == 26


def test_ulid_binary_length():
    assert len(generate_binary_ulid()) == 128 / 8


def test_get_time():
    dt = datetime.datetime(2010, 1, 1, 15, 11, 13)
    ulid = generate_ulid_as_base32(dt)
    assert get_ulid_time(ulid) == dt


def test_conversion_roundtrip():
    ulid = generate_binary_ulid()
    encoded = ulid_to_base32(ulid)
    uuid = ulid_to_uuid(ulid)
    assert ulid_to_binary(uuid) == ulid_to_binary(ulid)
    assert ulid_to_binary(encoded) == ulid_to_binary(ulid)
