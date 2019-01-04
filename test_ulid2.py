import datetime

import pytest
from ulid2 import (
    decode_ulid_base32, generate_binary_ulid, generate_ulid_as_base32,
    generate_ulid_as_uuid, get_ulid_time, get_ulid_timestamp, InvalidULID,
    ulid_to_base32, ulid_to_binary, ulid_to_uuid
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
        '2016-07-07 14:13:10',
        '2016-07-07 14:13:10',
        '2016-07-07 14:13:10',
    ]:
        dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        ulid = generator(dt, monotonic=True)
        if last:
            assert ulid > last
        last = ulid


def test_ulid_not_monotonic_if_flag_false():
    some_unordered_epoch_ulids = [generate_ulid_as_base32(timestamp=0, monotonic=False) for _ in range(100)]
    assert sorted(some_unordered_epoch_ulids) != some_unordered_epoch_ulids


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


def test_invalid():
    with pytest.raises(InvalidULID):  # invalid length (low-level)
        decode_ulid_base32('What is this')
    with pytest.raises(InvalidULID):  # invalid length (high-level)
        ulid_to_binary('What is this')
    with pytest.raises(InvalidULID):  # invalid characters
        ulid_to_binary('6' + '~' * 25)
    with pytest.raises(InvalidULID):  # invalid type
        ulid_to_binary(8.7)
    with pytest.raises(InvalidULID):  # out of range
        ulid_to_binary('8' + '0' * 25)
    with pytest.raises(InvalidULID):  # out of range
        ulid_to_binary('G' + '0' * 25)
    with pytest.raises(InvalidULID):  # out of range
        ulid_to_binary('R' + '0' * 25)


def test_parses_largest_possible_ulid():
    assert int(get_ulid_timestamp('7ZZZZZZZZZZZZZZZZZZZZZZZZZ') * 1000) == 2 ** 48 - 1
