(tutorialmultable)=
# `bmultable` Tutorial

`bmultable` is a simple utility for printing sexagesimal multiplication tables in the style of those that aspiring scribes in ancient Babylon struggled to memorize.

> [IMPORTANT] This application is obsolete and will be removed in the upcoming version 2.0.0. We strongly recommend that you use method `.multable()` instead from now on.

## Running `bmultable`

If you [installed](installation)  `MesoMath` using `pip`, `pipx` or `hatch`, you only have to issue:

```bash
$ bmultable
usage: bmultable [-h] [-s SEPARATOR] [-p] [-f] mult
bmultable: error: the following arguments are required: mult
```

The above output indicates that `bmultable` is there, but you haven't told it what to do. You can try also:

```bash
$ python -m mesomath.bmultable
```

to run `bmultable`.

### Options

```bash
$ bmultable -h
usage: bmultable [-h] [-s SEPARATOR] [-p] [-c] [-z] [-f] [--float] mult

Prints Babylonian multiplication tables.

positional arguments:
  mult                  Multiplier, use 0 for a list of multiplication tables
                        used in scribal learning

options:
  -h, --help            show this help message and exit
  -s SEPARATOR, --separator SEPARATOR
                        Sexagesimal digit separator (default: :)
  -p, --principal       Use only principal numbers (default: False)
  -c, --cuneiform       Output is cuneiform (default: False)
  -z, --zeros           strike out empty spaces (default: False)
  -f, --fill            Pad with zeros (default: False)
  --float               floating results (default: False)

jccsvq dub-sar fecit, 2025. Public domain.
```

### List of tables learned by the scribes

The list comprised only regular numbers and their reciprocals as multipliers... plus the number 7! You can obtain a listing of the tables by issuing:


    $ bmultable 0

    STANDARD MULTIPLIERS TABLE
    Value        | Reciprocal
    -------------------------
    50           |       1:12
    45           |       1:20
    44:26:40     |       1:21
    40           |       1:30
    36           |       1:40
    30           |          2
    25           |       2:24
    24           |       2:30
    22:30        |       2:40
    20           |          3
    18           |       3:20
    16:40        |       3:36
    16           |       3:45
    15           |          4
    12:30        |       4:48
    12           |          5
    10           |          6
    9            |       6:40
    8:20         |       7:12
    8            |       7:30
    7:30         |          8
    7:12         |       8:20
    Not regular, (igi nu)!
    7            |       None
    6:40         |          9
    6            |         10
    5            |         12
    4:30         |      13:20
    4            |         15
    3:45         |         16
    3:20         |         18
    3            |         20
    2:30         |         24
    2:24         |         25
    2            |         30
    1:40         |         36
    1:30         |         40
    1:20         |         45
    1:15         |         48


### Example

The following prints the multiplication table for sexagesimal number `1:12`. Options `-p --principal` limit multiplicand to the list of *principal numbers*. Without this option the table includes al multiplicands between 1 and 59.


    $ bmultable 1:12 -p

    |  i  |        i * 1:12|
    |-----|----------------|
    |  1  |            1:12|
    |  2  |            2:24|
    |  3  |            3:36|
    |  4  |            4:48|
    |  5  |             6:0|
    |  6  |            7:12|
    |  7  |            8:24|
    |  8  |            9:36|
    |  9  |           10:48|
    | 10  |            12:0|
    | 11  |           13:12|
    | 12  |           14:24|
    | 13  |           15:36|
    | 14  |           16:48|
    | 15  |            18:0|
    | 16  |           19:12|
    | 17  |           20:24|
    | 18  |           21:36|
    | 19  |           22:48|
    | 20  |            24:0|
    | 30  |            36:0|
    | 40  |            48:0|
    | 50  |           1:0:0|


>**Note**: As you can see, the previous outputs are in **Markdown table format**, so if you use Markdown for your documents, you're in luck, you just have to copy and paste the result from the terminal into your document and that's it. But you can also paste it into an intermediate `.csv` file that can be read by any spreadsheet (indicating the pipe `|` character as the column separator) and from there you can copy and paste it into your word processor or presentations.

