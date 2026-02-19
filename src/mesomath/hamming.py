"""
Generation of Hamming numbers (Regular numbers).
================================================

This module provides functions to generate Hamming numbers, also known as
**Regular numbers**. These are numbers whose prime factors are limited to 2, 3, and 5.

.. math::
   H = 2^i \cdot 3^j \cdot 5^k

with

.. math::
   i, j, k \geq 0

The implementation uses the cyclic generator (method #2) adapted from
`Rosetta Code <https://rosettacode.org/wiki/Hamming_numbers#Python>`_.
The Rosetta Code algorithm is a very elegant and functional implementation
(lazy evaluation style), but its brevity makes it cryptic. It uses generators
and the `tee` function from `itertools` to create self-feeding data streams,
emulating a recursive data structure.

Output Formats
--------------

The module can generate Hamming numbers in three formats:

1. **Python list**: Using the :func:`hamming` function.
2. **CSV**: Using the :func:`genCSV` function for spreadsheet compatibility.
3. **SQL**: Using the :func:`genSQL` function to populate databases.

Database Generation
-------------------

To create the ``regular.db3`` database required by the :class:`BabN` class,
you can pipe the script output directly into the ``sqlite3`` utility:

.. code-block:: bash

    $ python3 hamming.py | sqlite3 regular.db3

.. note::
   All output is directed to ``stdout`` by default.

:Author: jccsvq
:Date: 2025
"""

from itertools import islice, chain, tee
from mesomath.babn import BabN


def hamming(a: int, b: int | None = None) -> list[int]:
    """Generates a list of Hamming's numbers from a to b if b is not None,
    otherwise return a list containig the a-th hamming number only

    :param a: starting number
    :type a: int
    :param b: list ending number, defaults to None
    :type b: int | None, optional
    :return: list of Hamming's numbers
    :rtype: list[int]
    """

    def merge_generators(gen_a, gen_b) -> int:
        """Efficiently merges two sorted generators into a single sorted stream.
        This is a lightweight version of heapq.merge.

        It's a basic mixer. It compares the heads of two sorted streams and returns
        the smaller one. It's the key component for keeping the Hamming numbers list
        sorted without having to re-sort at the end.

        :param gen_a: _description_
        :type gen_a: _type_
        :param gen_b: _description_
        :type gen_b: _type_
        :return: _description_
        :rtype: int
        :yield: _description_
        :rtype: Iterator[int]
        """
        val_a = next(gen_a)
        val_b = next(gen_b)
        while True:
            if val_a < val_b:
                yield val_a
                val_a = next(gen_a)
            else:
                yield val_b
                val_b = next(gen_b)

    def power_generator(prime: int) -> int:
        """Creates an infinite stream of powers of a given prime: p^1, p^2, p^3...

        Generate the basis of the algorithm (the powers of 2).

        :param prime: _description_
        :type prime: int
        :return: _description_
        :rtype: int
        :yield: _description_
        :rtype: Iterator[int]
        """

        def gen():
            val = prime
            while True:
                yield val
                val *= prime

        return gen()

    def multi_prime_generator(prime: int, existing_stream: list[int]) -> list:
        """Creates a new stream that combines an existing stream of Hamming
        numbers with their multiples by a new prime.

        It uses `tee()` to split the generator so it can consume its own
        outputs to produce the next multiples (recursive-like generator).
        This is the magic. It uses `itertools.tee` to create a copy of the
        output stream (feedback_stream). That copy is multiplied by the new
        prime (3 or 5) and mixed back into the original stream. This allows
        the algorithm to "remember" previously generated numbers to produce
        subsequent ones by induction.

        :param prime: _description_
        :type prime: int
        :param existing_stream: _description_
        :type existing_stream: list[int]
        :return: _description_
        :rtype: list
        :yield: _description_
        :rtype: Iterator[list]
        """

        def gen():
            # Merges the base prime and the stream of all previously
            # found Hamming numbers multiplied by this prime.
            for x in merge_generators(
                existing_stream, chain([prime], (prime * y for y in feedback_stream))
            ):
                yield x

        # feedback_stream is a clone used to generate the next multiples
        # of the current prime based on numbers already yielded.
        result_stream, feedback_stream = tee(gen())
        return result_stream

    if not b:
        b = a + 1

    # The Hamming sequence is built by layers:
    # 1. Start with 1.
    # 2. Layer 2: Powers of 2.
    # 3. Layer 3: Hamming numbers using {2, 3}.
    # 4. Layer 4: Hamming numbers using {2, 3, 5}.
    seq = chain(
        [1], multi_prime_generator(5, multi_prime_generator(3, power_generator(2)))
    )

    return list(islice(seq, a - 1, b - 1))


def genCSV(maxn: int, sep: str = ",") -> None:
    """Generates csv table of regular numbers and reciprocals

    genCSV(80000) takes a few seconds! Writes to stdin.

    :param maxn: write the table up to this value
    :type maxn: int
    :param sep: csv field separator, defaults to ","
    :type sep: str, optional
    """
    rlist = hamming(1, maxn)
    i = 0
    BabN.fill = True
    for x in rlist:
        if x % 60 != 0:
            i += 1
            n = BabN(x)
            r = n.rec()
            print(i, n.dec, n, n.len(), r.dec, r, sep=sep)


def genSQL(maxn: int) -> None:
    """Generates list or regular numbers in sqlite3 SQL format

    :param maxn: decimal int, write the table up to this value
    :type maxn: int
    """
    sqlhead = """PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE  IF NOT EXISTS regulars (
    id INTEGER PRIMARY KEY,
    regular    TEXT,
    len     INTEGER
);
"""
    sqltail = """CREATE UNIQUE INDEX regs ON regulars (regular);
COMMIT;
"""

    rlist = hamming(1, maxn)
    i = 0
    BabN.fill = True
    print(sqlhead)
    for x in rlist:
        if x % 60 != 0:
            i += 1
            n = BabN(x)
            print(f"INSERT INTO regulars VALUES({i},'{n}',{n.len()});")
    print(sqltail)


if __name__ == "__main__":
    # The Hamming number #79405 is the last one
    # with 20 sexagesimal digits!
    genSQL(79405)
