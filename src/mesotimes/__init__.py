"""`mesotimes` - A high-fidelity astronomical and chronological engine for Mesopotamian history."""

# SPDX-FileCopyrightText: 2026-present jccsvq <jccsvq@gmail.com>
#
# SPDX-License-Identifier: MIT

from mesotimes.__about__ import __version__
from mesotimes.date import ChronDate
from mesotimes.astronomy import BabStar


# We define the strict public contract of the root package
__all__ = [
    "__version__",
    "ChronDate",
    "BabStar",
]