With the `-f --fill` option, the sexagesimal digits are padded with zeros if necessary:


    $ bmultable 1:12 -pf

    |  i  |        i * 1:12|
    |-----|----------------|
    |  1  |           01:12|
    |  2  |           02:24|
    |  3  |           03:36|
    |  4  |           04:48|
    |  5  |           06:00|
    |  6  |           07:12|
    |  7  |           08:24|
    |  8  |           09:36|
    |  9  |           10:48|
    | 10  |           12:00|
    | 11  |           13:12|
    | 12  |           14:24|
    | 13  |           15:36|
    | 14  |           16:48|
    | 15  |           18:00|
    | 16  |           19:12|
    | 17  |           20:24|
    | 18  |           21:36|
    | 19  |           22:48|
    | 20  |           24:00|
    | 30  |           36:00|
    | 40  |           48:00|
    | 50  |        01:00:00|


Use `--float` option for floating results:


    $ bmultable 1:12 -p --float

    |  i  |        i * 1:12|
    |-----|----------------|
    |  1  |            1:12|
    |  2  |            2:24|
    |  3  |            3:36|
    |  4  |            4:48|
    |  5  |               6|
    |  6  |            7:12|
    |  7  |            8:24|
    |  8  |            9:36|
    |  9  |           10:48|
    | 10  |              12|
    | 11  |           13:12|
    | 12  |           14:24|
    | 13  |           15:36|
    | 14  |           16:48|
    | 15  |              18|
    | 16  |           19:12|
    | 17  |           20:24|
    | 18  |           21:36|
    | 19  |           22:48|
    | 20  |              24|
    | 30  |              36|
    | 40  |              48|
    | 50  |               1|


Finally, you can also change the sexagesimal digit separator with the `-s --separator` option:


    $ bmultable 1:12 -pfs .

    |  i  |        i * 1:12|
    |-----|----------------|
    |  1  |           01.12|
    |  2  |           02.24|
    |  3  |           03.36|
    |  4  |           04.48|
    |  5  |           06.00|
    |  6  |           07.12|
    |  7  |           08.24|
    |  8  |           09.36|
    |  9  |           10.48|
    | 10  |           12.00|
    | 11  |           13.12|
    | 12  |           14.24|
    | 13  |           15.36|
    | 14  |           16.48|
    | 15  |           18.00|
    | 16  |           19.12|
    | 17  |           20.24|
    | 18  |           21.36|
    | 19  |           22.48|
    | 20  |           24.00|
    | 30  |           36.00|
    | 40  |           48.00|
    | 50  |        01.00.00|


## Cuneiform

### 𒍻 1. Cuneiform Font Requirement

To prevent "tofu" (empty boxes) or broken characters, your system or document compiler must have access to a compatible font. We recommend **Noto Sans Cuneiform**, which covers the Sumero-Akkadian Unicode block.

