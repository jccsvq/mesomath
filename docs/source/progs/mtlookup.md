
(mtlookup-tutorial)=
# `mtlookup` Tutorial


## Introduction

`mtlookup` is a Python3 command line application based on [MesoMath](https://github.com/jccsvq/mesomath) to search for the abstract number that corresponds to a measure or to list measures that correspond to a given abstract number (option: `-r`).

## Running `mtlookup`

If you [installed](installation)  `MesoMath` using `pip`, `pipx` or `hatch`, you only have to issue:

```bash
$ mtlookup
usage: mtlookup [-h] [-t {L,Lh,S,V,C,W,SysG,SysS}] [-r] [-f FORCE] [-v] [-F {0,1}] [-p] [-s] [-a] VALUE
mtlookup: error: the following arguments are required: VALUE
```

The above output indicates that `mtlookup` is there, but you haven't told it what to do. You can try also:

```bash
$ python -m mesomath.mtlookup
```

to run `mtlookup`.

### Options:

Use `-h` or `--help` to see the options:


```bash
$ mtlookup --help
usage: mtlookup [-h] [-t {L,Lh,S,V,C,W,B,SysG,SysS}] [-r] [-f FORCE] [-v]
                [-F {0,1}] [-p] [-s] [-a]
                VALUE

Prints abstract number corresponding to a meassure or lists measures having an
abstract number.

positional arguments:
  VALUE                 Value

options:
  -h, --help            show this help message and exit
  -t {L,Lh,S,V,C,W,B,SysG,SysS}, --type {L,Lh,S,V,C,W,B,SysG,SysS}
                        Metrology to use (default: None)
  -r, --reverse         Reverse lookup ,lists measures having an abstract
                        number (default: False)
  -f FORCE, --force FORCE
                        Force base unit to number FORCE (default: -1)
  -v, --verbose         Prints more information (default: False)
  -F {0,1}, --fractions {0,1}
                        Use fractions, -F 1 to include 1/6 (default: -1)
  -p, --pedantic        Write the coefficients of the units in the
                        measurements using the S and G Systems (default:
                        False)
  -s, --strict          Suppress partial matches in reverse lookup. (default:
                        False)
  -a, --academic        With [-F|--fractions] or [-r|--remainder] uses the
                        academic names of units. (default: False)

jccsvq fecit, 2025. Public domain.
```

### Metrologies

Metrology is selected with the options `-t` or `--type`:

* L:   length meassurements
* Lh:   length meassurements (Heights)
* S:   surface meassurements
* V:   volume meassurements
* C:   capacity meassurements
* W:   weight meassurements
* B:   brick counts
* SysS:   System S to count objects
* SysG:   System G to count objects

### Direct search

Return the abstract value corresponding to a measurement in a given metrology.

```bash
$ mtlookup -t L '1 us 30 ninda'
1 us 30 ninda  ->  1:30
```

You can use the verbose options `-v` or `--verbose`:

```bash
$ mtlookup -t L '1 us 30 ninda' --verbose

Abstract number for Babylonian length meassurement
    Base unit:  ninda
===================================================
1 us 30 ninda  ->  1:30 Reciprocal:  40
```


### Reverse search

With the `-r` or `--reverse` options you get a list of measures that match the given abstract number:

```bash
$ mtlookup -t L 1.30 -r

Looking for Babylonian length meassurement with Abstract = 1:30
Base reference unit: ninda
----------------------------------------------------------------
10800 danna          <- 1:30
180 danna            <- 1:30
3 danna              <- 1:30
1 us 30 ninda        <- 1:30
1 ninda 6 kus        <- 1:30
9 susi               <- 1:30

```

```bash
$ mtlookup -t L 1.30 -r -v

Looking for Babylonian length meassurement with Abstract = 1:30
Base reference unit: ninda
----------------------------------------------------------------
Meassure:   10800 danna
Equiv.:   116640000.0 meters
Abstract: 1:30

Meassure:   180 danna
Equiv.:   1944000.0 meters
Abstract: 1:30

Meassure:   3 danna
Equiv.:   32400.0 meters
Abstract: 1:30

Meassure:   1 us 30 ninda
Equiv.:   540.0 meters
Abstract: 1:30

Meassure:   1 ninda 6 kus
Equiv.:   9.0 meters
Abstract: 1:30

Meassure:   9 susi
Equiv.:   0.15 meters
Abstract: 1:30
```

In some cases, due to the discrete nature of the measurements and rounding, the last rows of the list only show approximate values:

```bash
$ mtlookup -r -t L 6.40.38 -w 30

Looking for Babylonian length meassurement with Abstract = 6:40:38
Base reference unit: ninda
-------------------------------------------------------------------
2884560 danna                  <- 6:40:38
48076 danna                    <- 6:40:38
801 danna 8 us                 <- 6:40:38
13 danna 10 us 38 ninda        <- 6:40:38
6 us 40 ninda 7 kus 18 susi    <- 6:40:38
6 ninda 8 kus 3 susi           <- 6:40:30
1 kus 10 susi                  <- 6:40
```


you can use options `-s --strict` to suppress them:

```bash
$ mtlookup -r -t L 6.40.38 -sw 30

Looking for Babylonian length meassurement with Abstract = 6:40:38
Base reference unit: ninda
-------------------------------------------------------------------
2884560 danna                  <- 6:40:38
48076 danna                    <- 6:40:38
801 danna 8 us                 <- 6:40:38
13 danna 10 us 38 ninda        <- 6:40:38
6 us 40 ninda 7 kus 18 susi    <- 6:40:38
```

###  Pedantic mode

Options `-p` `--pedantic` will print the coefficients of the units expressed in the system S  (system G for surfaces and volumes) making the output more closely mimic the way the measurements were actually inscribed on the clay tablets, but it complicates things for the modern reader:

```bash
$ mtlookup -t V '128 gan 133 se' -p
(7 bur 2 iku) gan (7 bur 1 ese 1 iku) se  ->  3:33:20:0:44:20
```

```bash
$ mtlookup -t V 3:33:20:0:44:20 -prw 60

Looking for Babylonian volume meassurement with Abstract = 3:33:20:0:44:20
Base reference unit: gin
---------------------------------------------------------------------------
(1536001 sargal 2 saru 8 sar 4 buru) gan                     <- 3:33:20:0:44:20
(25600 sargal 1 sar 2 buru 8 bur 2 ese) gan                  <- 3:33:20:0:44:20
(426 sargal 4 saru 1 bur 1 ese 2 iku) gan (3 bur 1 ese) sar  <- 3:33:20:0:44:20
(7 sargal 6 sar 4 buru) gan (4 u 4 dis) sar (2 u) gin        <- 3:33:20:0:44:20
(7 sar 6 bur 2 ese) gan (4 u 4 dis) gin (3 bur 1 ese) se     <- 3:33:20:0:44:20
(7 bur 2 iku) gan (7 bur 1 ese 1 iku) se                     <- 3:33:20:0:44:20
(2 iku) gan (1 u 3 dis) sar (2 u) gin (2 dis) se             <- 3:33:20:0:40
(3 dis) sar (3 u 3 dis) gin (3 bur 1 ese) se                 <- 3:33:20

```


### Fractions

Use the `-F0` option to have the output use the fractions `1/3, 1/2, 2/3, 5/6'`, `-F1` to also include the fraction `1/6`:

```bash
$ mtlookup -t V '128 gan 133 se' -pF0
(7 bur 2 iku) gan 2/3 gin (1 u 3 dis) se  ->  3:33:20:0:44:20
```

```bash
$ mtlookup -t L 1.30 -r -F0

Looking for Babylonian length meassurement with Abstract = 1:30
Base reference unit: ninda
----------------------------------------------------------------
10800 danna          <- 1:30
180 danna            <- 1:30
3 danna              <- 1:30
1 1/2 us             <- 1:30
1 1/2 ninda          <- 1:30
9 susi               <- 1:30
```


You may combine it with `-p` (pedantic mode):

```bash
$ mtlookup -t L 1.30 -r -pF1

Looking for Babylonian length meassurement with Abstract = 1:30
Base reference unit: ninda
----------------------------------------------------------------
(3 sar) danna        <- 1:30
(3 ges) danna        <- 1:30
(3 dis) danna        <- 1:30
(1 dis) 1/2 us       <- 1:30
(1 dis) 1/2 ninda    <- 1:30
1/6 kus (4 dis) susi <- 1:30
```

### Academic unit names

You can combine the `-F --fractions` options with `-a --academic` to obtain listings using the academic names of the units:

```bash
$ mtlookup -t L '1 us 30 ninda' -aF1
1 1/2 UŠ  ->  1:30
```

```bash
$ mtlookup -t L 1.30 -r -pF1 -aw 25

Looking for Babylonian length meassurement with Abstract = 1:30
Base reference unit: ninda
----------------------------------------------------------------
(3 sar) danna             <- 1:30
(3 ges) danna             <- 1:30
(3 dis) danna             <- 1:30
(1 dis) 1/2 UŠ            <- 1:30
(1 dis) 1/2 ninda         <- 1:30
1/6 kuš3 (4 dis) šu-si    <- 1:30
```
