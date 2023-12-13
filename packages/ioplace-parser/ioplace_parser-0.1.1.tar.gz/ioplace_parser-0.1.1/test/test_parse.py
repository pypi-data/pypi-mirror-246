# Copyright 2020-2023 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from decimal import Decimal

import pytest


def test_parse():
    from ioplace_parser import parse, Order

    example_path = os.path.join(pytest.test_root, "example", "complex.cfg")
    example_str = open(example_path, encoding="utf8").read()

    example_parsed = parse(example_str)

    assert example_parsed["N"].min_distance == Decimal(
        "0.42"
    ), "min distance not set for north"

    for side in ["E", "W", "S"]:
        assert (
            example_parsed[side].min_distance is None
        ), "min distance set for unset side"

    for side in ["N", "E", "W"]:
        assert (
            example_parsed[side].sort_mode is Order.bitMajor
        ), f"global @bit_major annotation did not affect side {side}"

    assert (
        example_parsed["S"].sort_mode == Order.busMajor
    ), "per-direction @bus_major annotation did not affect S"


def test_global_min():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "globals.cfg")
    example_str = open(example_path, encoding="utf8").read()

    example_parsed = parse(example_str)
    for side in ["N", "E", "W", "S"]:
        assert example_parsed[side].min_distance == Decimal(
            "0"
        ), f"min distance unset for {side} with global option"


def test_syntax_error():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "grammar_error.cfg")

    example_str = open(example_path, encoding="utf8").read()

    with pytest.raises(ValueError, match="Syntax Error"):
        parse(example_str)


def test_unknown_annotation():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "unknown_annotation.cfg")
    example_str = open(example_path, encoding="utf8").read()

    with pytest.raises(ValueError, match="Unknown annotation"):
        parse(example_str)


def test_misused_value():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "misused_value.cfg")
    example_str = open(example_path, encoding="utf8").read()

    with pytest.raises(ValueError, match=r"Annotation \w+ cannot be assigned a value"):
        parse(example_str)


def test_missing_value():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "missing_value.cfg")
    example_str = open(example_path, encoding="utf8").read()

    with pytest.raises(ValueError, match=r"Annotation \w+ requires a value"):
        parse(example_str)


def test_dep_annotation():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "deprecated_bus_sort.cfg")
    example_str = open(example_path, encoding="utf8").read()

    with pytest.warns(
        UserWarning,
        match=r"Specifying bit-major using the direction token \(\'\#BUS_SORT\'\) is deprecated",
    ):
        parse(example_str)


def test_invalid_vpin():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "invalid_virtual.cfg")
    example_str = open(example_path, encoding="utf8").read()

    with pytest.raises(
        ValueError,
        match=r"virtual pin declaration \$\d+ requires a direction to be set first",
    ):
        parse(example_str)


def test_invalid_pin():
    from ioplace_parser import parse

    example_path = os.path.join(pytest.test_root, "example", "invalid_pin.cfg")
    example_str = open(example_path, encoding="utf8").read()

    with pytest.raises(
        ValueError,
        match=r"identifier/regex [^ ]+ requires a direction to be set first",
    ):
        parse(example_str)