Consult [Font Configuration](#install-font) for more information.

𒍻

### 𒍻 Examples

The cuneiform tablets are modeled according to the way they were practiced by scribe apprentices. It includes the text "a-rá" (𒀀𒁺, "times").

    $ bmultable 33 -p --float -cz

    |    𒌍𒐗  𒀀𒁺  𒐕  |    𒌍𒐗 |
    |---------------|-------|
    |        𒀀𒁺   𒐖 |  𒐕  𒐚 |
    |        𒀀𒁺   𒐗 |  𒐕 𒌍𒑆 |
    |        𒀀𒁺   𒐘 |  𒐖 𒌋𒐖 |
    |        𒀀𒁺   𒐙 |  𒐖 𒑩𒐙 |
    |        𒀀𒁺   𒐚 |  𒐗 𒌋𒑄 |
    |        𒀀𒁺   𒑂 |  𒐗 𒑪𒐕 |
    |        𒀀𒁺   𒑄 |  𒐘 𒎙𒐘 |
    |        𒀀𒁺   𒑆 |  𒐘 𒑪𒑂 |
    |        𒀀𒁺  𒌋  |  𒐙 𒌍  |
    |        𒀀𒁺  𒌋𒐕 |  𒐚  𒐗 |
    |        𒀀𒁺  𒌋𒐖 |  𒐚 𒌍𒐚 |
    |        𒀀𒁺  𒌋𒐗 |  𒑂  𒑆 |
    |        𒀀𒁺  𒌋𒐘 |  𒑂 𒑩𒐖 |
    |        𒀀𒁺  𒌋𒐙 |  𒑄 𒌋𒐙 |
    |        𒀀𒁺  𒌋𒐚 |  𒑄 𒑩𒑄 |
    |        𒀀𒁺  𒌋𒑂 |  𒑆 𒎙𒐕 |
    |        𒀀𒁺  𒌋𒑄 |  𒑆 𒑪𒐘 |
    |        𒀀𒁺  𒌋𒑆 | 𒌋  𒎙𒑂 |
    |        𒀀𒁺  𒎙  |    𒌋𒐕 |
    |        𒀀𒁺  𒌍  | 𒌋𒐚 𒌍  |
    |        𒀀𒁺  𒑩  |    𒎙𒐖 |
    |        𒀀𒁺  𒑪  | 𒎙𒑂 𒌍  |

The previous cuneiform output should appear correctly aligned on almost any modern terminal; but, due to the variable width of the cuneiform glyphs, it is next to impossible to get it to appear aligned in an HTML document like this using a monospaced font, so henceforth the outputs will be presented in table format.

    $ bmultable 33 -p --float -cz

|    𒌍𒐗  𒀀𒁺  𒐕  |    𒌍𒐗 |
|--------------:|-------|
|        𒀀𒁺   𒐖 |  𒐕  𒐚 |
|        𒀀𒁺   𒐗 |  𒐕 𒌍𒑆 |
|        𒀀𒁺   𒐘 |  𒐖 𒌋𒐖 |
|        𒀀𒁺   𒐙 |  𒐖 𒑩𒐙 |
|        𒀀𒁺   𒐚 |  𒐗 𒌋𒑄 |
|        𒀀𒁺   𒑂 |  𒐗 𒑪𒐕 |
|        𒀀𒁺   𒑄 |  𒐘 𒎙𒐘 |
|        𒀀𒁺   𒑆 |  𒐘 𒑪𒑂 |
|        𒀀𒁺  𒌋  |  𒐙 𒌍  |
|        𒀀𒁺  𒌋𒐕 |  𒐚  𒐗 |
|        𒀀𒁺  𒌋𒐖 |  𒐚 𒌍𒐚 |
|        𒀀𒁺  𒌋𒐗 |  𒑂  𒑆 |
|        𒀀𒁺  𒌋𒐘 |  𒑂 𒑩𒐖 |
|        𒀀𒁺  𒌋𒐙 |  𒑄 𒌋𒐙 |
|        𒀀𒁺  𒌋𒐚 |  𒑄 𒑩𒑄 |
|        𒀀𒁺  𒌋𒑂 |  𒑆 𒎙𒐕 |
|        𒀀𒁺  𒌋𒑄 |  𒑆 𒑪𒐘 |
|        𒀀𒁺  𒌋𒑆 | 𒌋  𒎙𒑂 |
|        𒀀𒁺  𒎙  |    𒌋𒐕 |
|        𒀀𒁺  𒌍  | 𒌋𒐚 𒌍  |
|        𒀀𒁺  𒑩  |    𒎙𒐖 |
|        𒀀𒁺  𒑪  | 𒎙𒑂 𒌍  |


We can try some large numbers:

$ bmultable 33.1:12.45.48 -p --float -cz

<div class="tablet ">

| 𒌍𒐗  𒐕 𒌋𒐖 𒑩𒐙 𒑩𒑄  𒀀𒁺  𒐕  |    𒌍𒐗  𒐕 𒌋𒐖 𒑩𒐙 𒑩𒑄 |
|-----------------------:|-------------------|
|                 𒀀𒁺   𒐖 |  𒐕  𒐚  𒐖 𒎙𒐙 𒌍𒐕 𒌍𒐚 |
|                 𒀀𒁺   𒐗 |  𒐕 𒌍𒑆  𒐗 𒌍𒑄 𒌋𒑂 𒎙𒐘 |
|                 𒀀𒁺   𒐘 |  𒐖 𒌋𒐖  𒐘 𒑪𒐕  𒐗 𒌋𒐖 |
|                 𒀀𒁺   𒐙 |     𒐖 𒑩𒐙  𒐚  𒐗 𒑩𒑆 |
|                 𒀀𒁺   𒐚 |  𒐗 𒌋𒑄  𒑂 𒌋𒐚 𒌍𒐘 𒑩𒑄 |
|                 𒀀𒁺   𒑂 |  𒐗 𒑪𒐕  𒑄 𒎙𒑆 𒎙  𒌍𒐚 |
|                 𒀀𒁺   𒑄 |  𒐘 𒎙𒐘  𒑆 𒑩𒐖  𒐚 𒎙𒐘 |
|                 𒀀𒁺   𒑆 |  𒐘 𒑪𒑂 𒌋  𒑪𒐘 𒑪𒐖 𒌋𒐖 |
|                 𒀀𒁺  𒌋  |     𒐙 𒌍  𒌋𒐖  𒑂 𒌍𒑄 |
|                 𒀀𒁺  𒌋𒐕 |  𒐚  𒐗 𒌋𒐗 𒎙  𒎙𒐗 𒑩𒑄 |
|                 𒀀𒁺  𒌋𒐖 |  𒐚 𒌍𒐚 𒌋𒐘 𒌍𒐗  𒑆 𒌍𒐚 |
|                 𒀀𒁺  𒌋𒐗 |  𒑂  𒑆 𒌋𒐙 𒑩𒐙 𒑪𒐙 𒎙𒐘 |
|                 𒀀𒁺  𒌋𒐘 |  𒑂 𒑩𒐖 𒌋𒐚 𒑪𒑄 𒑩𒐕 𒌋𒐖 |
|                 𒀀𒁺  𒌋𒐙 |     𒑄 𒌋𒐙 𒌋𒑄 𒌋𒐕 𒎙𒑂 |
|                 𒀀𒁺  𒌋𒐚 |  𒑄 𒑩𒑄 𒌋𒑆 𒎙𒐘 𒌋𒐖 𒑩𒑄 |
|                 𒀀𒁺  𒌋𒑂 |  𒑆 𒎙𒐕 𒎙  𒌍𒐚 𒑪𒑄 𒌍𒐚 |
|                 𒀀𒁺  𒌋𒑄 |  𒑆 𒑪𒐘 𒎙𒐕 𒑩𒑆 𒑩𒐘 𒎙𒐘 |
|                 𒀀𒁺  𒌋𒑆 | 𒌋  𒎙𒑂 𒎙𒐗  𒐖 𒌍  𒌋𒐖 |
|                 𒀀𒁺  𒎙  |     𒌋𒐕 𒃵 𒎙𒐘 𒌋𒐙 𒌋𒐚 |
|                 𒀀𒁺  𒌍  |    𒌋𒐚 𒌍  𒌍𒐚 𒎙𒐖 𒑪𒐘 |
|                 𒀀𒁺  𒑩  |     𒎙𒐖 𒃵 𒑩𒑄 𒌍  𒌍𒐖 |
|                 𒀀𒁺  𒑪  |     𒎙𒑂 𒌍𒐕 𒃵 𒌍𒑄 𒌋  |

</div>

---

<center>

<strong><big> 𒍻 jccsvq 𒁾𒊬  𒐞𒐞𒐞 𒐗 𒐏 𒐋 </big></strong>

</center>


