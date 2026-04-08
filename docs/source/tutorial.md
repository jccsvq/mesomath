![mesomath](_static/mesomath.png)


# `babcalc` {{ release }}: The Scribe's Manual

> 𒎀 **Display Note**: Throughout this manual, you will see examples of cuneiform writing. If empty rectangles (▯) appear on your screen, consult the [Cuneiform Support](#cuneiform-support) section to install the necessary fonts.

## **I. Foundations: The Sexagesimal Engine**

(babcalc-intro)=

### 1\. **Introduction & Quickstart**

`babcalc` is the heart of the **MesoMath** ecosystem. It is a specialized [REPL (Read–Eval–Print Loop)](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) environment built upon Python 3, specifically architected to function as a seamless interactive calculator for Assyriological and mathematical research.

The `babcalc` interface serves two primary purposes:

  * **Interactive Computation**: It provides a pre-configured shell where all metrological and sexagesimal classes are pre-loaded and aliased for high-speed calculation.
  * **Workflow Automation**: It streamlines the execution of [scripts](https://www.google.com/search?q=%23scripting) by automatically resolving environment dependencies and paths, ensuring a consistent execution context regardless of your local [installation](#installation) method (e.g., `pipx` or virtual environments).

#### **Core Concepts: Classes and Objects**

For users less familiar with Object-Oriented Programming (OOP), it is helpful to understand that **Classes** act as blueprints. They define specific types of **Objects** (such as a weight or a length), their **Properties** (their value in different systems), and the **Methods** (operations like addition, reciprocal calculation, or transliteration) that can be performed upon them.

MesoMath organizes the metrology of the Old Babylonian Period (OBP) into the following optimized classes:

| Class | Domain | Shortcut |
| :--- | :--- | :--- |
| `BabN` | Sexagesimal Place Value Numbers | `bn` |
| `Blen` | Length (Linear measures) | `bl` |
| `Bsur` | Surface (Area) | `bs` |
| `Bvol` | Volume (Solid/Earth/Bricks) | `bv` |
| `Bcap` | Capacity (Liquid/Grain) | `bc` |
| `Bwei` | Weight (Mass) | `bw` |
| `Bbri` | Brick Metrology (Counts) | `bb` |
| `BsyG` | Enumeration (System **G**) | `bG` |
| `BsyS` | Enumeration (System **S**) | `bS` |
| `BsyC` | Enumeration (System **C**) | `bC` |
| `BsyK` | Enumeration (System **K**) | `bK` |

-----

**Invoking the Calculator**

If you have [installed](https://www.google.com/search?q=installation) MesoMath via `pip`, `pipx`, or `hatch`, the `babcalc` command is automatically added to your system's PATH. Simply execute it to initialize the environment:

```bash
$ babcalc
```

The terminal will display the initialization banner, confirming that the historical metrological models are ready for use:

```text
Welcome to Babylonian Calculator 2.0.0
    ...the calculator every scribe should have!

Use: bn(number) for sexagesimal calculations
Metrological classes: bl, bs, bv, bc, bw, bG, bS, bC, bK and bb loaded.
Use exit() or Ctrl-D to exit

--> 
```

> **Note**: The `-->` symbol represents the primary MesoMath prompt, indicating the system is ready for sexagesimal or metrological input.

#### **Manual Execution**

In the event that the command-line shortcut is not directly accessible, you may invoke the module via the Python interpreter:

```bash
$ python3 -m mesomath.babcalc
```

#### **Cloud Integration**

For a zero-install experience, a [Jupyter Notebook](https://jupyter.org/) version of this manual is available. You can launch a live, interactive instance of `babcalc` in the cloud by clicking the Binder badge below. (The notebooks may be outdated for a while)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2Findex.ipynb)



### 2. **The `BabN` Class: Creating Babylonian Numbers**

In MesoMath, a **Babylonian Number** is defined as a non-negative integer represented through **sexagesimal place-value notation**. The `BabN` class (aliased as `bn` in `babcalc`) is the fundamental engine for these numerical entities.

#### **Core Properties and Exploration**
Let us initialize a Babylonian number and examine its internal structure:

```pycon
--> a = bn(405)
```

By querying the object's attributes, we can observe how MesoMath maintains the duality between decimal and sexagesimal systems:

* `a.dec`: The decimal integer value (405).
* `a.list`: The sexagesimal digits represented as a Python list: `[6, 45]` ($6 \times 60 + 45$).
* `a.factors`: A tuple representing the prime factorization in the form $(2^i, 3^j, 5^k, l)$. For 405, this is `(0, 4, 1, 1)`, meaning $2^0 \cdot 3^4 \cdot 5^1 \cdot 1$.
* `a.isreg`: A Boolean indicating if the number is **regular**. A number is regular if its prime factors are limited to 2, 3, and 5, meaning it possesses a finite sexagesimal reciprocal.
* `print(a)`: Returns the standard string representation: `6:45`.
* `a.rec()` : Returns the reciprocal of regular numbers.

```pycon
--> a = bn(405)
--> a.dec
405
--> a.list
[6, 45]
--> a.factors
(0, 4, 1, 1)
--> a.isreg
True
--> print(a)
6:45
--> a
6:45
--> a.rec()
8:53:20
--> bn(7).rec()
Not regular, (igi nu)!
```

#### **The `.explain()` Method**
For a comprehensive analysis, the `.explain()` method provides a detailed breakdown of the number's mathematical properties:

```pycon
--> a.explain()
|  Sexagesimal number: [6, 45] is the decimal number: 405.
|    It may be written as (2^0 * 3^4 * 5^1 * 1),
|    so, it is a regular number with reciprocal: 8:53:20
```

If the number is **irregular** (contains prime factors other than 2, 3, or 5), the method provides useful heuristics:

```pycon
--> b = bn(7)
--> b.explain()
|  Sexagesimal number: [7] is the decimal number:   7.
|    It may be written as (2^0 * 3^0 * 5^0 * 7),
|    so, it is NOT a regular number and has NO reciprocal.
|    but an approximate inverse is: 8:34:17:9
|    and a close regular is: 6:59:54:14:24
|    whose reciprocal is: 8:34:24:11:51:6:40
```



---

#### **Input Flexibility**
MesoMath supports four distinct methods for instantiating Babylonian numbers, allowing you to work with decimal data, digit lists, literal strings, or prime factors:

1.  **Decimal**: `bn(405)`
2.  **Digit List**: `bn([6, 45])`
3.  **Literal String**: `bn('6:45')` or `bn("6.45")`
4.  **Factors (Tuple)**: `bn((0, 4, 1, 1))`

All these methods yield identical objects:
```pycon
--> bn(405) == bn([6, 45]) == bn('6:45') == bn((0, 4, 1, 1))
True
```

> **Implementation Note**: The `BabN` class handles **non-negative integers** only. If a negative value is passed (e.g., `bn(-405)`), the class will automatically use the absolute value.

---

#### **Formatting and Separators**
By default, MesoMath uses the colon (`:`) as the digit separator. However, this is globally configurable via the `bn.sep` attribute to match different publication styles:

```pycon
--> n1 = bn(314159265)
--> n1
24:14:26:27:45
--> bn.sep = '.'
--> n1
24.14.26.27.45
```

When parsing strings, the `bn` constructor is highly resilient and can interpret multiple separators (`:`,  `;`, `.`, `,`,`-`) and blank space (` `) simultaneously:
```pycon
--> bn('1:2;3,4.5 6-7')
1:2:3:4:5:6:7
```

#### **Digit Count**
To determine the precision or "length" of a number (the number of sexagesimal places it occupies), you can use either the class method `.len()` or the standard Python `len()` function:

```pycon
--> m = bn('3:14:16')
--> len(m)
3
```


### 3. **The Arithmetic of Clay**: Operations, Roots, Reciprocals and logic.


MesoMath assumes a foundational understanding of Mesopotamian mathematics, particularly the distinction between **absolute** and **floating** sexagesimal notation, as well as the properties of **regular** and **reciprocal** numbers.

#### **3.1 Basic Arithmetic**

##### **Addition and Subtraction**
In MesoMath, addition and subtraction are **absolute** operations. Unlike modern algebra, Mesopotamian mathematics did not utilize negative numbers. To prevent errors and align with historical logic, subtraction in `BabN` returns the absolute difference. Consequently, **subtraction is commutative** by design:

```pycon
--> bn(45689) - bn(325874)
1:17:49:45
--> bn(325874) - bn(45689)
1:17:49:45
```

Addition supports multiple addends and direct interaction with standard Python integers:

```pycon
--> a = bn('16:24:35')
--> a + 34 + bn('1:33:54:22')
1:50:19:31
```

If a **floating** result is required (normalizing the number by removing trailing zeros), use the `.float()` method or its shortcut `.f()`:

```pycon
--> c = bn('40:16:37:0:0')
--> c.f()
40:16:37
```

##### **Multiplication and Powers**
Multiplication is absolute by default, but its behavior can be globally toggled via the `bn.floatmult` attribute. Powers are handled via the standard `**` operator:

```pycon
--> bn(3)*bn(140)
7:0
--> bn.floatmult = True
--> bn(3)*bn(140)
7
--> bn.floatmult = False
--> bn(3)*bn(140)
7:0
--> a = bn('34:59:31:12')
--> a**2
20:24:26:24:13:49:26:24
--> a**3
11:54:5:36:24:11:24:33:52:7:40:48
```

##### **Division: Modern vs. Babylonian**
MesoMath distinguishes between two conceptual approaches to division:

1.  **Modern Division (`a / b`)**: An approximate floating-point division. It converts sexagesimal values to a decimal-like quotient for the convenience of the modern researcher. The precision is controlled by `bn.rdigits`.

```pycon
--> bn(34)/7
4:51:25:42:51:25:43
--> bn(34)/bn(7)
4:51:25:42:51:25:43
--> 34/bn(7)
4:51:25:42:51:25:43
```

2.  **Babylonian Division (`a // b`)**: Historically accurate division via the **product of the reciprocal**. This operation requires the divisor `b` to be a **regular number**.

```pycon
--> a = bn('14:15:16')
--> b = bn(405) # Regular: 6:45
--> a // b
2:6:42:22:13:20
--> a//bn(7)
Divisor is not a regular number (igi nu)!
```

---

#### **3.2 Root Extraction**

MesoMath provides methods for calculating floating-point square (`.sqrt()`) and cube (`.cbrt()`) roots. These tools are essential for verifying tablet calculations, such as the famous diagonal of the square in **YBC 7289**.

```pycon
--> bn(2).sqrt()
1:24:51:10:7:46
```

By multiplying this result by 30 (the side of the square), we can replicate the exact value inscribed by the apprentice scribe over 3,700 years ago:

```pycon
--> (30 * bn(2).sqrt()).f()
42:25:35
```

The class attribute `rdigitis` controls the number of digits in some results. For example,

```pycon
--> bn(2).sqrt()
1:24:51:10:7:46
--> bn.rdigits = 10
--> bn(2).sqrt()
1:24:51:10:7:46:6:4:44:52
```


---

#### **3.3 Logical Operations and Complex Expressions**

Because MesoMath is built upon Python, `BabN` objects integrate seamlessly with standard logic and data structures (lists, comprehensions, etc.).

**Filtering for Regularity:**
A common research task is identifying regular numbers within a range. This can be achieved with a single line of Python code:

```pycon
--> [bn(i) for i in range(400, 410) if bn(i).isreg]
[6:40, 6:45]
```

**Logical Comparisons:**
```pycon
--> a = bn('16:22')
--> b = bn('44:16')
--> a < b and a.isreg
True
```

---

#### **3.4 Formatting: The `bn.fill` Attribute**

For researchers generating tables or requiring consistent digit widths, the `bn.fill` attribute toggles zero-padding for single-digit sexagesimal values (0-9).

```pycon
--> z = bn('1:2:0:14:5')
--> bn.fill = True
--> z
01:02:00:14:05
```

This global setting ensures that printed outputs align perfectly in columns, facilitating the creation of professional-grade metrological or mathematical lists.



### **4. Precision and Heuristic Tools**

The `BabN` class includes a suite of methods designed to handle approximations, reciprocals, and digit manipulation—essential for replicating the iterative processes of ancient calculators.

#### **4.1 Reciprocals and Inverses**

In the Babylonian system, division is conceptualized as multiplication by a reciprocal. MesoMath provides two ways to handle this:

* **`.rec()` (Reciprocal)**: Returns the exact reciprocal of a **regular** number. If the number is irregular (possessing prime factors other than 2, 3, or 5), it returns `None`.
* **`.inv(n)` (Inverse)**: A heuristic method for **irregular** numbers. Since irregular numbers have infinite sexagesimal expansions, `.inv(n)` calculates the first `n` digits of the approximation.

```pycon
--> a = bn(400) # 6:40
--> a.rec()
9
--> b = bn(406) # 6:46 (Irregular)
--> b.rec()
Not regular, (igi nu)!
--> b.inv(4)
08:52:01:11
```

#### **4.2 Digit Slicing and Rounding**

When working with long floating-point strings, researchers often need to truncate or round results to match the precision found on specific tablets.

* **`.round(n)`**: Returns the first `n` digits with standard rounding. This can also be invoked via the standard Python `round(obj, n)` function.
* **`.head(n)`**: Truncates the number, returning the first `n` digits without rounding.
* **`.tail(n)`**: Returns the final `n` digits, useful for analyzing remainders or lower-order values.

```pycon
--> c = bn('8:52:1:10:56:9:27')
--> c.round(4)
8:52:1:11
--> c.head(3)
8:52:1
--> c.tail(2)
9:27
```

#### **4.3 The Heuristic Search: `.searchreg()`**

A sophisticated feature of MesoMath is the ability to find the "closest regular" number to an irregular target. This mirrors the technique used by ancient scribes who substituted irregular values with nearby regular approximations to facilitate further calculations.

The `.searchreg(minn, maxn, limdigits=6, prt=False)` method queries an internal database to find the best candidate within a specified range:

```pycon
--> bn(7).searchreg('06:40', '07:40', 4, prt=True)
        72000 06:40
        54000 06:45
        37440 06:49:36
        35775 06:50:03:45
        19008 06:54:43:12
        12000 06:56:40
         6750 07:01:52:30
        24000 07:06:40
        43200 07:12
        50500 07:14:01:40
        60864 07:16:54:24
        62640 07:17:24
        82323 07:22:52:03
        88000 07:24:26:40
       108000 07:30
       126400 07:35:06:40
       128250 07:35:37:30
Minimal distance: 6750, closest regular is: 07:01:52:30
07:01:52:30
```

> **Note on Distance**: MesoMath uses a specialized "floating distance" (`.dist()`). Unlike decimal distance, this metric prioritizes the similarity of the **most significant digits** (the "head" of the number), correctly identifying that `7` is closer to `6:59:54:14:24` than to `7:10`.

---

#### **4.4 Accessing Documentation: `help()`**

MesoMath is fully documented internally. If you are unsure about the parameters of a method or its default values, you can use the built-in Python `help()` system directly from the `babcalc` prompt:

```pycon
--> help(bn.searchreg)
```
This will display the docstring for the method, including parameter types and return values. (Press `q` to return to the prompt).



### **5. Cuneiform Representation**

The `BabN` class can transform any sexagesimal number into its equivalent Unicode cuneiform signs. This is not a static mapping but a dynamic rendering that supports different scribal styles.

Using the `.cuneiform()` method, you can visualize the number directly:

```pycon
--> a = bn('1:12:0:52:37')
--> print(a.cuneiform())
  𒐕 𒌋𒐖  𒐐𒐖 𒌍𒑂  
```

MesoMath allows for nuanced control over the paleography through parameters:

  * **`alter=True`**: Uses alternative sign forms for certain values (e.g., variant forms of 40 or 50).
  * **`stroke=True`**: Adds structural or separation strokes where historically applicable to improve readability.



```pycon
--> # Using alternative signs and strokes for a more distinct rendering
--> print(a.cuneiform(alter=1, stroke=1))
 𒐕 𒌋𒐖 𒃵 𒑪𒐖 𒌍𒑂  
```

> **Tip:** Use `help(bn.cuneiform)` to see all available styles and stroke options. Note that the output relies on having a **Cuneiform Unicode font** installed on your system.

### **6. Multiplication Tables**

In the Babylonian *Edubba* (tablet house), learning the multiplication tables of "principal" numbers was a foundational requirement for any scribe. MesoMath replicates this experience through the `.multable()` method, allowing you to generate these tables instantly for any sexagesimal value.

#### **5.1 The Internal Method: `.multable()`**

Unlike standard calculators, MesoMath allows a `BabN` object to "reveal" its own multiplication table. By default, it follows the ancient scribal tradition of displaying products for the multipliers: **1–20, 30, 40, and 50**.

```pycon
--> n = bn(9)
--> n.multable()

|  i  | i * 9|
|-----|------|
|  1  |    9 |
|  2  |   18 |
|  3  |   27 |
|  4  |   36 |
|  5  |   45 |
|  6  |   54 |
|  7  |  1:3 |
|  8  | 1:12 |
|  9  | 1:21 |
| 10  | 1:30 |
| 11  | 1:39 |
| 12  | 1:48 |
| 13  | 1:57 |
| 14  |  2:6 |
| 15  | 2:15 |
| 16  | 2:24 |
| 17  | 2:33 |
| 18  | 2:42 |
| 19  | 2:51 |
| 20  |  3:0 |
| 30  | 4:30 |
| 40  |  6:0 |
| 50  | 7:30 |
```

#### **5.2 Advanced Options**

The `.multable()` method is highly customizable to suit different research needs:

* **Full Tables (`pral=False`)**: Generates a continuous table from 1 to 59.
* **Floating Point (`floating=True`)**: Displays results in sexagesimal floating-point notation (useful for complex reciprocal calculations).
* **Cuneiform Output (`cuneiform=True`)**: Renders the entire table in original characters, including the multiplication operator label.



#### **5.3 Cuneiform Tables**

When using the `cuneiform=True` flag, MesoMath uses the `TIMES_LABEL` glyph and properly aligns the columns to provide a high-fidelity digital reconstruction of a clay tablet.

```pycon
--> n = bn(25)
--> n.multable(cuneiform=True, stroke=True)

|   𒎙𒐙  𒀀 𒁺  𒐕  |    𒎙𒐙 |
|---------------|-------|
|       𒀀 𒁺   𒐖 |    𒑪  |
|       𒀀 𒁺   𒐗 |  𒐕 𒌋𒐙 |
|       𒀀 𒁺   𒐘 |  𒐕 𒑩  |
|       𒀀 𒁺   𒐙 |  𒐖  𒐙 |
|       𒀀 𒁺   𒐚 |  𒐖 𒌍  |
|       𒀀 𒁺   𒑂 |  𒐖 𒑪𒐙 |
|       𒀀 𒁺   𒑄 |  𒐗 𒎙  |
|       𒀀 𒁺   𒑆 |  𒐗 𒑩𒐙 |
|       𒀀 𒁺  𒌋  |  𒐘 𒌋  |
|       𒀀 𒁺  𒌋𒐕 |  𒐘 𒌍𒐙 |
|       𒀀 𒁺  𒌋𒐖 |   𒐙 𒃵 |
|       𒀀 𒁺  𒌋𒐗 |  𒐙 𒎙𒐙 |
|       𒀀 𒁺  𒌋𒐘 |  𒐙 𒑪  |
|       𒀀 𒁺  𒌋𒐙 |  𒐚 𒌋𒐙 |
|       𒀀 𒁺  𒌋𒐚 |  𒐚 𒑩  |
|       𒀀 𒁺  𒌋𒑂 |  𒑂  𒐙 |
|       𒀀 𒁺  𒌋𒑄 |  𒑂 𒌍  |
|       𒀀 𒁺  𒌋𒑆 |  𒑂 𒑪𒐙 |
|       𒀀 𒁺  𒎙  |  𒑄 𒎙  |
|       𒀀 𒁺  𒌍  | 𒌋𒐖 𒌍  |
|       𒀀 𒁺  𒑩  | 𒌋𒐚 𒑩  |
|       𒀀 𒁺  𒑪  | 𒎙  𒑪  |
```

The previous cuneiform output should appear correctly aligned on almost any modern terminal; but, due to the variable width of the cuneiform glyphs, it is next to impossible to get it to appear aligned in an HTML document like this using a monospaced font, so henceforth the outputs will be presented in table format.


|   𒎙𒐙  𒀀 𒁺  𒐕  |    𒎙𒐙 |
|---------------|-------|
|       𒀀 𒁺   𒐖 |    𒑪  |
|       𒀀 𒁺   𒐗 |  𒐕 𒌋𒐙 |
|       𒀀 𒁺   𒐘 |  𒐕 𒑩  |
|       𒀀 𒁺   𒐙 |  𒐖  𒐙 |
|       𒀀 𒁺   𒐚 |  𒐖 𒌍  |
|       𒀀 𒁺   𒑂 |  𒐖 𒑪𒐙 |
|       𒀀 𒁺   𒑄 |  𒐗 𒎙  |
|       𒀀 𒁺   𒑆 |  𒐗 𒑩𒐙 |
|       𒀀 𒁺  𒌋  |  𒐘 𒌋  |
|       𒀀 𒁺  𒌋𒐕 |  𒐘 𒌍𒐙 |
|       𒀀 𒁺  𒌋𒐖 |   𒐙 𒃵 |
|       𒀀 𒁺  𒌋𒐗 |  𒐙 𒎙𒐙 |
|       𒀀 𒁺  𒌋𒐘 |  𒐙 𒑪  |
|       𒀀 𒁺  𒌋𒐙 |  𒐚 𒌋𒐙 |
|       𒀀 𒁺  𒌋𒐚 |  𒐚 𒑩  |
|       𒀀 𒁺  𒌋𒑂 |  𒑂  𒐙 |
|       𒀀 𒁺  𒌋𒑄 |  𒑂 𒌍  |
|       𒀀 𒁺  𒌋𒑆 |  𒑂 𒑪𒐙 |
|       𒀀 𒁺  𒎙  |  𒑄 𒎙  |
|       𒀀 𒁺  𒌍  | 𒌋𒐖 𒌍  |
|       𒀀 𒁺  𒑩  | 𒌋𒐚 𒑩  |
|       𒀀 𒁺  𒑪  | 𒎙  𒑪  |

>**Note**: As you can see, the previous output is in **Markdown table format**, so if you use Markdown for your documents, you're in luck, you just have to copy and paste the result from the terminal into your document and that's it. But you can also paste it into an intermediate `.csv` file that can be read by any spreadsheet (indicating the pipe `|` character as the column separator) and from there you can copy and paste it into your word processor or presentations.

<div class="tablet mini" style="text-align: right;">


|   𒎙𒐙  𒀀 𒁺  𒐕  |    𒎙𒐙 |
|---------------|------:|
|       𒀀 𒁺   𒐖 |    𒑪  |
|       𒀀 𒁺   𒐗 |  𒐕 𒌋𒐙 |
|       𒀀 𒁺   𒐘 |  𒐕 𒑩  |
|       𒀀 𒁺   𒐙 |  𒐖  𒐙 |
|       𒀀 𒁺   𒐚 |  𒐖 𒌍  |
|       𒀀 𒁺   𒑂 |  𒐖 𒑪𒐙 |
|       𒀀 𒁺   𒑄 |  𒐗 𒎙  |
|       𒀀 𒁺   𒑆 |  𒐗 𒑩𒐙 |
|       𒀀 𒁺  𒌋  |  𒐘 𒌋  |
|       𒀀 𒁺  𒌋𒐕 |  𒐘 𒌍𒐙 |
|       𒀀 𒁺  𒌋𒐖 |   𒐙 𒃵 |
|       𒀀 𒁺  𒌋𒐗 |  𒐙 𒎙𒐙 |
|       𒀀 𒁺  𒌋𒐘 |  𒐙 𒑪  |
|       𒀀 𒁺  𒌋𒐙 |  𒐚 𒌋𒐙 |
|       𒀀 𒁺  𒌋𒐚 |  𒐚 𒑩  |
|       𒀀 𒁺  𒌋𒑂 |  𒑂  𒐙 |
|       𒀀 𒁺  𒌋𒑄 |  𒑂 𒌍  |
|       𒀀 𒁺  𒌋𒑆 |  𒑂 𒑪𒐙 |
|       𒀀 𒁺  𒎙  |  𒑄 𒎙  |
|       𒀀 𒁺  𒌍  | 𒌋𒐖 𒌍  |
|       𒀀 𒁺  𒑩  | 𒌋𒐚 𒑩  |
|       𒀀 𒁺  𒑪  | 𒎙  𒑪  |

</div>


> **Warning**: If you are using the legacy `bmultable.py` script, we strongly recommend migrating your workflow to the `.multable()` method. The standalone script is considered **obsolete** and will be removed in the final stable 2.0.0 release.

---

#### **Summary of Parameters**

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `pral` | `bool` | `True` | If `True`, only prints the traditional "principal" multipliers. |
| `cuneiform`| `bool` | `False` | Switches output to Unicode Cuneiform characters. |
| `floating` | `bool` | `False` | Displays results as sexagesimal floating point numbers. |
| `sep` | `str` | `":"` | Custom separator for sexagesimal digits in ASCII mode. |
| `stroke` | `bool` | `False` | In cuneiform mode, uses a specific stroke for empty positional values (zeroes). |


---

## **II. Metrology: The Weight of Tradition**

The metrological engine of MesoMath is designed to handle the complex, non-linear systems of the Old Babylonian Period (OBP). Unlike the metric system, where conversion is a simple shift of the decimal point, Babylonian metrology relies on specific coefficients and discrete systems for different domains.

### 1\. **The Four Pillars and the Specificity of Classes**

MesoMath defines several specialized classes to represent different physical domains. While a modern mathematician might treat surfaces, volumes, and brick counts as "just numbers," the Babylonian scribe—and consequently this library—treats them as distinct ontological categories because **they support different mathematical operations and socio-economic rules.**

| Class | Domain | Base Unit |
| :--- | :--- | :--- |
| `Blen` | **Length** | `ninda` (approx. 6m) |
| `Bsur` | **Surface** | `sar` (approx. 36m²) |
| `Bvol` | **Volume** | `sar` (standard thickness of 1 `kuš3`) |
| `Bcap` | **Capacity** | `gur` (approx. 300 litres) |
| `Bwei` | **Weight** | `gu2` (talent, approx. 30kg) |
| `Bbri` | **Bricks** | `sar` (standardized brick volumes) |

#### **The Volume-Surface Equivalence (The 1-cubit Rule)**

In Babylonian mathematics, **Volumes** (`Bvol`) and **Brick counts** (`Bbri`) are expressed using the same units as **Surfaces** (`Bsur`). This is not a coincidence:

  * A volume is conceptually a "surface with a standardized thickness" of **1 `kuš3`** (cubit).
  * Therefore, a volume of `1 sar` represents a block with a base of `1 sar` (1x1 `ninda`) and a height of `1 kuš3`.

#### **Why separate classes?**

Although they share units (like the `sar`), MesoMath uses separate classes because:

1.  **Validation**: It prevents the accidental addition of a weight (`Bwei`) to a capacity (`Bcap`).
2.  **Specialized Methods**: `Bbri` (Bricks) includes methods for counting physical units that `Bsur` does not need.
3.  **Epigraphy**: Transliteration rules can vary slightly depending on whether you are describing a field or a pile of grain.

-----

### 2\. **The "Vertical Problem": Defining Height**

A common question for new users is: **"Where is the class for vertical lengths (height/depth)?"**

In the OBP system, vertical measures (heights of walls, depths of canals) are technically lengths. However, while horizontal lengths are measured in `ninda`, vertical measures are almost exclusively recorded in **`kuš3`**.

MesoMath does **not** include a separate `Bheight` class by default because:

  * Mathematically, it is redundant; any vertical measure is a `Blen` object.
  * The system is designed to favor the `ninda` as the primary sexagesimal unit for `Blen`, which is the standard for mathematical tablets.

> **User Extension**: If your specific research involves heavy interaction between vertical and horizontal measures and you prefer the semantic clarity of a dedicated class, you can easily [extend the metrology](#vertical-problem) to create one. However, for 99% of applications, using `Blen` with the appropriate unit (e.g., `bl('2 kuš3')`) is the historically accurate and functionally sufficient approach.

-----


### **3. Basics of Metrological Classes**

MesoMath handles historical metrology through specialized classes. While these classes are pre-imported in `babcalc` (as `bl`, `bc`, `bw`, etc.), their full academic names and internal structures are essential for advanced scripting and research.

#### **3.1 The Metrological Systems (OBP)**
Each class represents a specific physical domain with its own hierarchy of units and conversion factors:

**Measurements**

* **`bl` (Length)**: `danna` <-30- `UŠ` <-60- `ninda` <-12- `kuš3` <-30- `šu-si`
* **`bs`/`bv`/`bb` (Surface/Volume/Bricks)**: `GAN2` <-100- `sar` <-60- `gin2` <-180- `še`
* **`bc` (Capacity)**: `gur` <-5- `bariga` <-6- `ban2` <-10- `sila3` <-60- `gin2` <-180- `še`
* **`bw` (Weight)**: `gu2` <-60- `ma-na` <-60- `gin2` <-180- `še`

**Sexagesimal NPVS; Specialized counting systems**

* **`bG`**: `šar2-gal` <-6- `šar'u` <-10- `šar2` <-6- `bur'u` <-10- `bur3` <-3- `eše3` <-6- `iku`
* **`bS`**: `šar2-gal` <-6- `šar'u` <-10- `šar2` <-6- `geš'u` <-10- `geš` <-6- `u` <-10- `aš`
* **`bK`**: `šar2-gal` <-6- `šar'u` <-10- `šar2` <-6- `geš'u` <-10- `geš` <-6- `u` <-10- `diš`


#### **3.2 Unit Names and Schemas**
For ease of use in the REPL, unit names have been simplified (e.g., `susi` for *šu-si*, `kus` for *kuš3*). You can query any class to see its internal schema and academic nomenclature:

```pycon
--> bc.uname   # Simplified names for input
['se', 'gin', 'sila', 'ban', 'bariga', 'gur']

--> bc.aname   # Academic names with diacritics
['še', 'gin2', 'sila3', 'ban2', 'bariga', 'gur']

--> bc.cname()
['𒊺', '𒂆', '𒋡', '𒑏', '𒉿', '𒄥']

--> print(*bc.scheme(bc, 0)) # Visual representation of the hierarchy
gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še

--> print(*bc.scheme(bc, 1)) # Cuneiform representation of the hierarchy
𒄥   ╼5╾  𒉿   ╼6╾  𒑏   ╼10╾  𒋡   ╼60╾  𒂆   ╼180╾  𒊺
```

---

#### **3.3 Defining Measurements**
You can instantiate metrological objects using two primary methods:
1.  **Smallest Unit (Integer)**: Passing a raw integer represents the total count of the smallest unit in that system.
2.  **String Literal**: A descriptive string using unit names.

```pycon
--> a = bl(11111)              # 11,111 susi
--> b = bl('5 ninda 25 susi')  # Textual definition
--> a
30 ninda 10 kus 11 susi
--> b
5 ninda 25 susi
--> a.dec
11111                          # total count of the smallest unit
--> b.dec
1825

```

#### **3.4 The `.sex()` and `.explain()` Methods**
To bridge the gap between concrete metrology and sexagesimal abstraction, the `.sex(unit_index)` method calculates the **sexagesimal floating value** relative to a specific unit in the hierarchy.

* `a.sex(2)`: Calculates the value relative to the 3rd unit (index 2), which for lengths is the `ninda`.

```pycon
--> bl.uname
['susi', 'kus', 'ninda', 'us', 'danna']
--> bl.uname[2]
'ninda'
```

This is the engine used to recreate historical **metrological lists**:

```pycon
--> bl('1 kus').sex(2)  # 1 kus as a fraction of a ninda (1/12)
5
--> bl('1 kus').sex(1)  # 1 kus as a fraction of a kus (1)
1
--> bl('1 kus').sex()  # 1 kus as a multiple of a susi (30) (Default = 0)
30
```

For a complete overview, including the approximate International System (SI) equivalent, use `.explain()`:

```pycon
--> bl('1 kus').explain()
This is a Babylonian length measurement: 1 kus
    Metrology:  danna <-30- us <-60- ninda <-12- kus <-30- susi
    Factor with unit 'susi':  1 30 360 21600 648000
Measurement in terms of the smallest unit: 30 (susi)
Sexagesimal floating value of the above: 30
Approximate SI value: 0.5 meters
```

---

### **4. Metrological Operations**

MesoMath objects are aware of their dimensional nature. They allow for both intra-class arithmetic and inter-class geometric operations.

#### **4.1 Intra-class Arithmetic**
Objects of the same class support addition, subtraction (absolute difference), and scaling by a number.

```pycon
--> a = bl('1 ninda')
--> b = bl('2 kus')
--> a + b
1 ninda 2 kus

--> a - b == b - a   # Subtraction is commutative (absolute difference)
True

--> a * 2.5          # Scaling by a factor
2 ninda 6 kus
--> c=bl(11111)
--> c
30 ninda 10 kus 11 susi
--> c*2
1 us 1 ninda 8 kus 22 susi
--> c/2
15 ninda 5 kus 6 susi  # Rounding!!
--> 2*(c/2)
30 ninda 10 kus 12 susi
```


#### **4.2 Geometric Interaction (Dimensionality)**

MesoMath enforces logical geometric rules through **Dimensional Awareness**. You can multiply lengths to generate surfaces, and surfaces by lengths to generate volumes. Conversely, you can divide these higher-order magnitudes to find missing linear or planar dimensions. 

However, “illegal” operations (like multiplying two volumes or dividing a length by a surface) are prohibited to maintain historical and physical consistency.

##### **Building Up: Multiplication**
Assembling a 3D structure follows the logical progression from $L \to S \to V$.

```pycon
--> length = bl('10 ninda')
--> width  = bl('5 ninda')
--> height = bl('2 kus')

--> surface = length * width      # returns a Bsur object (50 sar)
--> volume  = surface * height    # returns a Bvol object (1 2/3 sar)
--> volume2 = length * width * height
--> volume == volume2
True
```

##### **Breaking Down: Division**
MesoMath overloads the division operator to perform **Dimensional Descent**. This allows you to solve for a missing side or height directly.

* **Surface / Length = Length** ($S / L \to L$)
* **Volume / Length = Surface** ($V / L \to S$)
* **Volume / Surface = Length** ($V / S \to L$)

```pycon
--> # Finding the missing side of a 1 sar rectangle
--> area = bs('1 sar')
--> side_a = bl('3 ninda')
--> side_b = area / side_a
--> side_b.prtf()
'1/3 ninda'

--> # Finding the height of a canal from its volume and base area
--> total_vol = bv('10 sar')
--> base_area = bs('20 sar')
--> canal_depth = total_vol / base_area
--> canal_depth.prtf()
'1/2 kus'

--> # Finding the surface area from volume and a known linear dimension
--> width = bl('1/2 ninda')
--> canal_surface = total_vol / width
--> canal_surface
2(u) gan2
```



##### **Scaling and Distribution**
You can also divide any magnitude by a scalar (integer or float) for equal distribution or scaling without changing the dimension of the object.

```pycon
--> # Dividing a field of 1 gan2 among 3 brothers
--> field = bs('1 gan2')
--> share = field / 3
--> share
33 1/3 sar
```

> **Engineering Note**: In these operations, MesoMath automatically handles the internal conversion factors (e.g., the implicit thickness of $1 \text{ kuš}_3$ in volumes) and rounds the result to the nearest integer of the system's smallest unit.




### **4.3 SI Conversion & Modern Interoperability**

MesoMath provides a robust bridge between ancient units and the International System of Units (SI). This allows researchers to translate archaeological field data directly into Babylonian metrological objects.

#### **From Ancient to Modern: `.si()` and `.SI()`**
To obtain the approximate modern equivalent of a Babylonian measure, use `.si()` for a raw float or `.SI()` for a formatted string including the unit name.

```pycon
--> w = bw('1 mana 3 gin')
--> w.si()
0.525
--> w.SI()
'0.525 kilograms'
```

#### **From Modern to Ancient: `.from_si()`**
Reciprocally, the `@classmethod` `.from_si()` allows you to instantiate a metrological object starting from a modern value (meters, kilograms, square meters, cubic meters, or brick counts).

```pycon
--> # Converting 0.572 kg to Babylonian weight
--> a = bw.from_si(0.572)
--> a
1 mana 8 gin 115 se

--> # Checking the precision loss after conversion
--> a.SI()
'0.5719907407407407 kilograms'

--> # Converting a modern brick count to Babylonian Brick Metrology (Bbri)
--> bricks_total = bb.from_si(1700)
--> bricks_total
2 sar 21 gin 120 se
--> bricks_total.SI()
'1700.0 bricks'
```

> **Precision Note**: Since Babylonian metrology is based on discrete "units of account" (integers of the smallest unit), `.from_si()` uses a `round()` function. The small discrepancy seen in the example (`0.57199...` vs `0.572`) reflects the historical granularity of the system.


### **5. Advanced Metrological Input and Representation**

Mesopotamian scribes did not always record quantities as simple counts. Depending on the system (capacity, surface, etc.), they used specific sexagesimal notations known as **Systems S, G, C, and K**. MesoMath allows you to toggle between modern simplified output and these historical "sexagesimalized" representations.

#### **5.1 Historical Sexagesimal Modes (Systems C, S and G)**
By default, metrological objects display their values using simplified unit names and absolute decimal counts. However, you can switch to a mode that mimics the way measurements were actually inscribed on clay by grouping coefficients into higher-order sexagesimal signs (`bur3`, `iku`, `geš2`, etc.), see [Appendix A](#systems-SGC) for details on the use of systems C, S and G.

To activate this for a specific class (e.g., Volumes):
```pycon
--> bv.prtsex = True  # Enable historical sexagesimal grouping
--> a = bv('128 gan')
--> a
(7 bur 2 iku) gan
--> b=bw(11223344)
--> b
17 gu 19 mana 11 gin 164 se
--> bw.prtsex = True  # also: bw.prtsex = 1
--> b
(1 u 7 as) gu (1 u 9 dis) mana (1 u 1 dis) gin (2 ges 4 u 4 as) se
```

To apply this behavior globally to all metrological classes, use the master controller:
```python
from mesomath.npvs import MesoM
MesoM.prtsex = True
```

#### **5.2 The Third Input Method: Parenthetical Strings**
As a direct consequence of the historical mode, MesoMath supports a **third input method**. This method is highly resilient and allows you to copy-paste complex strings (even those with parentheses) directly into the constructor. For instance, continuing from above:

```pycon
--> c = bw('(1 u 7 as) gu (1 u 9 dis) mana (1 u 1 dis) gin (2 ges 4 u 4 as) se')
--> b == c
True
--> c.dec
11223344
```

The system can even interpret **sexagesimal coefficients** directly:
```pycon
--> d = bv('2:8:0:0 gan 44 sar 20 gin')
--> d
(7 sargal 6 sar 4 buru) gan (4 u 4 dis) sar (2 u) gin
```

---

#### **5.3 Fractional Support**
The Babylonian system relied heavily on a specific set of **principal fractions**: $1/6, 1/3, 1/2, 2/3,$ and $5/6$. MesoMath supports these fractions for both input and output.

**Inputting Fractions:**
Fractions can be entered using various natural syntaxes within the string literal:
```pycon
--> bl('1/3 ninda')        # Simple fraction
4 kus
--> bl('2 1/3 ninda')      # Integer + fraction
2 ninda 4 kus
--> bl('2 + 1/3 ninda')    # Explicit addition
2 ninda 4 kus
```

**Outputting Fractions (`.prtf()`):**
To generate a human-readable string that utilizes these fractions, use the `.prtf()` method.
* `prtf()`: Uses standard fractions ($1/3, 1/2, 2/3, 5/6$).
* `prtf(1)`: Includes the less frequent $1/6$ fraction.

```pycon
--> a = bl(11223344)
--> bl.prtsex = 0
--> a.prtf()
'17 danna 9 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
```

If `prtsex` is active, the fractions are seamlessly integrated into the historical notation:
```pycon
--> bl.prtsex = True
--> a.prtf()
'(1 u 7 dis) danna (9 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi'
```

and this result can also be used as input:

```pycon
--> b = bl('(1 u 7 dis) danna (9 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi')
--> a == b
True
```

---

#### **5.4 Academic Nomenclature**
For final publications or formal research notes, you may require the exact **academic names** of units (including diacritics and Sumerian/Akkadian terminology like `kuš3` or `šu-si`). 

The `.prtf()` method accepts a second parameter (`academic=True`) to toggle this nomenclature:

```pycon
--> a = bl(11223344)
--> # Using both fraction extension and academic names:
--> a.prtf(1, 1)  # bl.prtsex = True !!
'(1 u 7 diš) 1/6 danna (4 diš) 1/2 UŠ (5 diš) 5/6 ninda (1 diš) 1/3 kuš3 (4 diš) šu-si'
```

**Crucially**, MesoMath's parser is symmetrical: any string generated by `.prtf()`—including those with parentheses, fractions, and academic diacritics—is valid input for creating new objects.

```pycon
--> b = bl(a.prtf(1, 1))
--> b.dec
11223344
```

You can also use `.acad` to view academic names without fractions:

```pycon
--> b
(1 u 7 dis) danna (9 dis) us (3 u 5 dis) ninda (1 u 1 dis) kus (1 u 4 dis) susi
--> b.acad
'(1 u 7 diš) danna (9 diš) UŠ (3 u 5 diš) ninda (1 u 1 diš) kuš3 (1 u 4 diš) šu-si'
```

---


### **6. Volume, Capacity, and Brick Metrology**

In Mesopotamia, the concept of "volume" diverged based on the physical nature of the substance being measured. MesoMath respects this historical distinction through specialized classes that allow for fluid conversion between administrative domains.

#### **6.1 Volume vs. Capacity**
There were two distinct systems for measuring three-dimensional space:
* **Capacity (`Bcap` / `bc`)**: Used for "hollow" measures such as grain, beer, and other commodities. Its primary unit is the **`sila`** (approx. 1 liter).
* **Volume Proper (`Bvol` / `bv`)**: Used for "solid" measures such as earth, canals, and architectural structures. Its primary unit is the **`sar`** (approx. 18 m³).

Since both systems measure the same physical magnitude, MesoMath provides direct conversion methods: `.cap()` and `.vol()`.

```pycon
--> a = bv('1 gin')
--> b = a.cap()  # Convert volume to capacity
--> b
1 gur
--> b.vol()  # Convert back to volume
1 gin

```
* **Note**: In the Babylonian system, 1 `gin2` of volume is exactly equivalent to 1 `gur` of capacity.



---

#### **6.2 Brick Metrology (`Bbri`)**
The calculation of bricks is one of the most sophisticated applications of Babylonian mathematics. Rather than counting individual bricks, scribes used the **`sar-b`** (a unit representing a "stack" or volume of 720 bricks) and the concept of the **`Nalbanum`**.

> **The Nalbanum**: This is a conversion coefficient. While the physical volume of a wall remains constant, the number of bricks required depends on their specific dimensions. The *Nalbanum* acts as the multiplier to translate "theoretical volume" into an "actual brick count."

##### **Using the `.bricks()` Method**
By default, MesoMath assumes a *Nalbanum* of 1.0 (Standard Type-12 brick). For other historical types, pass the coefficient as an argument:

```pycon
--> wall_volume = bv('1 sar')
--> # Calculating for Type-2 bricks (Nalbanum 7.20)
--> brick_count = wall_volume.bricks(7.2)
--> brick_count.SI()
'5184.0 bricks'
```

##### **The Brick Unit: 15 `še`**
Internally, MesoMath defines a single standard brick as equivalent to **15 `še`**. This allows you to instantiate `Bbri` objects directly from a known count:

```pycon
--> # Creating an object for a shipment of 10,000 bricks
--> shipment = bb(15 * 10000)
--> shipment.SI()
'10000.0 bricks'
--> # Convert back to physical volume for a specific brick type
--> shipment.vol(7.2).SI()
'34.721666666666664 cube meters'
```

but you can also use the `.from_si()` method:

```pycon
--> shipment = bb.from_si(10000)
--> shipment.SI()
'10000.0 bricks'
--> shipment.vol(7.2).SI()
'34.721666666666664 cube meters'
```

---

#### **6.3 Reference: Nalbanum Table**
The following table details the coefficients for common brick types based on archaeological and mathematical evidence (notably the work of Robson and Maza):

| Brick Type | Nalbanum (Dec.) | Nalbanum (Sex.) | Description |
| :--- | :--- | :--- | :--- |
| **Type 1** | 9.00 | 9 | Standard square brick (*sig-al-ur-ra*) |
| **Type 1a** | 8.33 | 8:20 | Variant square form |
| **Type 2** | 7.20 | 7:12 | 2/3 `kuš3` brick |
| **Type 4** | 5.00 | 5 | Standard rectangular brick |
| **Type 12** | 1.00 | 1 | Unit reference for transport logistics |



---

### **⚠️ Crucial Metrological Note**
As established in the foundations of this manual, in Babylonian metrology, **Volumes and Bricks are treated identically to Surfaces**.

* Objects of class `Bvol` and `Bbri` utilize the same unit hierarchy as `Bsur` (`sar`, `gin2`, `še`).
* This reflects the ancient conception of volume as a **surface area with a default thickness of 1 `kuš3` (cubit)**.
* **Structural Integrity**: To maintain physical consistency, MesoMath allows multiplying `Surface * Length` to yield a `Volume`, but strictly prohibits multiplying `Volume * Length`. This prevents the inadvertent creation of four-dimensional "hyper-volumes," which remained outside the scope of scribal praxis.



---

### **What's Next?**
Now that we have covered the diverse metrological domains, we will explore the **`.metrolist()` method** in the next section. This tool allows the researcher to automatically generate reference tables and simulate the school-text lists used by ancient apprentices.



### **7. Generating Reference Tables: The `.metrolist()` Method**

MesoMath does not just calculate; it generates structured data. The `.metrolist()` family of methods allows you to create segments of metrological lists and tables in various formats, from simple terminal output to academic $\LaTeX$.

#### **7.1 Method Overview**
Depending on your final destination, MesoMath provides different "siblings" for the same generation engine:

| Format | Method | Best For |
| :--- | :--- | :--- |
| **Markdown / Terminal** | `.metrolist()` | Quick reference and documentation. |
| **HTML** | `.metrohtml()` | Web publishing and Sphinx documentation. |
| **Academic ($\LaTeX$)** | `.metrolatex()` | Direct inclusion in papers and books. |
| **Data Science (CSV)** | `.metrocsv()` | Analysis in spreadsheets or R/Pandas. |

>**Note**: Everything above depends internally on the `.metro_generator()` class method. Use, for example, `--> help(bl.metro_generator)` to see a complete list of options.

#### **7.2 Basic Usage**
The `.metrolist()` method requires three core parameters: **Initial Value**, **Final Value**, and **Increment**. These can be provided as unit strings or as raw integers (representing the smallest unit).

```pycon
--> # Creating a list of weights from 10 gin to 1 mana in 10-gin steps
--> bw.metrolist('10 gin', '1 mana', '10 gin')

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         |
|--------------------|
|10 gin              |
|20 gin              |
|30 gin              |
|40 gin              |
|50 gin              |
|1 mana              |
```

#### **7.3 Advanced Table Features**
By using **optional parameters**, you can transform a simple list into a complex comparative table:

* **`verbose=True`**: Adds columns for the **Sexagesimal value** and the **Reciprocal** (crucial for division problems).
* **`fractions=1` (or `2`)**: Automatically converts measurements to their fractional representations ($1/3$, $1/2$, $2/3$, $5/6$, and $1/6$).
* **`actual=True`**: Uses the academic unit names (e.g., `ma-na` instead of `mana`).
* **`echo=False`**: Instead of printing, it returns the table as a Python list of strings for script processing.

```pycon
--> # A comprehensive table with fractions and sexagesimal grouping enabled
--> bw.prtsex = True
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, fractions=1)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         | Sexag. (gin)    | Reciprocal  |
|--------------------|-----------------|-------------|
|(1 u) gin           | 10              | 6           |
|1/3 mana            | 20              | 3           |
|1/2 mana            | 30              | 2           |
|2/3 mana            | 40              | 1:30        |
|5/6 mana            | 50              | 1:12        |
|(1 dis) mana        | 1               | 1           |
```

---

#### **7.4 Segmented Lists (Historical Reconstruction)**
Historical tables often changed their increments as the values increased (e.g., counting by $1$ unit up to $10$, then by $10$ up to $60$). MesoMath replicates this by allowing **lists** for the `mmax` and `step` parameters.

```pycon
--> # Counting from 10 susi to 2 kus (step: 5 susi), then up to 12 kus (step: 1 kus)...
--> bl.metrolist("10 susi", ["2 kus", "12 kus"], ["5 susi", "1 kus"], verbose=True, fractions=1)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement         | Sexag. (ninda)  | Reciprocal  |
|--------------------|-----------------|-------------|
|1/3 kus             | 1:40            | 36          |
|1/2 kus             | 2:30            | 24          |
|2/3 kus             | 3:20            | 18          |
|5/6 kus             | 4:10            | 14:24       |
|1 kus               | 5               | 12          |
|1 kus 5 susi        | 5:50            | --igi nu--  |
|1 1/3 kus           | 6:40            | 9           |
|1 1/2 kus           | 7:30            | 8           |
|1 2/3 kus           | 8:20            | 7:12        |
|1 5/6 kus           | 9:10            | --igi nu--  |
|2 kus               | 10              | 6           |
|3 kus               | 15              | 4           |
|1/3 ninda           | 20              | 3           |
|1/3 ninda 1 kus     | 25              | 2:24        |
|1/2 ninda           | 30              | 2           |
|1/2 ninda 1 kus     | 35              | --igi nu--  |
|2/3 ninda           | 40              | 1:30        |
|2/3 ninda 1 kus     | 45              | 1:20        |
|5/6 ninda           | 50              | 1:12        |
|5/6 ninda 1 kus     | 55              | --igi nu--  |
|1 ninda             | 1               | 1           |
```

The table above is obviously a metrological table for horizontal lengths. If you wish to construct the same table for vertical lengths, use the parameter `ubase=1` (kus):

```pycon
--> bl.metrolist("10 susi", ["2 kus", "12 kus"], ["5 susi", "1 kus"], ubase=1,verbose=True, fractions=1)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement         | Sexag. (kus)    | Reciprocal  |
|--------------------|-----------------|-------------|
|1/3 kus             | 20              | 3           |
|1/2 kus             | 30              | 2           |
|2/3 kus             | 40              | 1:30        |
|5/6 kus             | 50              | 1:12        |
|1 kus               | 1               | 1           |
|1 kus 5 susi        | 1:10            | --igi nu--  |
|1 1/3 kus           | 1:20            | 45          |
|1 1/2 kus           | 1:30            | 40          |
|1 2/3 kus           | 1:40            | 36          |
|1 5/6 kus           | 1:50            | --igi nu--  |
|2 kus               | 2               | 30          |
|3 kus               | 3               | 20          |
|1/3 ninda           | 4               | 15          |
|1/3 ninda 1 kus     | 5               | 12          |
|1/2 ninda           | 6               | 10          |
|1/2 ninda 1 kus     | 7               | --igi nu--  |
|2/3 ninda           | 8               | 7:30        |
|2/3 ninda 1 kus     | 9               | 6:40        |
|5/6 ninda           | 10              | 6           |
|5/6 ninda 1 kus     | 11              | --igi nu--  |
|1 ninda             | 12              | 5           |
```

This is the most authentic way to recreate segments of the **Standard Metrological Tables** used in the Old Babylonian period.

---

#### **7.5 Exporting for Publication**
The siblings `.metrohtml()` and `.metrolatex()` generate files or raw code ready for use in external editors.

**Example: Generating an HTML table**
```pycon
--> bw.metrohtml('10 gin', '1 mana', '10 gin', verbose=True, file='weight_table')
--> Exported 6 rows to 'weight_table.html'
```

**Example: Generating a $\LaTeX$ table**
The $\LaTeX$ output uses the `booktabs` package style for a professional, academic look:

```latex
\begin{table}[h]
  \centering
  \begin{tabular}{lll}
    \toprule
    Measurement & Sexag. (gin) & Reciprocal \\
    \midrule
    (1 u) gin & 10 & 6 \\
    1/3 mana & 20 & 3 \\
    \bottomrule
  \end{tabular}
\end{table}
```

> **Note on Compatibility**: Some options are interdependent. For instance, `actual=True` (academic names) or `fractions` only trigger specific formatting when the system can resolve those units. Always use `help(bw.metro_generator)` to check the latest parameter overrides.


### **8. Historical Presets: The Proust Series**

Manually determining the start, end, and increment values to replicate an archaeological tablet can be tedious. To solve this, MesoMath includes `metrology_presets` based on the work of **Christine Proust** (e.g., *Tablettes mathématiques de Nippur*). 

These are pre-configured in `babcalc` under the following aliases:
* `clist`: Capacity Series (Proust 8.1)
* `wlist`: Weight Series (Proust 8.2)
* `slist`: Surface Series (Proust 8.3)
* `llist`: Length Series (Proust 8.4)

but for your scripts you need to import them:

```python
from mesomath.metrology_presets import CAPACITY_PROUST_81 as clist
from mesomath.metrology_presets import WEIGHT_PROUST_82 as wlist
from mesomath.metrology_presets import SURFACE_PROUST_83 as slist
from mesomath.metrology_presets import LENGTH_PROUST_84 as llist
```

#### **8.1 Exploring a Preset**
You can inspect the structure of a series by simply typing its name. This reveals the "curriculum steps" used in ancient scribal training:

```pycon
--> clist
MetrologySeries: Proust 8.1 Capacities (se)
-----------------------------------------------------------------
Step   | Start Value     | End Value       | Increment      
-----------------------------------------------------------------
0      | 1 gin           | 3 gin           | 30 se          
1      | 3 gin           | 20 gin          | 1 gin          
2      | 20 gin          | 2 sila          | 10 gin         
3      | 2 sila          | 2 ban           | 1 sila         
4      | 2 ban           | 1 bariga        | 5 sila         
5      | 1 bariga        | 1 gur           | 1 ban          
6      | 1 gur           | 2 gur           | 1 bariga       
7      | 2 gur           | 20 gur          | 1 gur          
8      | 20 gur          | 120 gur         | 10 gur         
9      | 120 gur         | 1200 gur        | 60 gur         
10     | 1200 gur        | 7200 gur        | 600 gur        
11     | 7200 gur        | 72000 gur       | 3600 gur       
12     | 72000 gur       | 216000 gur      | 36000 gur      
-----------------------------------------------------------------
--> clist.nframes 
13
```

#### **8.2 Using `.select()` to Generate Tables**
The real power of these presets lies in the `.select()` method. This allows you to pick specific ranges from the historical series and feed them directly into `.metrolist()` (or its siblings `.metrohtml()` / `.metrolatex()`).

If you want to reconstruct the segment of a capacity list from **Step 2 to Step 4** (covering measurements from `20 gin` up to `1 bariga` with their historically accurate shifting increments):

```pycon
--> # Extract start, end, and increment list for steps 2 through 4
--> a, b, c = clist.select(2, 4)
--> # Generate the segmented metrological list
--> bc.metrolist(a, b, c)

Babylonian capacity measurement
gur <-5- bariga <-6- ban <-10- sila <-60- gin <-180- se
|Measurement         |
|--------------------|
|20 gin              |
|30 gin              |
|40 gin              |
|50 gin              |
|1 sila              |
|1 sila 10 gin       |
|1 sila 20 gin       |
|1 sila 30 gin       |
|1 sila 40 gin       |
|1 sila 50 gin       |
|2 sila              |
|3 sila              |
|4 sila              |
|5 sila              |
|6 sila              |
|7 sila              |
|8 sila              |
|9 sila              |
|1 ban               |
|1 ban 1 sila        |
|1 ban 2 sila        |
|1 ban 3 sila        |
|1 ban 4 sila        |
|1 ban 5 sila        |
|1 ban 6 sila        |
|1 ban 7 sila        |
|1 ban 8 sila        |
|1 ban 9 sila        |
|2 ban               |
|2 ban 5 sila        |
|3 ban               |
|3 ban 5 sila        |
|4 ban               |
|4 ban 5 sila        |
|5 ban               |
|5 ban 5 sila        |
|1 bariga            |
```

#### **8.3 Why use Presets?**
1.  **Academic Accuracy**: You don't have to guess the increments used in ancient Nippur; they are already encoded.
2.  **Efficiency**: It allows for the rapid creation of comparative tables for papers or classroom presentations.
3.  **Cross-Validation**: Use these lists to verify if a broken fragment of a tablet follows the standard curriculum steps.

> **Pro Tip**: You can combine these presets with the advanced formatting seen earlier. For example, `bc.metrolatex(*clist.select(0, 2), verbose=True)` will generate a high-quality LaTeX table of the earliest capacity measures, including their sexagesimal reciprocals.


#### **8.4 Custom Metrology Series**

While the Proust presets cover standard academic needs, you can create your own `MetrologySeries`. This is particularly useful when working with non-standard archives or specific commodities.

By passing integers instead of strings, you can define the series based on the absolute count of the smallest unit (e.g., `se` for weights or volumes).

```pycon
--> from mesomath.metrology_presets import MetrologySeries

--> # Define a series using raw integer values
--> my_series = MetrologySeries(
...     name='Silver Logistics',
...     ini=1000, 
...     endlist=[1500, 2500], 
...     inclist=[100, 200], 
...     unit_class='Weight'
... )

--> # Display the custom steps
--> my_series
MetrologySeries: Silver Logistics (Weight)
-----------------------------------------------------------------
Step   | Start Value     | End Value       | Increment       
-----------------------------------------------------------------
0      | 1000            | 1500            | 100             
1      | 1500            | 2500            | 200             
-----------------------------------------------------------------
```

Now, because we used integers, we can apply it to any class; for instance:

```pycon
--> a, b, c = my_series.select(0,1)
--> bc.metrolist(a,b,c)

Babylonian capacity measurement
gur <-5- bariga <-6- ban <-10- sila <-60- gin <-180- se
|Measurement         |
|--------------------|
|5 gin 100 se        |
|6 gin 20 se         |
|6 gin 120 se        |
|7 gin 40 se         |
|7 gin 140 se        |
|8 gin 60 se         |
|8 gin 160 se        |
|10 gin              |
|11 gin 20 se        |
|12 gin 40 se        |
|13 gin 60 se        |
|13 gin 160 se       |
```

> MesoMath's ability to interpret this type of integer-based preset definition is probably useless beyond the developer's scope. Measurements such as '1 sila', '1/3 ninda', etc., will normally be used.

#### **8.5 Specialized Formatting: `subst`, `incipit` and `colophon`**
When generating the final table, you can add contextual information to the output to better reflect the nature of the transaction or the document:

* **`subst`**: Appends a specific string (like the commodity name) to the measurements.
* **`incipit`**: If set to `True` (or `1`), it only places the `subst` label at the very first and very last rows of each segment, mimicking the "header/footer" style often seen in administrative records.
* **`width`**: Manually sets the character width of the table columns.

```pycon
--> # Using the custom series for Weight (bw)
--> a, b, c = my_series.select(0, 1)
--> bw.metrolist(a, b, c, width=37, subst='ku-babbar', incipit=1, verbose=1)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement                          | Sexag. (gin)    | Reciprocal  |
|-------------------------------------|-----------------|-------------|
|(5 dis) gin (1 ges 4 u) se ku-babbar | 5:33:20         | 10:48       |
|(6 dis) gin (2 u) se                 | 6:6:40          | --igi nu--  |
|(6 dis) gin (2 ges) se               | 6:40            | 9           |
|(7 dis) gin (4 u) se                 | 7:13:20         | --igi nu--  |
|(7 dis) gin (2 ges 2 u) se           | 7:46:40         | --igi nu--  |
|(8 dis) gin (1 ges) se               | 8:20            | 7:12        |
|(8 dis) gin (2 ges 4 u) se ku-babbar | 8:53:20         | 6:45        |
|(1 u) gin                            | 10              | 6           |
|(1 u 1 dis) gin (2 u) se             | 11:6:40         | 5:24        |
|(1 u 2 dis) gin (4 u) se             | 12:13:20        | --igi nu--  |
|(1 u 3 dis) gin (1 ges) se           | 13:20           | 4:30        |
|(1 u 3 dis) gin (2 ges 4 u) se       | 13:53:20        | 4:19:12     |

```

In this example, `ku-babbar` (silver) is used as the substance. Notice how `incipit=1` ensures the label is not repeated on every single line, making the table cleaner and historically more authentic.

Finally, we can add a *colophon*:

```pycon
--> bw.metrolist(a, b, c, width=37, subst='ku-babbar', incipit=1, verbose=1, colophon=1)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement                          | Sexag. (gin)    | Reciprocal  |
|-------------------------------------|-----------------|-------------|
|(5 dis) gin (1 ges 4 u) se ku-babbar | 5:33:20         | 10:48       |
|(6 dis) gin (2 u) se                 | 6:6:40          | --igi nu--  |
|(6 dis) gin (2 ges) se               | 6:40            | 9           |
|(7 dis) gin (4 u) se                 | 7:13:20         | --igi nu--  |
|(7 dis) gin (2 ges 2 u) se           | 7:46:40         | --igi nu--  |
|(8 dis) gin (1 ges) se               | 8:20            | 7:12        |
|(8 dis) gin (2 ges 4 u) se ku-babbar | 8:53:20         | 6:45        |
|(1 u) gin                            | 10              | 6           |
|(1 u 1 dis) gin (2 u) se             | 11:6:40         | 5:24        |
|(1 u 2 dis) gin (4 u) se             | 12:13:20        | --igi nu--  |
|(1 u 3 dis) gin (1 ges) se           | 13:20           | 4:30        |
|(1 u 3 dis) gin (2 ges 4 u) se       | 13:53:20        | 4:19:12     |
--------------------------------------------------
| Grand Total: (1 dis) 5/6 mana (1 dis) gin (2 u) se ku-babbar
| Number of lines: 12 | Scribe: MesoMath 2.0.0 |
| April 2026 |
--------------------------------------------------
```

The **`colophon=True`** argument adds a summary block at the end of the table, including the total sum of the measurements, the line count, and the "scribe" (software version), mimicking the metadata found at the end of many ancient tablets.

## **III. Epigraphy: From Math to Tablet**

<div style="text-align:center;">
<div class="tablet" >

| NAM-DUB-SAR |
|:---:|
|<big>𒉆𒁾𒊬</big>|

</div>
</div>

MesoMath is first and foremost a high-precision calculator. However, its primary objective extends beyond mathematical correctness. A significant effort has been made to include two representations that reflect how quantities were actually recorded on clay: **transliteration** and **original cuneiform characters**.

### **1. Transliteration: The `.translit` Property**

MesoMath incorporates the composite metrological tables of the Old Babylonian Period (Nippur) published by **Proust (2009)** as the foundation for its transliteration engine. To achieve a representation faithful to ancient scribal practices, the library employs a two-step process:

1.  **Greedy Decomposition**: The internal decimal value (`self.dec`) is decomposed into the largest possible values corresponding to specific graphemes present in Proust’s composite lists.
2.  **Post-processing**: The resulting tokens are concatenated and re-analyzed to regroup identical units and recalculate coefficients (e.g., aggregating multiple `še` or `gin2` tokens), ensuring historical accuracy in the final string.

```pycon
--> a = bc(11223344)
--> a.translit
'3(aš) gur 2(barig) 1(ban2) še 9(diš) sila3 1(u) 1(diš) 5/6 gin2 1(u) 4(diš) še'
```

#### **Reliability Limits**

The `.translit` property is optimized for the standard ranges found in archaeological contexts. Beyond these limits, historical systems often diverged or used non-standard notations.

| Domain | Limit (Traditional) | Limit (Metric/SI) |
| :--- | :--- | :--- |
| **Capacity** | `(2 sargal) gur` (432,000 gur) | 129,600,000 litres |
| **Weight** | `(2 sargal) gu2` (432,000 gu2) | 12,960,000 kg |
| **Surface** | `(2 sargal) gan2` (129,600 gan2) | 466,560,000 m² |
| **Length** | `(2 ges2) danna` (120 danna) | 1,296,000 m |

> ⚠️ **Warning**: For values exceeding these limits, the transliteration engine enters experimental territory where results may become unpredictable.

#### **Note on Volume and Brick Metrology**

In Babylonian practice, **Volumes** and **Brick counts** do not have a dedicated unit system; they are expressed using the **Surface system** (`Bsur`).

  * **Volumes** are conceived as a surface area with a default thickness of 1 `kuš3` (cubit).
  * **Bricks** are standardized into volumes, allowing scribes to calculate counts via "surface-volume" logic.

MesoMath's `.translit` property correctly reflects this by using surface units (`sar`, `gan2`, etc.) when calling volume or brick objects.

-----

### **2. Transliteration in Tables**

You can generate metrological lists and tables using professional transliteration by passing the `translit=True` flag. This is the preferred method for generating data for academic publications.

```pycon
--> # Generating a length list with transliteration and a colophon
--> bl.metrolist("1 kus", ["5 kus", "1 ninda"], ["10 susi", "1 kus"], 
...             verbose=True, translit=True, width=25, colophon=True)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement              | Sexag. (ninda)  | Reciprocal  |
|-------------------------|-----------------|-------------|
|1(diš) kuš3              | 5               | 12          |
|1(diš) 1/3 kuš3          | 6:40            | 9           |
|1(diš) 2/3 kuš3          | 8:20            | 7:12        |
|2(diš) kuš3              | 10              | 6           |
|2(diš) 1/3 kuš3          | 11:40           | --igi nu--  |
|2(diš) 2/3 kuš3          | 13:20           | 4:30        |
|3(diš) kuš3              | 15              | 4           |
|3(diš) 1/3 kuš3          | 16:40           | 3:36        |
|3(diš) 2/3 kuš3          | 18:20           | --igi nu--  |
|4(diš) kuš3              | 20              | 3           |
|4(diš) 1/3 kuš3          | 21:40           | --igi nu--  |
|4(diš) 2/3 kuš3          | 23:20           | --igi nu--  |
|5(diš) kuš3              | 25              | 2:24        |
|1/2 ninda                | 30              | 2           |
|1/2 ninda 1(diš) kuš3    | 35              | --igi nu--  |
|1/2 ninda 2(diš) kuš3    | 40              | 1:30        |
|1/2 ninda 3(diš) kuš3    | 45              | 1:20        |
|1/2 ninda 4(diš) kuš3    | 50              | 1:12        |
|1/2 ninda 5(diš) kuš3    | 55              | --igi nu--  |
|1(diš) ninda             | 1               | 1           |
--------------------------------------------------
| Grand Total: 8(diš) 1/2 ninda 
| Number of lines: 20 | Scribe: MesoMath 2.0.0 |
| April 2026 |
--------------------------------------------------
```



-----

### **3. Cuneiform: The `.cuneiform` Property**

The cuneiform representation is derived directly from the `.translit` output. The engine maps each transliterated token to its corresponding Unicode glyph.

```pycon
--> a = bc(11223344)
--> print(a.cuneiform)
𒐁 𒄥 𒑖 𒑏 𒊺 𒐎 𒋡 𒌋 𒁹 𒑜 𒂆 𒌋 𒐉 𒊺
```

```pycon
--> print(*bc.scheme(actual=1))
gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še
--> print(*bc.scheme(cuneiform=1))
𒄥   ╼5╾  𒉿   ╼6╾  𒑏   ╼10╾  𒋡   ╼60╾  𒂆   ╼180╾  𒊺

--> print(*bw.scheme(actual=1))
gu2 <-60- ma-na <-60- gin2 <-180- še
--> print(*bw.scheme(cuneiform=1))
𒄘   ╼60╾  𒈠 𒈾   ╼60╾  𒂆   ╼180╾  𒊺

--> print(*bs.scheme(actual=1))
GAN2 <-100- sar <-60- gin2 <-180- še
--> print(*bs.scheme(cuneiform=1))
𒃷   ╼100╾  𒊬   ╼60╾  𒂆   ╼180╾  𒊺

--> print(*bl.scheme(actual=1))
danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si
--> print(*bl.scheme(cuneiform=1))
𒆜 𒁍   ╼30╾  𒍑   ╼60╾  𒃻   ╼12╾  𒌑   ╼30╾  𒋗 𒋛
```

#### **Visualizing the Script**

Cuneiform characters reside in the **Supplementary Multilingual Plane** of Unicode. To see them correctly, you must have a specialized font installed.

> ▯ **Rendering Check**: If you see empty boxes or "tofu" instead of wedges, please refer to the [Cuneiform Support](https://www.google.com/search?q=%23cuneiform-support) section for font recommendations and installation guides.

### **4. Cuneiform in Tables**

```pycon
--> # Generating a length list with cuneiform and a colophon
--> bl.metrolist("1 kus", ["5 kus", "1 ninda"], ["10 susi", "1 kus"], 
...             verbose=True, cuneiform=True, width=25, colophon=True)

Babylonian length measurement
𒆜 𒁍   ╼30╾  𒍑   ╼60╾  𒃻   ╼12╾  𒌑   ╼30╾  𒋗 𒋛
|Measurement              | Sexag. (𒃻 )     | Reciprocal  |
|-------------------------|-----------------|-------------|
|𒁹 𒌑                      |  𒐙              | 𒌋𒐖          |
|𒁹 𒑚 𒌑                    |  𒐚 𒑩            |  𒑆          |
|𒁹 𒑛 𒌑                    |  𒑄 𒎙            |  𒑂 𒌋𒐖       |
|𒐖 𒌑                      | 𒌋               |  𒐚          |
|𒐖 𒑚 𒌑                    | 𒌋𒐕 𒑩            | 𒅆 𒉡         |
|𒐖 𒑛 𒌑                    | 𒌋𒐗 𒎙            |  𒐘 𒌍        |
|𒐈 𒌑                      | 𒌋𒐙              |  𒐘          |
|𒐈 𒑚 𒌑                    | 𒌋𒐚 𒑩            |  𒐗 𒌍𒐚       |
|𒐈 𒑛 𒌑                    | 𒌋𒑄 𒎙            | 𒅆 𒉡         |
|𒐉 𒌑                      | 𒎙               |  𒐗          |
|𒐉 𒑚 𒌑                    | 𒎙𒐕 𒑩            | 𒅆 𒉡         |
|𒐉 𒑛 𒌑                    | 𒎙𒐗 𒎙            | 𒅆 𒉡         |
|𒐊 𒌑                      | 𒎙𒐙              |  𒐖 𒎙𒐘       |
|𒈦 𒃻                      | 𒌍               |  𒐖          |
|𒈦 𒃻 𒁹 𒌑                  | 𒌍𒐙              | 𒅆 𒉡         |
|𒈦 𒃻 𒐖 𒌑                  | 𒑩               |  𒐕 𒌍        |
|𒈦 𒃻 𒐈 𒌑                  | 𒑩𒐙              |  𒐕 𒎙        |
|𒈦 𒃻 𒐉 𒌑                  | 𒑪               |  𒐕 𒌋𒐖       |
|𒈦 𒃻 𒐊 𒌑                  | 𒑪𒐙              | 𒅆 𒉡         |
|𒁹 𒃻                      |  𒐕              |  𒐕          |
--------------------------------------------------
| 𒋗 𒆸 𒃲: 𒐆 𒈦 𒃻 
| 𒈬 𒋃 𒁉: 𒐀 | 𒁾 𒊬: MesoMath 2.0.0 |
| 𒌗 𒐂 𒐈 𒐈 𒐉 𒐋 𒈬 |
--------------------------------------------------
```

<div class="tablet">

|Babylonian length measurement|
|----------------------------|
|𒆜 𒁍   ╼30╾  𒍑   ╼60╾  𒃻   ╼12╾  𒌑   ╼30╾  𒋗 𒋛|

|Measurement              | Sexag. (𒃻 )     | Reciprocal  |
|-------------------------|-----------------|-------------|
|𒁹 𒌑                      |  𒐙              | 𒌋𒐖          |
|𒁹 𒑚 𒌑                    |  𒐚 𒑩            |  𒑆          |
|𒁹 𒑛 𒌑                    |  𒑄 𒎙            |  𒑂 𒌋𒐖       |
|𒐖 𒌑                      | 𒌋               |  𒐚          |
|𒐖 𒑚 𒌑                    | 𒌋𒐕 𒑩            | 𒅆 𒉡         |
|𒐖 𒑛 𒌑                    | 𒌋𒐗 𒎙            |  𒐘 𒌍        |
|𒐈 𒌑                      | 𒌋𒐙              |  𒐘          |
|𒐈 𒑚 𒌑                    | 𒌋𒐚 𒑩            |  𒐗 𒌍𒐚       |
|𒐈 𒑛 𒌑                    | 𒌋𒑄 𒎙            | 𒅆 𒉡         |
|𒐉 𒌑                      | 𒎙               |  𒐗          |
|𒐉 𒑚 𒌑                    | 𒎙𒐕 𒑩            | 𒅆 𒉡         |
|𒐉 𒑛 𒌑                    | 𒎙𒐗 𒎙            | 𒅆 𒉡         |
|𒐊 𒌑                      | 𒎙𒐙              |  𒐖 𒎙𒐘       |
|𒈦 𒃻                      | 𒌍               |  𒐖          |
|𒈦 𒃻 𒁹 𒌑                  | 𒌍𒐙              | 𒅆 𒉡         |
|𒈦 𒃻 𒐖 𒌑                  | 𒑩               |  𒐕 𒌍        |
|𒈦 𒃻 𒐈 𒌑                  | 𒑩𒐙              |  𒐕 𒎙        |
|𒈦 𒃻 𒐉 𒌑                  | 𒑪               |  𒐕 𒌋𒐖       |
|𒈦 𒃻 𒐊 𒌑                  | 𒑪𒐙              | 𒅆 𒉡         |
|𒁹 𒃻                      |  𒐕              |  𒐕          |

| 𒋗 𒆸 𒃲: 𒐆 𒈦 𒃻 |
|-----------------------------|
| 𒈬 𒋃 𒁉: 𒐀   𒁾 𒊬: MesoMath 2.0.0 |
| 𒌗 𒐂 𒐈 𒐈 𒐉 𒐋 𒈬 |

</div>


## **IV. Socio-Economic Applications**

In the ancient Near East, mathematics was the language of management. MesoMath provides specialized methods to solve the three pillars of the Babylonian economy: **labor management**, **food distribution**, and **silver-based accounting**.

### **1. Labor and Rations**

The following methods allow you to calculate the human and caloric cost of a project without manually navigating reciprocal tables.

#### **Labor Cost: `.labor_cost()`**
This method calculates the total "man-days" required for a project. You provide the total volume of work (e.g., a canal to be excavated) and the **work quota** (the amount one man is expected to finish in one day).

```pycon
--> # Excavating a small canal of 10 sar volume
--> canal = bv('10 sar')
--> quota = '20 gin'  # Standard quota: 1/3 sar per man-day
--> wages = canal.labor_cost(quota)
--> print(f"{wages} man-days required.")
30.0 man-days required.
```

#### **Food Management: `.rations()`**
Once the labor force is calculated, the next step for an administrator is feeding them. This method calculates the total grain, beer, or oil required based on the daily ration per worker.



```pycon
--> daily_grain_ration = '2 sila'
--> # Calculate total barley needed for the canal project
--> total_grain = canal.rations(work_man='20 gin', wage=daily_grain_ration)
--> total_grain
1 bariga
```

---

### **2. The Silver Standard: `.silver_payments()`**

While rations were the primary means of subsistence, silver served as the unit of account for higher-level transactions and professional wages. The `.silver_payments()` method translates physical work into its equivalent weight in silver.

```pycon
--> # A construction project involving 2 sar-b of bricks
--> bricks = bb('2 sar')
--> silver_wage = '8 se' # Daily wage in silver
--> # Calculate cost based on a quota of 1 sar-b per day
--> total_silver = bricks.silver_payments(work_man='1 sar', wage=silver_wage)
--> total_silver
16 se
```



---

### **3. Construction Engineering (`Bbri`)**

As discussed in Section 6, the `Bbri` class is not just for counting; it is a tool for architectural planning. By combining the `Nalbanum` coefficients with labor methods, you can estimate the entire lifecycle of a building project:

1.  **Volume**: Calculate the physical space of the walls (`Bvol`).
2.  **Count**: Convert volume to bricks using `.bricks(nalbanum)` (`Bbri`).
3.  **Logistics**: Use `.labor_cost()` to see how many workers are needed to mold or carry those bricks.

> **Historical Context**: The standard work quotas used in these examples (like 1/3 *sar* of earth per day) are derived directly from the **Mathematical Susa Texts** and the **Old Babylonian "coefficient lists"** (*pikkurtum*).


## **V. Automation and Extension**

### **1. Scripting with `babcalc`**

While the interactive REPL is ideal for exploration, research often requires batch processing of large datasets or the reproduction of complex calculations. `babcalc` acts as a command-line interface (CLI) that can execute Python scripts directly.

#### **CLI Usage**
```bash
$ babcalc -h
Usage:
  babcalc                Launch interactive REPL
  babcalc <script.py>    Execute a script and exit
  babcalc -i <script.py> Execute a script and stay in interactive mode
```

* **The `-i` flag**: This is essential for debugging. It runs your script and then leaves the session open, allowing you to inspect the final state of your variables.
* **Compatibility**: By design, `babcalc -i` does not auto-import its internal classes into the script's namespace. This ensures that your `.py` scripts are **standard Python code** that can be shared and run by anyone with the `mesomath` library installed.

MesoMath is designed to handle multi-step mathematical procedures. A prime example is the reconstruction of ancient reciprocal algorithms. The following script implements two methods described by Duncan J. Melville (2005) to find the reciprocal of a multi-digit sexagesimal number.

**Case Study: The Reciprocal of 2:5**: Taken from [Duncan J. Melville: Reciprocals and Reciprocal algorithms in Mesopotamian Mathematics (2005)](https://www.researchgate.net/publication/237309438_RECIPROCALS_AND_RECIPROCAL_ALGORITHMS_IN_MESOPOTAMIAN_MATHEMATICS).  In this example, we apply the "Simple Reciprocal Algorithm" and "The Technique" to find the inverse of $2;5$. Save the following code as `Melville.py`:


```python
# Example of use of `BabN` class

from mesomath.babn import BabN

# Example 1: Searching the reciprocal of 2:5  according to D. J. Melville (2005)
# from Table 2. Simple Reciprocal algorithm

d1 = BabN("2:5")
r1 = d1.tail()
r2 = r1.rec()
r3 = d1 * r2
r4 = r3.rec()
r5 = r4 * r2

print(f"{d1 = }")
print(f"{r1 = }")
print(f"{r2 = }")
print(f"{r3 = }")
print(f"{r4 = }")
print(f"{r5 = }\n")

print(f"Result: {r5 = }\n")

print(f"\nTesting: {d1 * r5 = }")

# Example 2: from Table 3. using *The Technique*

r1 = d1.tail()
r2 = r1.rec()
r3 = d1.head() * r2
r4 = r3 + BabN(1)
r5 = r4.rec()
r6 = r5 * r2

print(f"{d1 = }")
print(f"{r1 = }")
print(f"{r2 = }")
print(f"{r3 = }")
print(f"{r4 = }")
print(f"{r5 = }")
print(f"{r6 = }")

print(f"\nResult: {r6 = }")

print(f"\nTesting: {d1 * r6 = }")
```

**Execution**: Running this script via `babcalc` provides a step-by-step trace of the Babylonian logic:

```bash
$ babcalc Melville.py
d1 = 2:5
r1 = 5
r2 = 12
r3 = 25:0
r4 = 2:24
r5 = 28:48

Result: r5 = 28:48


Testing: d1 * r5 = 1:0:0:0
d1 = 2:5
r1 = 5
r2 = 12
r3 = 24
r4 = 25
r5 = 2:24
r6 = 28:48

Result: r6 = 28:48

Testing: d1 * r6 = 1:0:0:0
```
> **Expert Insight**: The result `1:0:0:0` represents the sexagesimal unit. Since Babylonian math used a **floating-place system**, this confirms that $2;5 \times 0;28,48 = 1$.
---

### **2. Advanced Topic: Extending Metrology**

MesoMath's greatest strength is its **polymorphic architecture**. You are not restricted to the built-in units. By inheriting from base classes like `Blen` (Length) or `Bcap` (Capacity), you can define custom systems for specific cities, periods, or professional niches.

(vertical-problem)=
#### **The "Vertical Problem": Custom Height Class**
In many tablets, vertical measurements (depth of a canal, height of a wall) use length unit names but fixed ratios for calculation. We can create a dedicated `bh` (Babylonian Height) class in just a few lines:

```python
from mesomath.npvs import Blen, Bsur, Bvol

class bh(Blen):
    title: str = "Babylonian Height Measurement"
    ubase: int = 1  # Standardizes calculations around the 'kus' (cubit)
```

Because `bh` inherits from `Blen`, it is fully compatible with the rest of the library. You can multiply a standard surface (`Bsur`) by your custom height (`bh`) to get a volume (`Bvol`) without any errors.

---

### **3. Case Study: Late Babylonian Period (LBP)**

The metrology of the Late Babylonian period shifted significantly (e.g., the introduction of the *GAR*). We can implement this entire system by creating a new module (e.g., `lateb.py`):

```python
from mesomath.npvs import Bcap, Bvol

class LBcap(Bcap):
    """Late Babylonian: gur <-5- bariga <-6- ban2 <-10- sila3 <-10- GAR"""
    title = "Late Babylonian capacity"
    uname = "gar sila ban bariga gur".split()
    ufact = [10, 10, 6, 5]
    siv = 0.1 # 1 gar = 0.1 litres
    
    def vol(self):
        # Specific conversion logic for LBP
        return LBvol(int(round(self.dec / (100/6))))
```

#### **Running the Extension**
Once defined, load your custom metrology into the calculator:

```bash
$ babcalc -i lateb.py
```

```pycon
--> a = LBcap('1000 sila')
--> a.SI()
'100.0 litres'
--> a.vol()
3 gin 60 se  # Converted to LBP volume standards
```

### **Why Extend MesoMath?**
1.  **Chronological Flexibility**: Adapt the tool for Neo-Sumerian, Old Assyrian, or Seleucid data.
2.  **Regional Variations**: Account for the different *sila* sizes used in Mari vs. Nippur.
3.  **Automatic Tools**: Your custom classes automatically inherit `.metrolist()`, `.translit()`, and `.cuneiform()` capabilities.

<center>

<strong><big> 𒍻 jccsvq 𒁾𒊬  𒐞𒐞𒐞 𒐗 𒐏 𒐋 </big></strong>

</center>



## **VI. Reference & Appendices**

(systems-SGC)=
### Appendix A: Use of System C, S and G in MesoMath Metrology

According to {ref}`Proust's: Numerical and Metrological Graphemes: From Cuneiform to Transliteration.  Table 9 <ref-Proust3>`

|Measurement| System | Unit   | Class            |
|------------|--------|--------|------------------|
| capacities | C      | gin2   | Bcap             |
| capacities | C	  | sila3  | Bcap             |
| capacities | C*     | ban2   | Bcap             |
| capacities | C*     | bariga | Bcap             |
| capacities | S      | gur	   | Bcap             |
| weights    | C      | še     | Bwei             |
| weights    | C	  | gin2   | Bwei             |
| weights    | C	  | ma-na  | Bwei             |
| weights    | S	  | gu2    | Bwei             |
| surfaces   | C      | še     | Bsur, Bvol, Bbri |
| surfaces   | C      | gin2   | Bsur, Bvol, Bbri |
| surfaces   | C      | sar    | Bsur, Bvol, Bbri |
| surfaces   | G      | GAN2   | Bsur, Bvol, Bbri |
| lengths    | C      | šu-si  | Blen             |
| lengths    | C      | kuš3   | Blen             |
| lengths    | C      | ninda  | Blen             |
| lengths    | C      | UŠ     | Blen             |
| lengths    | C      | danna  | Blen             |

>**(*)**: Note These are not in the reference.

### 1. **The Metrological Catalog**: Full list of units and coefficients.
### 2. **Cuneiform Font Guide**: Solving the "Tofu" problem.
### 3. **Commodity Lists & Conversion factors**.






## Metrology OLD!!!

### Basics

As explained in the [Introduction](#babcalc-intro), `babcalc` already has the metrological classes `BabN, Blen, Bsur,`... pre-imported as `bn, bl, bs,` etc.

```python
from mesomath.babn import BabN as bn
from mesomath.npvs import Blen as bl
from mesomath.npvs import Bsur as bs
from mesomath.npvs import Bvol as bv
from mesomath.npvs import Bcap as bc
from mesomath.npvs import Bwei as bw
from mesomath.npvs import Bbri as bb
from mesomath.npvs import BsyG as bG
from mesomath.npvs import BsyS as bS
from mesomath.npvs import BsyC as bC
from mesomath.npvs import BsyK as bK

```

This is what the classes `bl`, `bs`, `bv`, `bc`, `bw`, `bG`, `bS` and `bb` represent:

    class  bl: Babylonian length system:
               danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si

    class  bs: Babylonian surface system:
               GAN2 <-100- sar <-60- gin2 <-180- še

    class  bv: Babylonian volume system:
               GAN2 <-100- sar <-60- gin2 <-180- še

    class  bc: Babylonian capacity system:
               gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še

    class  bw: Babylonian weight system:
               gu2 <-60- ma-na <-60- gin2 <-180- še

    Class  bb: Babylonian brick counting system:
               GAN2 <-100- sar <-60- gin2 <-180- še

    class  bG: Babylonian counting System G:
               šar2-gal <-6- šar'u <-10- šar2 <-6- bur'u <-10- bur3 <-3- eše3 <-6- iku

    class  bS: Babylonian counting System S:
               šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- aš
    
    class  bC: Babylonian counting System C:
               u <-10- diš

    class  bK: Babylonian counting System K:
               šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- diš


However, for ease of writing, the real or academic names of the units in these metrological systems have been simplified by removing capital letters, numbers, hyphens, and diacritics. Therefore, for introduction of measurements, we will use the following unit names:

Class|Metrology|Units
-----|---------|-----
bl| Babylonian length system|  susi, kus, ninda, us, danna
bs| Babylonian surface system|  se, gin, sar, gan
bv| Babylonian volume system|  se, gin, sar, gan
bc| Babylonian capacity system|  se, gin, sila, ban, bariga, gur
bw| Babylonian weight system|  se, gin, mana, gu
bG| Babylonian System G|  iku, ese, bur, buru, sar, saru, sargal
bS| Babylonian System S|  dis, u, ges, gesu, sar, saru, sargal
bC| Babylonian System C|  dis, u
bb| Babylonian brick counting system|  se gin sar gan

>Note that scribes wrote volumes as an equivalent surface area multiplied by a standard height of 1 kus; thus, they used the same metrology for surfaces and volumes. Here, however, two different classes will be used, so that one can multiply a surface area by a length to obtain a volume, but one cannot multiply a volume by a length to obtain a four-dimensional volume, which was probably beyond the scribes' understanding.

At any time, you can review the names of the units in each system and their factors through the following, e.g., for capacities:

```pycon
--> bc.uname
['se', 'gin', 'sila', 'ban', 'bariga', 'gur']
--> bc.ufact
[180, 60, 10, 6, 5]
```
the cumulative factors:

```pycon
--> bc.cfact
[1, 180, 10800, 108000, 648000, 3240000]
```

and the academic names:

```pycon
--> bc.aname
['še', 'gin2', 'sila3', 'ban2', 'bariga', 'gur']
```

or, otherwise:

```pycon
--> print(*bc.scheme(bc))
gur <-5- bariga <-6- ban <-10- sila <-60- gin <-180- se
--> print(*bc.scheme(bc,1))
gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še
```

In a similar way to what we saw for sexagesimal numbers with the `bn` class. We can introduce measurements in two different ways:

```pycon
--> a = bl(11111)
--> a
30 ninda 10 kus 11 susi
--> b = bl('5 ninda 25 susi')
--> b
5 ninda 25 susi
```

In the first case, `a` is defined as a certain (integer) number of times the smallest unit ("susi" in the case of lengths). In the second case, we define the value for `b` textually. Note that we can only use integer values ​​in both cases. Both input methods are available for all classes.

>In fact, there is a [**third input method**](#third-input-method).

Once you have defined measurements, you can "explain" them:

```pycon
--> a.explain()
This is a Babylonian length measurement: 30 ninda 10 kus 11 susi
    Metrology:  danna <-30- us <-60- ninda <-12- kus <-30- susi
    Factor with unit 'susi':  1 30 360 21600 648000
measurement in terms of the smallest unit: 11111 (susi)
Sexagesimal floating value of the above: 3:5:11
Approximate SI value: 185.18333333333334 meters
--> 
--> b.explain()
This is a Babylonian length measurement: 5 ninda 25 susi
    Metrology:  danna <-30- us <-60- ninda <-12- kus <-30- susi
    Factor with unit 'susi':  1 30 360 21600 648000
measurement in terms of the smallest unit: 1825 (susi)
Sexagesimal floating value of the above: 30:25
Approximate SI value: 30.416666666666668 meters
```

That will give us information about the nature of the measurement and the properties of the measurement system being used.

Note that the value given as "Sexagesimal floating value of the above:" is generated by the `.sex()` method; however, this method accepts a numeric parameter to indicate the unit relative to which this sexagesimal floating value is calculated. This parameter defaults to zero, indicating the first unit in the list provided by `.explain()`: `Unit names: ['susi', 'kus', 'ninda', 'us', 'danna']`

```pycon
--> a.sex()   # susi as the base unit
3:5:11
--> a.sex(0)  # the same as .sex()
3:5:11
--> a.sex(1)  # kus as the base unit
6:10:22
--> a.sex(2)  # ninda as the base unit
30:51:50
--> a.sex(3)  # us as the base unit
30:51:50
--> a.sex(4)  # danna as the base unit
1:1:43:40
```

This will be useful if you want to recreate **metrological lists** yourself. For example, code:

```python
from mesomath import Blen as bl

ls = []
for i in range(1, 10):
    ls.append(str(i) + " susi")

for i in "10 15 20 25".split():
    ls.append(i + " susi")

ls.append("1 kus")
for i in "10 15 20 25".split():
    ls.append("1 kus " + i + " susi")

ls.append("2 kus")
for i in ls:
    x = bl(i)
    print(f"{str(x).ljust(15)} -> {str(x.sex(2)).rjust(6)}")

```


will print this excerpt of the metrological table for length using ninda (x.sex(2)) as base unit:

```pycon
1 susi          ->     10
2 susi          ->     20
3 susi          ->     30
4 susi          ->     40
5 susi          ->     50
6 susi          ->      1
7 susi          ->   1:10
8 susi          ->   1:20
9 susi          ->   1:30
10 susi         ->   1:40
15 susi         ->   2:30
20 susi         ->   3:20
25 susi         ->   4:10
1 kus           ->      5
1 kus 10 susi   ->   6:40
1 kus 15 susi   ->   7:30
1 kus 20 susi   ->   8:20
1 kus 25 susi   ->   9:10
2 kus           ->     10
```

(See page 8 of [Floating calculation in Mesopotamia](https://hal.science/hal-01515645v2/document) by Christine Proust).

But you will rarely need to resort to programming, since **MesoMath** has specialized resources for building metrological lists and tables:

*   The [`metrotable`](#metrotable-tutorial) tool, which specializes in printing segments of metrological list and tables.
*   The [`mtlookup`](#mtlookup-tutorial) tool that simulates direct and inverse searches in metrological tables.
*   The [`.metrolist()`](#metrolist) method that works with all metrological classes, including [those you define yourself](#advanced-topics).

For instance for horizontal distances (base unit ninda):

```pycon
--> bl.metrolist('1 kus', '5 kus', '1 kus', verbose=True)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement         | Sexag. (ninda)      | Reciprocal  |
|--------------------|---------------------|-------------|
|1 kus               | 5                   | 12          |
|2 kus               | 10                  | 6           |
|3 kus               | 15                  | 4           |
|4 kus               | 20                  | 3           |
|5 kus               | 25                  | 2:24        |

```


For vertical distances (base unit kus):

```pycon
--> bl.metrolist('1 kus', '5 kus', '1 kus', verbose=True, ubase =1)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement         | Sexag. (kus)        | Reciprocal  |
|--------------------|---------------------|-------------|
|1 kus               | 1                   | 1           |
|2 kus               | 2                   | 30          |
|3 kus               | 3                   | 20          |
|4 kus               | 4                   | 15          |
|5 kus               | 5                   | 12          |

```

But we will explore `.metrolist()` and its sibling methods in depth [below](#metrolist).

You can get also the metrological value of an object directly using the `.metval()` method:

```pycon
--> bl('1 kus 15 susi').metval()
7:30
```


We finish this section with the `.si()` and `.SI()` conversion methods that show us the approximate equivalence of the Babylonic measurementss in the International System of Units:

```pycon
--> w = bw(' 1 mana 3 gin')
--> w.si()
0.525
--> w.SI()
'0.525 kilograms'
```

### Operations

For objects of the **same** class, the following operations are available:

* Addition
* Subtraction (returns the absolute value of the difference)
* Multiplication by a number
* Division by a number
* Logical operations

Let's look at some examples:

```pycon
--> a >= b
True
--> a+b
35 ninda 11 kus 6 susi
--> a-b
25 ninda 9 kus 16 susi
--> b-a                   # a-b == b-a !!!
--> a-b == b-a
True
25 ninda 9 kus 16 susi
--> 2*a
1 us 1 ninda 8 kus 22 susi
--> b*2
10 ninda 1 kus 20 susi
--> b*2.5
12 ninda 8 kus 2 susi
--> a/2
15 ninda 5 kus 6 susi
--> (a+2*b)/5
8 ninda 2 kus 12 susi
--> (a+2*b)/5.3
7 ninda 8 kus 25 susi
```

Additionally, for length measurements we can multiply them together to obtain surfaces and volumes, and for surfaces we can multiply them by lengths to obtain volumes:

```pycon
--> c = bl('2 kus')
--> c
2 kus
--> s=a*b
--> s
1 gan 56 sar 27 gin 138 se
--> s.explain()
This is a Babylonian surface measurement: 1 gan 56 sar 27 gin 138 se
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 1689798 (se)
Sexagesimal floating value of the above: 7:49:23:18
Approximate SI value: 5632.66 square meters
--> v=s*c
--> v
3 gan 12 sar 55 gin 96 se
--> v.explain()
This is a Babylonian volume measurement: 3 gan 12 sar 55 gin 96 se
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 3379596 (se)
Sexagesimal floating value of the above: 15:38:46:36
Approximate SI value: 5632.66 cube meters

--> v2=a*b*c
--> v2 == v
True
```

### Systems S and G

Finally, in cases like this:

```pycon
--> a = bv('128 gan')
--> a
128 gan
```

we might prefer to see the coefficients of the units expressed in the sexagesimal systems C, S and G (see [Appendix](#systems-SGC) for the use of System C, S and G in MesoMath Metrology):

```pycon
--> bv.prtsex=True  # switch to sexagesimal mode
--> a
(7 bur 2 iku) gan
```

This changes the default for objects of the `bv` class and makes the output more closely mimic the way the measurements were actually inscribed on clay tablets, but it complicates things for the modern reader:

```pycon
--> a = bv('128 gan 133 se')
--> a
(7 bur 2 iku) gan (7 bur 1 ese 1 iku) se
```

If you want this to be the default for all classes, use:

```python
from mesomath.npvs import MesoM
MesoM.prtsex = True
```

(third-input-method)=
### Third input method


The third input method cited above makes use of these types of strings; in fact, the parentheses have been introduced to make them easier to parse as input:

```pycon
--> b = bv('460800 gan 44 sar 20 gin')
--> b
(7 sargal 6 sar 4 buru) gan (4 u 4 dis) sar (2 u) gin
--> c = bv('(7 sargal 6 sar 4 buru) gan (4 u 4 dis) sar (2 u) gin')
--> c
(7 sargal 6 sar 4 buru) gan (4 u 4 dis) sar (2 u) gin
--> bv.prtsex = False
--> c
460800 gan 44 sar 20 gin
```

Note that we can also enter the coefficients of the units in sexagesimal form:

```pycon
--> b = bv('2:8:0:0 gan 44 sar 20 gin')
--> b
460800 gan 44 sar 20 gin
```

but only using `:` as a separator.

### Fractions

There is also support for entering the **principal fractions**: 1/6, 1/3, 1/2, 2/3, 5/6 (and only for them), they can be entered in several ways:

```pycon
--> a=bl('0+1/3 ninda')
--> a
4 kus
--> a=bl('+1/3 ninda')
--> a
4 kus
--> a=bl('1/3 ninda')
--> a
4 kus
--> a=bl('2 + 1/3 ninda')
--> a
2 ninda 4 kus
--> a=bl('2 1/3 ninda')
--> a
2 ninda 4 kus
--> a=bl('21/3 ninda')
--> a
2 ninda 4 kus

```


For output using 1/3, 1/2, 2/3, 5/6 fractions, use the `.prtf()` method:

```pycon
--> a=bl(11223344)
--> a
17 danna 9 us 35 ninda 11 kus 14 susi
--> a.prtf()
'17 danna 9 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
```

and if you wish also include the less frecuently used fraction `1/6`:

```pycon
--> a.prtf(1)
'17 1/6 danna 4 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
```

If you activate `prtsex` you get:

```pycon
--> bl.prtsex=True
--> a.prtf()
'(1 u 7 dis) danna (9 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi'
--> a.prtf(1)
'(1 u 7 dis) 1/6 danna (4 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi'
```

These results can be used for input:

```pycon
--> bl.prtsex=0
--> b=bl('(1 u 7 dis) 1/6 danna (4 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi')
--> b
17 danna 9 us 35 ninda 11 kus 14 susi
--> b.prtf()
'17 danna 9 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
--> b.prtf(1)
'17 1/6 danna 4 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
--> b.dec
11223344
--> c=bl(a.prtf(1))
--> c.dec
11223344
```

### Academic names

Since v1.1.0, the .prtf() method has a second switch that allows the academic unit names to be used in the output:

```pycon
--> a=bl(11223344)
--> a.prtf()
'17 danna 9 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
--> a.prtf(1)
'17 1/6 danna 4 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
--> a.prtf(1,1)
'17 1/6 danna 4 1/2 UŠ 5 5/6 ninda 1 1/3 kuš3 4 šu-si'
--> bl.prtsex=True
--> a.prtf(0,1)
'(1 u 7 dis) danna (9 dis) 1/2 UŠ (5 dis) 5/6 ninda (1 dis) 1/3 kuš3 (4 dis) šu-si'
--> a.prtf(1,1)
'(1 u 7 dis) 1/6 danna (4 dis) 1/2 UŠ (5 dis) 5/6 ninda (1 dis) 1/3 kuš3 (4 dis) šu-si'

```

This kind of string can also be used as input:

```pycon
--> b=bl('(1 u 7 dis) 1/6 danna (4 dis) 1/2 UŠ (5 dis) 5/6 ninda (1 dis) 1/3 kuš3 (4 dis) šu-si')
--> b.dec
11223344
```

equivalent to:

```pycon
--> b=bl(a.prtf(1,1))
--> b.dec
11223344
```

### Volume vs. Capacity

There were two systems for measuring volume: 

* **capacities**, used to measure grain, beer, and other types of food and goods
* **volume** proper, used to measure everything else. 

Here, they are represented by the metrological classes `Bcap` (imported in `babcalc` as `bc`) and `Bvol` (imported as `bv`), respectively. Since they are two systems for measuring the same physical quantity, we can convert quantities from one system to the other with the methods `Bvol.cap()` and `Bcap.vol()`:

```pycon
--> a = bv('1 gin')
--> a.explain()
This is a Babylonian volume measurement: 1 gin
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 180 (se)
Sexagesimal floating value of the above: 3
Approximate SI value: 0.3 cube meters
--> b = a.cap()
--> b.explain()
This is a Babylonian capacity measurement: 1 gur
    Metrology:  gur <-5- bariga <-6- ban <-10- sila <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 108000 648000 3240000
measurement in terms of the smallest unit: 3240000 (se)
Sexagesimal floating value of the above: 15
Approximate SI value: 300.0 litres
--> (b.vol()).explain()
This is a Babylonian volume measurement: 1 gin
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 180 (se)
Sexagesimal floating value of the above: 3
Approximate SI value: 0.3 cube meters
```

### Bricks

Volume measurements were frequently transformed into their **"brick" equivalents**. These were measured in "*sar-b*" (units or packages of 720 bricks), and each brick type was characterized by its *{ref}`Nalbanum <ref-robson-math>`*, or the number of *sar-b* of that type that fits in 1 *sar* of volume. 

>*"The Nalbanum is a conversion coefficient. While a volume is fixed in space, the number of bricks it contains depends on their size. The Nalbanum acts as the multiplier to go from 'theoretical volume' to 'actual brick count'.*

The `.bricks()` method allows us to perform this transformation:

```pycon
--> a = bv('1 sar')
--> a
1 sar
--> b = a.bricks()
--> b
1 sar
--> b.explain()
This is a Babylonian brick counting: 1 sar
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 10800 (se)
Sexagesimal floating value of the above: 3
Approximate SI value: 720.0 bricks
```

This is for  *nalbanum* =1.0  type-12 bricks, for type-2 bricks with decimal *nalbanum* = 7.20:

```pycon
--> b = a.bricks(7.20)
--> b
7 sar 12 gin
--> b.SI()
'5184.0 bricks'
```

A *sar* is equivalent to 10800 *še* and also to 720 bricks; therefore, each brick is equivalent to $10800/720=15$ *še*.
Then, if we have 10000 type-2 bricks,  we can do:

```pycon
--> c = bb(15 * 10000)  # 15 še/brick
--> c
13 sar 53 gin 60 se
--> c.SI()
'10000.0 bricks'
```

`c` is a `Bbri` object:

```pycon
--> c.explain()
This is a Babylonian brick counting: 13 sar 53 gin 60 se
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 150000 (se)
Sexagesimal floating value of the above: 41:40
Approximate SI value: 10000.0 bricks
```

that you can convert into a volume:

```pycon
--> d = c.vol(7.20)  # 7.20 nalbanum of type-2 bricks
--> d.explain()
This is a Babylonian volume measurement: 1 sar 55 gin 133 se
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 20833 (se)
Sexagesimal floating value of the above: 5:47:13
Approximate SI value: 34.721666666666664 cube meters
```



Here is a nalbanum table by 
[Carlos Maza](https://personal.us.es/cmaza/mesopotamia/edificios.htm#Tipos%20de%20ladrillos) (Spanish only, sorry):

|Brick type|Nalb. (dec.) |Nalb. (sex.)|
|------|---------|-----|
|  1(*)   |    9.00 |9|
|  1a  |     8.33| 8:20|
|  2(*)   |     7.20 |7:12|
|3 |  5.40 | 5:24|
|4 |   5.00 |5|
|5 |  4.80 |4:48|
|7 |   3.33 |3:20|
|8 |  2.70 |2:42|
|9 |  2.25 |2:15|
|10|  1.875 |1:52:30|
|11|  1.20| 1:12|
|12(*)|1.00 |1  |

**(*)** Notes:
| Type | Sexagesimal | Comment |
|:--- |:--- |:--- |
|**1** | **9** | Standard square brick (*sig-al-ur-ra*). |
|**2** | **7;12** | 2/3 kùš brick. |
|**12** | **1** | The unit value, used as a reference for transportation calculations. |

(metrolist)=
### `.metrolist()` method

| Destination | Method | State |
:--- |:--- |:--- |
|**Console / MD** | `.metrolist()` | Active (User-friendly) |
|**Web / Sphinx** | `.metrohtml()` | Active (Via `metro_generator`) |
|**Academic** | `.metrolatex()` | Active (Via `metro_generator`) |
|**Data Science** | `.metrocsv()` | Planned (Via `metro_generator`) |

#### Basics

The `.metrolist()` method generates segments of metrological lists and tables. It requires three mandatory parameters:

* initial value
* final value
* increment

which can be strings or integers:

```pycon
--> bw.metrolist('10 gin', '1 mana', '10 gin')

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         |
|--------------------|
|10 gin              |
|20 gin              |
|30 gin              |
|40 gin              |
|50 gin              |
|1 mana              |
--> bw('10 gin').dec
1800
--> bw('1 mana').dec
10800
--> bw.metrolist(1800, 10800, 1800)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         |
|--------------------|
|10 gin              |
|20 gin              |
|30 gin              |
|40 gin              |
|50 gin              |
|1 mana              |
```

and a certain number of {meth}`optional parameters<.metrolist>`. For example, if we want a metrological table instead of the metrological list above, we will use `verbose=True` or its equivalent `verbose=1`:

```pycon
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         | Sexag. (gin)        | Reciprocal  |
|--------------------|---------------------|-------------|
|10 gin              | 10                  | 6           |
|20 gin              | 20                  | 3           |
|30 gin              | 30                  | 2           |
|40 gin              | 40                  | 1:30        |
|50 gin              | 50                  | 1:12        |
|1 mana              | 1                   | 1           |
```

if we want to use the main fractions:

```pycon
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, fractions=1)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         | Sexag. (gin)        | Reciprocal  |
|--------------------|---------------------|-------------|
|10 gin              | 10                  | 6           |
|1/3 mana            | 20                  | 3           |
|1/2 mana            | 30                  | 2           |
|2/3 mana            | 40                  | 1:30        |
|5/6 mana            | 50                  | 1:12        |
|1 mana              | 1                   | 1           |
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, fractions=2)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         | Sexag. (gin)        | Reciprocal  |
|--------------------|---------------------|-------------|
|1/6 mana            | 10                  | 6           |
|1/3 mana            | 20                  | 3           |
|1/2 mana            | 30                  | 2           |
|2/3 mana            | 40                  | 1:30        |
|5/6 mana            | 50                  | 1:12        |
|1 mana              | 1                   | 1           |
```

```pycon
--> bw.prtsex = True   # switch to sexagesimal mode
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, fractions=1)

Babylonian weight measurement
gu <-60- mana <-60- gin <-180- se
|Measurement         | Sexag. (gin)        | Reciprocal  |
|--------------------|---------------------|-------------|
|(1 u) gin           | 10                  | 6           |
|1/3 mana            | 20                  | 3           |
|1/2 mana            | 30                  | 2           |
|2/3 mana            | 40                  | 1:30        |
|5/6 mana            | 50                  | 1:12        |
|(1 dis) mana        | 1                   | 1           |
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, fractions=1, actual=1)

Babylonian weight measurement
gu2 <-60- ma-na <-60- gin2 <-180- še
|Measurement         | Sexag. (gin2)       | Reciprocal  |
|--------------------|---------------------|-------------|
|(1 u) gin2          | 10                  | 6           |
|1/3 ma-na           | 20                  | 3           |
|1/2 ma-na           | 30                  | 2           |
|2/3 ma-na           | 40                  | 1:30        |
|5/6 ma-na           | 50                  | 1:12        |
|(1 dis) ma-na       | 1                   | 1           |
```
etc.

>**Note**: As you can see, the previous outputs are in **Markdown table format**, so if you use Markdown for your documents, you're in luck, you just have to copy and paste the result from the terminal into your document and that's it. But you can also paste it into an intermediate `.csv` file that can be read by any spreadsheet (indicating the pipe `|` character as the column separator) and from there you can copy and paste it into your word processor or presentations.

The option `echo = False` suppresses terminal output. Instead, `.metrolist()` returns a list of strings with the rows of the table. This will be useful for your scripts.

```pycon
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, fractions=1, echo=0)
['|(1 u) gin           | 10                  | 6           |', '|1/3 mana            | 20                  | 3           |', '|1/2 mana            | 30                  | 2           |', '|2/3 mana            | 40                  | 1:30        |', '|5/6 mana            | 50                  | 1:12        |', '|(1 dis) mana        | 1                   | 1           |']
--> a = bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, fractions=1, echo=0)
--> for _ in a:
...     print(_)
... 
|(1 u) gin           | 10                  | 6           |
|1/3 mana            | 20                  | 3           |
|1/2 mana            | 30                  | 2           |
|2/3 mana            | 40                  | 1:30        |
|5/6 mana            | 50                  | 1:12        |
|(1 dis) mana        | 1                   | 1           |

```

#### Segmented lists

You can use lists for the `mmax` and `step` parameters to generate segmented lists with different increments, as was the case with the metrological lists and tables found in archaeological sites.

```pycon
--> bl.metrolist("1 kus", ["5 kus", "1 ninda"], ["10 susi", "1 kus"],verbose=1,fractions=1)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement         | Sexag. (ninda)      | Reciprocal  |
|--------------------|---------------------|-------------|
|1 kus               | 5                   | 12          |
|1 1/3 kus           | 6:40                | 9           |
|1 2/3 kus           | 8:20                | 7:12        |
|2 kus               | 10                  | 6           |
|2 1/3 kus           | 11:40               | --igi nu--  |
|2 2/3 kus           | 13:20               | 4:30        |
|3 kus               | 15                  | 4           |
|3 1/3 kus           | 16:40               | 3:36        |
|3 2/3 kus           | 18:20               | --igi nu--  |
|1/3 ninda           | 20                  | 3           |
|1/3 ninda 1/3 kus   | 21:40               | --igi nu--  |
|1/3 ninda 2/3 kus   | 23:20               | --igi nu--  |
|1/3 ninda 1 kus     | 25                  | 2:24        |
|1/2 ninda           | 30                  | 2           |
|1/2 ninda 1 kus     | 35                  | --igi nu--  |
|2/3 ninda           | 40                  | 1:30        |
|2/3 ninda 1 kus     | 45                  | 1:20        |
|5/6 ninda           | 50                  | 1:12        |
|5/6 ninda 1 kus     | 55                  | --igi nu--  |
|1 ninda             | 1                   | 1           |
```

```pycon
--> bl.metrolist("10 susi", ["2 kus", "12 kus", "5 ninda"], ["5 susi", "1 kus","6 kus"],verbose=1,fractions=1)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement         | Sexag. (ninda)      | Reciprocal  |
|--------------------|---------------------|-------------|
|1/3 kus             | 1:40                | 36          |
|1/2 kus             | 2:30                | 24          |
|2/3 kus             | 3:20                | 18          |
|5/6 kus             | 4:10                | 14:24       |
|1 kus               | 5                   | 12          |
|1 kus 5 susi        | 5:50                | --igi nu--  |
|1 1/3 kus           | 6:40                | 9           |
|1 1/2 kus           | 7:30                | 8           |
|1 2/3 kus           | 8:20                | 7:12        |
|1 5/6 kus           | 9:10                | --igi nu--  |
|2 kus               | 10                  | 6           |
|3 kus               | 15                  | 4           |
|1/3 ninda           | 20                  | 3           |
|1/3 ninda 1 kus     | 25                  | 2:24        |
|1/2 ninda           | 30                  | 2           |
|1/2 ninda 1 kus     | 35                  | --igi nu--  |
|2/3 ninda           | 40                  | 1:30        |
|2/3 ninda 1 kus     | 45                  | 1:20        |
|5/6 ninda           | 50                  | 1:12        |
|5/6 ninda 1 kus     | 55                  | --igi nu--  |
|1 ninda             | 1                   | 1           |
|1 1/2 ninda         | 1:30                | 40          |
|2 ninda             | 2                   | 30          |
|2 1/2 ninda         | 2:30                | 24          |
|3 ninda             | 3                   | 20          |
|3 1/2 ninda         | 3:30                | --igi nu--  |
|4 ninda             | 4                   | 15          |
|4 1/2 ninda         | 4:30                | 13:20       |
|5 ninda             | 5                   | 12          |
```

#### Siblings methods

The `.metrohtml()` and `.metrolatex()` methods make use of the above to create metrological lists and tables in HTML and LaTeX format. Estos métodos aceptan las mismas opciones que `.metrolist()` junto con algunas otras que les son propias:

```pycon
--> a=bw.metrohtml('10 gin', '1 mana', '10 gin', verbose=True, fractions=1, echo=0, file='testhtml')
--> Exported 6 rows to 'testhtml.html' (raw style)
```

escribirá el fichero `testhtml.html`

```html
  <table>
  <tr>
    <th>Measurement</th>
    <th>Sexag. (gin)</th>
    <th>Reciprocal</th>
  </tr>
  <tr>
    <td>(1 u) gin</td>
    <td>10</td>
    <td>6</td>
  </tr>
  <tr>
    <td>1/3 mana</td>
    <td>20</td>
    <td>3</td>
  </tr>
  <tr>
    <td>1/2 mana</td>
    <td>30</td>
    <td>2</td>
  </tr>
  <tr>
    <td>2/3 mana</td>
    <td>40</td>
    <td>1:30</td>
  </tr>
  <tr>
    <td>5/6 mana</td>
    <td>50</td>
    <td>1:12</td>
  </tr>
  <tr>
    <td>(1 dis) mana</td>
    <td>1</td>
    <td>1</td>
  </tr>
</table>
```
which will be rendered on your HTML page as:

<div>
  <table>
  <tr>
    <th>Measurement</th>
    <th>Sexag. (gin)</th>
    <th>Reciprocal</th>
  </tr>
  <tr>
    <td>(1 u) gin</td>
    <td>10</td>
    <td>6</td>
  </tr>
  <tr>
    <td>1/3 mana</td>
    <td>20</td>
    <td>3</td>
  </tr>
  <tr>
    <td>1/2 mana</td>
    <td>30</td>
    <td>2</td>
  </tr>
  <tr>
    <td>2/3 mana</td>
    <td>40</td>
    <td>1:30</td>
  </tr>
  <tr>
    <td>5/6 mana</td>
    <td>50</td>
    <td>1:12</td>
  </tr>
  <tr>
    <td>(1 dis) mana</td>
    <td>1</td>
    <td>1</td>
  </tr>
</table>
</div>

De modo similar, `.metrolatex()`:

```pycon
--> a=bw.metrolatex('10 gin', '1 mana', '10 gin', verbose=True, fractions=1, echo=0,
 file='testlatex')
--> Exported to 'testlatex.tex' (LaTeX HEX-Safe style)
```

will write the file `testlatex.tex`:


```latex
\begin{table}[h]
  \centering
  \begin{tabular}{lll}
    \toprule
    Measurement & Sexag. ({\cuneifont gin}) & Reciprocal \\
    \midrule
    (1 u) gin & 10 & 6 \\
    1/3 mana & 20 & 3 \\
    1/2 mana & 30 & 2 \\
    2/3 mana & 40 & 1:30 \\
    5/6 mana & 50 & 1:12 \\
    (1 dis) mana & 1 & 1 \\
    \bottomrule
  \end{tabular}
\end{table}
```

You can also use the option `full_page = True` to create files with the complete document, HTML or LaTex that you can use as independent tests.


The `cuneiform` option will be described [below](#metrolist-cuneiform).

Please see the options for {meth}`.metrolist()<.metrolist>`, {meth}`.metrohtml()<.metrohtml>`, {meth}`.metrolatex()<.metrolatex>`.

>Please note that not all combinations of options can have an effect simultaneously; for example, you will not be able to see the actual or academic names of the units if you do not activate the fractions.

## Epigraphy

MesoMath is first and foremost a calculator; therefore, its primary objective is the mathematical correctness of its operations and the consistency of the ten alternative expressions provided for metrological measures. Nevertheless, significant effort has been made to include two additional representations that reflect how these quantities were actually recorded on clay: **transliteration** and **original cuneiform characters**.

### Transliteration: The `.translit` property

MesoMath incorporates the composite metrological tables of the Old Babylonian Period (Nippur) published by {ref}`Proust (2009) <ref-Proust3>` as the foundation for its transliteration engine. To achieve a representation faithful to ancient scribal practices, the library employs a two-step process:

1.  **Greedy Decomposition**: The internal decimal value (`self.dec`) is decomposed into the largest possible values corresponding to specific graphemes present in Proust’s composite lists.
2.  **Post-processing**: The resulting tokens are concatenated and re-analyzed to regroup identical units and recalculate coefficients (e.g., aggregating multiple `še` or `gin2` tokens), ensuring historical accuracy in the final string.


#### Reliability Limits

The `.translit` property is designed to provide reliable results within the following practical limits. Beyond these values, the historical systems often diverged or used non-standard notations, and results should be treated as experimental:

| Measure | Limit (Traditional) | Limit (Decimal/SI) |
| :--- | :--- | :--- |
| **Capacity** | `(2 sargal) gur` (432,000 gur) | 129,600,000 litres |
| **Weight** | `(2 sargal) gu2` (432,000 gu2) | 12,960,000 kg |
| **Surface** | `(2 sargal) gan2` (129,600 gan2) | 466,560,000 m² |
| **Length** | `(2 ges2) danna` (120 danna) | 1,296,000 m |

> **Warning**: For values exceeding these limits, the transliteration engine may produce unpredictable results ("expect disaster").

⚠️ **Note on Volume and Brick Metrology**

It is crucial to note that in Babylonian mathematics, **Volumes** and **Brick counts** do not have a dedicated unit system. Instead, they are expressed using the **Surface system** (`Bsur`).

* **Volumes**: A volume is conceived as a surface area with a default thickness of 1 `kuš3` (cubit). Therefore, a `1 sar` volume is actually a block of $1 \times 1$ `ninda` base and $1$ `kuš3` height.
* **Bricks**: Bricks were standardized into volumes, allowing scribes to calculate the number of bricks needed for a wall by simply calculating its total "surface-volume".

When using MesoMath for volume or brick calculations, the `.translit` property will correctly reflect the surface units (`sar`, `gan2`, etc.) used in these archaeological contexts.

**Example of high-precision decomposition:**

```pycon
--> a = bc('(2 sargal) gur')
--> b = bc(a.dec - 1)
--> b.translit 
'1(šargal)gal 5(šar’u) 9(šar2) 5(geš’u) 9(geš2) 5(u) 9(aš) gur 4(barig) 5(ban2) še 9(diš) 5/6 sila3 9(diš) 5/6 gin2 2(u) 9(diš) še'
```

**Metrological list and tables**

For generating metrological lists and tables with transliteration, use the `translit=True` flag in the respective generator methods.


```pycon
--> bl.metrolist("1 kus",["5 kus","1 ninda"],["10 susi","1 kus"],verbose=1,translit=1,width=25,colophon=1)

Babylonian length measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement              | Sexag. (ninda)  | Reciprocal  |
|-------------------------|-----------------|-------------|
|1(diš) kuš3              | 5               | 12          |
|1(diš) 1/3 kuš3          | 6:40            | 9           |
|1(diš) 2/3 kuš3          | 8:20            | 7:12        |
|2(diš) kuš3              | 10              | 6           |
|2(diš) 1/3 kuš3          | 11:40           | --igi nu--  |
|2(diš) 2/3 kuš3          | 13:20           | 4:30        |
|3(diš) kuš3              | 15              | 4           |
|3(diš) 1/3 kuš3          | 16:40           | 3:36        |
|3(diš) 2/3 kuš3          | 18:20           | --igi nu--  |
|4(diš) kuš3              | 20              | 3           |
|4(diš) 1/3 kuš3          | 21:40           | --igi nu--  |
|4(diš) 2/3 kuš3          | 23:20           | --igi nu--  |
|5(diš) kuš3              | 25              | 2:24        |
|1/2 ninda                | 30              | 2           |
|1/2 ninda 1(diš) kuš3    | 35              | --igi nu--  |
|1/2 ninda 2(diš) kuš3    | 40              | 1:30        |
|1/2 ninda 3(diš) kuš3    | 45              | 1:20        |
|1/2 ninda 4(diš) kuš3    | 50              | 1:12        |
|1/2 ninda 5(diš) kuš3    | 55              | --igi nu--  |
|1(diš) ninda             | 1               | 1           |
--------------------------------------------------
| Grand Total: 8(diš) 1/2 ninda 
| Number of lines: 20 | Scribe: MesoMath 2.0.0rc0 |
| April 2026 |
--------------------------------------------------

```


### Cuneiform, the `.cuneiform` property.

The cuneiform representation is derived directly from the `.translit` output. The engine maps each transliterated token to its corresponding Unicode glyph.

**Note on Rendering**: Cuneiform characters are part of the Supplementary Multilingual Plane of Unicode. Correct on-screen rendering requires a specialized font (e.g., *Sumerian*, *Akkadian*, or *Noto Sans Cuneiform*). Without these, the system may display "tofu" (empty boxes). Please refer to the [Cuneiform Support](#cuneiform-support) section for installation instructions.

(scripting)=
## Scripting

`babcalc`, in addition to serving as an interface for interactive work, can execute `.py` scripts for batch processing. Let's look at its options:

```bash
$ babcalc -h
babcalc 1.3.0 - Command Line Interface

Usage:
  babcalc                 Launch interactive REPL
  babcalc <script.py>     Execute a script
  babcalc -i <script.py>  Execute a script and stay in interactive mode
  babcalc -m <module>     Run a library module (Reserved for future use)
  babcalc --help          Show this message
```

The `-i` option allows you to run a script and remain in interactive mode, which is important for debugging. We show an [example](#lbp-metrology) below.

**Note:** By design, `babcalc` will **NOT** import any of the MesoMath classes when called with the `-i` option. Using this option requires writing pure Python scripts that can be run on other systems directly using the Python interpreter (once the package is installed). This is done for compatibility and program sharing purposes.

The `-m` option is reserved for future use. Currently, there are no modules in MesoMath that can be run this way.

(advanced-topics)=
## Advanced Topic: Extending Metrology

One of the core strengths of **MesoMath v{{ release }}** is its extensibility. You are not limited to the built-in Babylonian units; you can define your own metrological systems by inheriting from the base classes.

(vertical-class)=
### The "Vertical Problem": Defining Height

In many Mesopotamian mathematical problems, vertical measurements (height or depth) are treated with specific units that, while sharing the same names as lengths, behave differently in calculations.

Let's define a custom class `bh` (Babylonian Height) that inherits from the length system (`bl` or `Blen`) but fixes the base unit to the *kuš3* (cubit).

```python
from mesomath.npvs import Blen, Bsur, Bvol

# We define our custom height class
class bh(Blen):
    title: str = "Babylonian Height Measurement"
    ubase: int = 1  # Fixed to 'kus' (cubit)

```

### Seamless Interaction

Thanks to the polymorphic design of **v{{ release }}**, your custom classes are recognized by the core engine. You can multiply a standard surface (`Bsur`) by your new height (`bh`) to obtain a volume (`Bvol`) without any type errors.

```python
# 1. Define a surface of 1 sar
area = Bsur('1 sar')

# 2. Define a height using our custom class
height = bh('1 kus')

# 3. Calculate volume (Area * Height)
# The system recognizes 'bh' as a valid length for this operation.
volume = area * height

print(f"Volume: {volume}") 
# Output: 1 sar

```

(automatic-utilities)=
### Automatic Utilities

By inheriting from `MesoM` (via `Blen`), your new class automatically gains all the new administrative and diagnostic tools of this version:

1. **Metrological Lists/Tables**: Generate tables for your custom units instantly.

Please see the options for {meth}`.metrolist()<.metrolist>` method.

```pycon
--> from mesomath.npvs import Blen, Bsur, Bvol
--> 
--> # We define our custom height class
--> class bh(Blen):
...     title: str = "Babylonian Height Measurement"
...     ubase: int = 1  # Fixed to 'kus' (cubit)
... 
--> bh.metrolist('1 kus', '5 kus', '1 kus', verbose=True, ubase=None)

Babylonian Height Measurement
danna <-30- us <-60- ninda <-12- kus <-30- susi
|Measurement         | Sexag. (kus)        | Reciprocal  |
|--------------------|---------------------|-------------|
|1 kus               | 1                   | 1           |
|2 kus               | 2                   | 30          |
|3 kus               | 3                   | 20          |
|4 kus               | 4                   | 15          |
|5 kus               | 5                   | 12          |
--> bh.metrolist('10 susi', '2 kus', '5 susi', verbose=True, width=30,fractions=2,actual=True)

Babylonian Height Measurement
danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si
|Measurement                   | Sexag. (kuš3)                 | Reciprocal  |
|------------------------------|-------------------------------|-------------|
|1/3 kuš3                      | 20                            | 3           |
|1/2 kuš3                      | 30                            | 2           |
|2/3 kuš3                      | 40                            | 1:30        |
|5/6 kuš3                      | 50                            | 1:12        |
|1 kuš3                        | 1                             | 1           |
|1 1/6 kuš3                    | 1:10                          | --igi nu--  |
|1 1/3 kuš3                    | 1:20                          | 45          |
|1 1/2 kuš3                    | 1:30                          | 40          |
|1 2/3 kuš3                    | 1:40                          | 36          |
|1 5/6 kuš3                    | 1:50                          | --igi nu--  |
|1/6 ninda                     | 2                             | 30          |
--> bh.prtsex = 1
--> bh.metrolist('10 susi', '2 kus', '5 susi', verbose=True, width=30,fractions=2,actual=True)

Babylonian Height Measurement
danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si
|Measurement                   | Sexag. (kuš3)                 | Reciprocal  |
|------------------------------|-------------------------------|-------------|
|1/3 kuš3                      | 20                            | 3           |
|1/2 kuš3                      | 30                            | 2           |
|2/3 kuš3                      | 40                            | 1:30        |
|5/6 kuš3                      | 50                            | 1:12        |
|(1 dis) kuš3                  | 1                             | 1           |
|(1 dis) 1/6 kuš3              | 1:10                          | --igi nu--  |
|(1 dis) 1/3 kuš3              | 1:20                          | 45          |
|(1 dis) 1/2 kuš3              | 1:30                          | 40          |
|(1 dis) 2/3 kuš3              | 1:40                          | 36          |
|(1 dis) 5/6 kuš3              | 1:50                          | --igi nu--  |
|1/6 ninda                     | 2                             | 30          |
```


2. **Economic Calculations**: Use the new methods for labor costs.

The following three methods can help us study the economic problems commonly addressed by scribes. They offer a shortcut, saving us from having to work with metrological tables and reciprocal numbers.

#### `.labor_cost()`

This method calculates the cost of a project in terms of man-days to be paid or the number of workers needed to complete the project in one day, based on the work to be carried out and the work quota that each worker is expected to complete per day.

Please see the options for {meth}`.labor_cost()<.labor_cost>` method.

```pycon
--> canal = bv('10 sar')
--> quota = '20 gin'  # 1/3 sar per day
--> wages = canal.labor_cost(quota)
--> print(f"{wages} men required to finish in a day.")
30.0 men required to finish in a day.
```

#### `.rations()`

This method calculates the cost of a project in rations of barley, beer, oil, etc. based on the work to be carried out and the work quota that each worker is expected to complete per day.

Please see the options for {meth}`.rations()<.rations>` method.


```pycon
--> daily_ration = '2 sila'
--> total_grain = canal.rations(work_man='20 gin', wage=daily_ration)
--> print(f"Total barley: {total_grain}")
Total barley: 1 bariga
```


#### `.silver_payments()`

This method calculates the cost of a project in monetary terms (silver weight) based on the work to be carried out and the work quota that each worker is expected to complete per day.

Please see the options for {meth}`.silver_payments()<.silver_payments>` method.


```pycon
--> bricks = bb('2 sar')
--> silver_wage = '8 se'
--> total_silver = bricks.silver_payments(work_man='1 sar', wage=silver_wage)
--> print(f"Total silver payment: {total_silver}")
Total silver payment: 16 se
```



(lbp-metrology)=
### Late Babylonian Period Metrology


**MesoMath** is designed to work with the metrology of the Old Babylonian period, but it can be extended to use the metrology of other periods. For example, for the {ref}`Late Babylonian Period <ref-Proust2>`, we can start by defining a class `LBcap` for the capacities in a file `lateb.py`:

```python
from mesomath.npvs import Bcap, Bvol


class LBcap(Bcap):  # Capacity
    """This class implement Non-Place-Value System arithmetic
    for Late Babylonian Period capacity units:

        **gur <-5- bariga <-6- ban2 <-10- sila3 <-10- GAR**

    """

    title: str = "Late Babylonian capacity measurement"
    uname: list[str] = "gar sila ban bariga gur".split()
    aname: list[str] = "GAR sila3 ban2 bariga gur".split()
    ufact: list[int] = [10, 10, 6, 5]
    cfact: list[int] = [1, 10, 100, 600, 3000]
    siv: float = 0.1
    siu: str = "litres"
    ubase: int = 3  # bariga

    def vol(self) -> object:
        """Convert capacity to volume measurement

        :return: volume measurement
        :rtype: "Bvol"
        """
        return LBvol(int(round(self.dec/(100/6))))

class LBvol(Bvol):  # Volume
    """This class implement Non-Place-Value System arithmetic
    for Late Babylonian Period volume units:

        **GAN2 <-100- sar <-60- gin2 <-180- še**

    """
    title: str = "Late Babylonian volume measurement"
    
    def cap(self) -> object:
        """Convert volume to capacity measurement"""
        return LBcap(int(round(self.dec*(100/6))))
```

and then:

```bash
$ babcalc -i lateb.py 
```

```pycon
--> a = LBcap('1000 sila')
--> b = a.vol()
--> b
3 gin 60 se
--> b.explain() 
This is a Late Babylonian volume measurement: 3 gin 60 se
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
measurement in terms of the smallest unit: 600 (se)
Sexagesimal floating value of the above: 10
Approximate SI value: 0.9999999999999999 cube meters
--> c=b.cap() 
--> c
3 gur 1 bariga 4 ban
--> c.SI() 
'1000.0 litres'
--> c.explain() 
This is a Late Babylonian capacity measurement: 3 gur 1 bariga 4 ban
    Metrology:  gur <-5- bariga <-6- ban <-10- sila <-10- gar
    Factor with unit 'gar':  1 10 100 600 3000
measurement in terms of the smallest unit: 10000 (gar)
Sexagesimal floating value of the above: 2:46:40
Approximate SI value: 1000.0 litres
-->
--> LBcap.metrolist('1 bariga','3 bariga', '1 ban',1)
1 bariga             | 1              
1 bariga 1 ban       | 1:10           
1 bariga 2 ban       | 1:20           
1 bariga 3 ban       | 1:30           
1 bariga 4 ban       | 1:40           
1 bariga 5 ban       | 1:50           
2 bariga             | 2              
2 bariga 1 ban       | 2:10           
2 bariga 2 ban       | 2:20           
2 bariga 3 ban       | 2:30           
2 bariga 4 ban       | 2:40           
2 bariga 5 ban       | 2:50           
3 bariga             | 3              
```

etc. but we should also redefine the rest of the classes to ensure consistency in the operations with the new units.

(cuneiform-support)=
## 𒍻 Advanced Topic: Cuneiform Support


<div style="text-align:center;">
<div class="tablet" >

| NAM-DUB-SAR |
|:---:|
|<big>𒉆𒁾𒊬</big>|

</div>
</div>

>*The art of writing on clay, known in Sumerian as NAM-DUB-SAR (𒉆𒁾𒊬), is in the heart of MesoMath's visual engine.*


MesoMath goes beyond mere calculation; it allows you to represent metrological data in its original historical script. This chapter covers how to enable, display, and export cuneiform signs for academic publications and web displays.

𒍻
 

### 𒍻 1. The Cuneiform Font Requirement

To prevent "tofu" (empty boxes) or broken characters, your system or document compiler must have access to a compatible font. We recommend **Noto Sans Cuneiform**, which covers the Sumero-Akkadian Unicode block.

* **For Web/HTML:** MesoMath automatically links to Google Fonts.
* **For LaTeX/PDF:** You must provide the font file (see the LaTeX section below).

Consult [Font Configuration](#install-font) for more information.

𒍻

### 𒍻 2 BabN class

```pycon
--> a=bn('33.34.0.45.0.0')
--> print(a.to_cunei())
𒌍𒐗 𒌍𒐘  𒐏𒐙   
--> print(a.to_cunei(alter=True))
𒌍𒐗 𒌍𒐘  𒑩𒐙   
--> print(a.to_cunei(alter=True, stroke=True))
𒌍𒐗 𒌍𒐘 𒃵 𒑩𒐙 𒃵 𒃵 
--> print(a.to_cunei(alter=False, stroke=True))
𒌍𒐗 𒌍𒐘 𒃵 𒐏𒐙 𒃵 𒃵 
```

𒍻


### 𒍻 3 Metrological classes

#### 𒍻 `.scheme()` method

Use the parameter `cuneiform = True` or equivalently `cuneiform = 1` to see the factor diagram in cuneiform.
Please see the options for {meth}`.scheme()<mesomath.npvs._MesoM.scheme>`

**Lengths**:

```pycon
--> print(*bl.scheme(actual=1))
danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si
--> print(*bl.scheme(cuneiform=1))
𒆜𒁍   ╼30╾  𒍑   ╼60╾  𒃻   ╼12╾  𒌑   ╼30╾  𒋗𒋛
```
**Surface**:

```pycon
--> print(*bs.scheme(actual=1))
GAN2 <-100- sar <-60- gin2 <-180- še
--> print(*bs.scheme(cuneiform=1))
𒃷   ╼100╾  𒊬   ╼60╾  𒂆   ╼180╾  𒊺
```
**Volumes**:

```pycon
--> print(*bv.scheme(actual=1))
GAN2 <-100- sar <-60- gin2 <-180- še
--> print(*bv.scheme(cuneiform=1))
𒃷   ╼100╾  𒊬   ╼60╾  𒂆   ╼180╾  𒊺
```
**Capacities**:

```pycon
--> print(*bc.scheme(actual=1))
gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še
--> print(*bc.scheme(cuneiform=1))
𒄥   ╼5╾  𒉿   ╼6╾  𒑏   ╼10╾  𒋡   ╼60╾  𒂆   ╼180╾  𒊺
```
**Weights**:

```pycon
--> print(*bw.scheme(actual=1))
gu2 <-60- ma-na <-60- gin2 <-180- še
--> print(*bw.scheme(cuneiform=1))
𒄘   ╼60╾  𒈠𒈾   ╼60╾  𒂆   ╼180╾  𒊺
```
**Bricks**:

```pycon
--> print(*bb.scheme(actual=1))
GAN2 <-100- sar <-60- gin2 <-180- še
--> print(*bb.scheme(cuneiform=1))
𒃷   ╼100╾  𒊬   ╼60╾  𒂆   ╼180╾  𒊺
```
**System S**:

```pycon
--> print(*bS.scheme(actual=1))
šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- aš
--> print(*bS.scheme(cuneiform=1))
𒊹   ╼6╾  𒐬   ╼10╾  𒊬   ╼6╾  𒐞   ╼10╾  𒐕   ╼6╾  𒌋   ╼10╾  𒀸
```
**System G**:

```pycon
--> print(*bG.scheme(actual=1))
šar2-gal <-6- šar'u <-10- šar2 <-6- bur'u <-10- bur3 <-3- eše3 <-6- iku
--> print(*bG.scheme(cuneiform=1))
𒊹   ╼6╾  𒐬   ╼10╾  𒊬   ╼6╾  𒐴   ╼10╾  𒌋   ╼3╾  𒑘   ╼6╾  𒀸
```
**System SKL**:

```pycon
--> print(*bK.scheme(actual=1))
šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- diš
--> print(*bK.scheme(cuneiform=1))
𒊹   ╼6╾  𒐬   ╼10╾  𒊬   ╼6╾  𒐞   ╼10╾  𒐕   ╼6╾  𒌋   ╼10╾  𒁹
```

𒍻

#### 𒍻 `.cuneiform` property

#### 𒍻 `.to_cunei()` method

This method attempts, to the extent that the complexity of the code allows, to imitate the idiosyncratic way in which ancient scribes wrote physical quantities. This means the use of fractions and the additive sexagesimal systems C, S, G, and SKL. Let's look at some examples starting with a high integer:



```pycon
--> a = bS(11223344)
--> a.prtf()
'51 sargal 5 saru 7 sar 3 gesu 5 ges 4 u 4 as'
--> print(a.to_cunei(onesixth=True))
𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲 𒐬𒐬𒐬𒐬𒐬 𒐅 𒐞𒐞𒐞 𒐙 𒐏 𒐂
--> a = bG(11223344)
--> a.prtf()
'173 sargal 1 saru 1 sar 5 buru 9 bur 2 iku'
--> print(a.to_cunei(onesixth=True))
𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲𒐲 𒐬 𒀸 𒐴𒐴𒐴𒐴𒐴 𒐔 𒐀
--> a = bl(11223344)
--> a.prtf()
'17 danna 9 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi'
--> print(a.to_cunei(onesixth=True))
𒌋𒐌𒑡 𒆜𒁍 𒐉𒈦 𒍑 𒐊𒑜 𒃻 𒁹𒑚 𒌑 𒐉 𒋗𒋛
--> a = bs(11223344)
--> a.prtf()
'10 gan 39 sar 11 5/6 gin 14 se'
--> print(a.to_cunei(onesixth=True))
𒌋 𒃷 𒌍𒐇𒑡 𒁹𒑜 𒂆 𒌋𒐉 𒊺
--> a = bv(11223344)
--> a.prtf()
'10 gan 39 sar 11 5/6 gin 14 se'
--> print(a.to_cunei(onesixth=True))
𒌋 𒃷 𒌍𒐇𒑡 𒁹𒑜 𒂆 𒌋𒐉 𒊺
--> a = bw(11223344)
--> a.prtf()
'17 gu 19 mana 11 5/6 gin 14 se'
--> print(a.to_cunei(onesixth=True))
𒌋𒐌𒑡 𒄘 𒐎𒑡 𒈠𒈾 𒁹𒑜 𒂆 𒌋𒐉 𒊺
--> a = bc(11223344)
--> a.prtf()
'3 gur 2 bariga 1 1/2 ban 4 sila 11 5/6 gin 14 se'
--> print(a.to_cunei(onesixth=True))
𒐈 𒄥 𒐖𒑡 𒁹 𒈦 𒑏 𒐉𒑡 𒋡 𒁹𒑜 𒂆 𒌋𒐉 𒊺
--> a = bb(11223344)
--> a.prtf()
'10 gan 39 sar 11 5/6 gin 14 se'
--> print(a.to_cunei(onesixth=True))
𒌋 𒃷 𒌍𒐇𒑡 𒁹𒑜 𒂆 𒌋𒐉 𒊺
```

and then with a small one:


```pycon
--> a=bK(121)
--> print(a.to_cunei())
𒐖 𒋢𒋛 𒁹                     # 𒋢𒋛 ("ŠU-SI") intercalated to avoid confusion (𒐖𒁹)
```

If you wish, you can add the commodity name; for instance, for silver weights:

```pycon
--> print(bw('1 mana').to_cunei(subst='ku_babbar'))
𒁹 𒈠𒈾  𒆬𒌓
```

[Appendix C](#commodities-list) lists all the commodity names that may be used.


Please see the options for {meth}`.to_cunei()<mesomath.npvs._MesoM.to_cunei>`

𒍻

(metrolist-cuneiform)=
#### 𒍻 `.metrolist()` method and its siblings

```pycon
--> bl.metrolist('1 kus','1 ninda','2 kus', verbose=1, fractions=2,cuneiform=1,
actual=1, width=22,full_page=1,file='caca')

Babylonian length measurement
𒆜𒁍   ╼30╾  𒍑   ╼60╾  𒃻   ╼12╾  𒌑   ╼30╾  𒋗𒋛
|Measurement           | Sexag. (𒃻)            | Reciprocal  |
|----------------------|-----------------------|-------------|
|𒁹 𒌑                   |  𒐙                    | 𒌋𒐖          |
|𒑡 𒃻 𒁹 𒌑               | 𒌋𒐙                    |  𒐘          |
|𒑚 𒃻 𒁹 𒌑               | 𒎙𒐙                    |  𒐖 𒎙𒐘       |
|𒈦 𒃻 𒁹 𒌑               | 𒌍𒐙                    | 𒅆𒉡          |
|𒑛 𒃻 𒁹 𒌑               | 𒑩𒐙                    |  𒐕 𒎙        |
|𒑜 𒃻 𒁹 𒌑               | 𒑪𒐙                    | 𒅆𒉡          |
```

The previous cuneiform output should appear correctly aligned on almost any modern terminal; but, due to the variable width of the cuneiform glyphs, it is next to impossible to get it to appear aligned in an HTML document like this using a monospaced font, so henceforth the outputs will be presented in table format.


```pycon
--> bl.metrolist('1 kus','1 ninda','2 kus', verbose=1, fractions=2,cuneiform=1,
actual=1, width=22,full_page=1,file='caca')
```

output:


<div class="tablet" >

|Babylonian length measurement|
|---|
|𒆜𒁍   ╼30╾  𒍑   ╼60╾  𒃻   ╼12╾  𒌑   ╼30╾  |

|Measurement           | Sexag. (𒃻)            | Reciprocal  |
|----------------------|-----------------------|-------------|
|𒁹 𒌑                   |  𒐙                    | 𒌋𒐖          |
|𒑡 𒃻 𒁹 𒌑               | 𒌋𒐙                    |  𒐘          |
|𒑚 𒃻 𒁹 𒌑               | 𒎙𒐙                    |  𒐖 𒎙𒐘       |
|𒈦 𒃻 𒁹 𒌑               | 𒌍𒐙                    | 𒅆𒉡          |
|𒑛 𒃻 𒁹 𒌑               | 𒑩𒐙                    |  𒐕 𒎙        |
|𒑜 𒃻 𒁹 𒌑               | 𒑪𒐙                    | 𒅆𒉡          |

</div>

If you wish, you can add the commodity name; for instance, for silver weights:

```pycon
--> bw.metrolist('10 gin', '1 mana', '10 gin', verbose=True, cuneiform=1, subst='ku_babbar')
```

output:


<div class="tablet" >

|Babylonian weight measurement|
|---|
|𒄘   ╼60╾  𒈠𒈾   ╼60╾  𒂆   ╼180╾  𒊺|

|Measurement         | Sexag. (𒂆)          | Reciprocal  |
|--------------------|---------------------|-------------|
|𒌋 𒂆  𒆬𒌓             | 𒌋                   |  𒐚          |
|𒑚 𒈠𒈾  𒆬𒌓            | 𒎙                   |  𒐗          |
|𒈦 𒈠𒈾  𒆬𒌓            | 𒌍                   |  𒐖          |
|𒑛 𒈠𒈾  𒆬𒌓            | 𒑩                   |  𒐕 𒌍        |
|𒑜 𒈠𒈾  𒆬𒌓            | 𒑪                   |  𒐕 𒌋𒐖       |
|𒁹 𒈠𒈾  𒆬𒌓            |  𒐕                  |  𒐕          |

</div>

Another example:


```pycon
--> bc.metrolist(180, 280, 20,verbose=1,fractions=1, cuneiform=1, subst="kas")
```

output:


<div class="tablet" >


|Babylonian capacity measurement|
|---|
|𒄥   ╼5╾  𒉿   ╼6╾  𒑏   ╼10╾  𒋡   ╼60╾  𒂆   ╼180╾  𒊺|


|Measurement         | Sexag. (𒂆)          | Reciprocal  |
|--------------------|---------------------|-------------|
|𒁹 𒂆  𒁉              |  𒐕                  |  𒐕          |
|𒁹 𒂆 𒎙 𒊺  𒁉          |  𒐕  𒐚 𒑩             | 𒑪𒐘          |
|𒁹 𒂆 𒐏 𒊺  𒁉          |  𒐕 𒌋𒐗 𒎙             | 𒅆 𒉡         |
|𒁹𒑚 𒂆  𒁉             |  𒐕 𒎙                | 𒑩𒐙          |
|𒁹𒑚 𒂆 𒎙 𒊺  𒁉         |  𒐕 𒎙𒐚 𒑩             | 𒅆 𒉡         |
|𒁹𒈦 𒂆 𒌋 𒊺  𒁉         |  𒐕 𒌍𒐗 𒎙             | 𒅆 𒉡         |

</div>


[Appendix C](#commodities-list) lists all the commodity names that may be used.

The `.metrohtml()` and `.metrolatex()` methods also work in cuneiform using the `cuneiform=True` option.

When exporting to a full HTML page with cuneiform enabled, MesoMath applies a CSS class called `.tablet`. This style mimics the appearance of a Mesopotamian clay tablet, using warm tones and optimized font sizes for the complex glyphs; for instance:


```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Cuneiform&display=swap" rel="stylesheet">
  <style>
    body { background-color: #f4f1ea; font-family: sans-serif; display: flex; justify-content: center; padding: 20px; }
    .tablet { background-color: #e2c08d; border-radius: 15px; padding: 25px; 
              box-shadow: inset 2px 2px 5px #bc9a6c, 5px 5px 15px rgba(0,0,0,0.3);
              border: 1px solid #cdaa7d; max-width: fit-content; }
    table { border-collapse: collapse; background: rgba(255,255,255,0.1); }
    th, td { border: 1px solid rgba(0,0,0,0.1); padding: 8px 15px; text-align: left; }
    th { background: rgba(0,0,0,0.05); color: #5d4037; font-variant: small-caps; }
    td { font-family: "Noto Sans Cuneiform", sans-serif; font-size: 1.2rem; }
    caption { margin-bottom: 10px; font-weight: bold; color: #5d4037; }
  </style>
</head>
<body>
<div class="tablet">
  <table class="table">
  <tr>
    <th>Measurement</th>
    <th>Sexag. (𒃻)</th>
    <th>Reciprocal</th>
  </tr>
  <tr>
    <td>𒁹&thinsp;𒌑</td>
    <td>𒐙</td>
    <td>𒌋𒐖</td>
  </tr>
  <tr>
    <td>𒑡&thinsp;𒃻&thinsp;𒁹&thinsp;𒌑</td>
    <td>𒌋𒐙</td>
    <td>𒐘</td>
  </tr>
  <tr>
    <td>𒑚&thinsp;𒃻&thinsp;𒁹&thinsp;𒌑</td>
    <td>𒎙𒐙</td>
    <td>𒐖&thinsp;𒎙𒐘</td>
  </tr>
  <tr>
    <td>𒈦&thinsp;𒃻&thinsp;𒁹&thinsp;𒌑</td>
    <td>𒌍𒐙</td>
    <td>𒅆𒉡</td>
  </tr>
  <tr>
    <td>𒑛&thinsp;𒃻&thinsp;𒁹&thinsp;𒌑</td>
    <td>𒑩𒐙</td>
    <td>𒐕&thinsp;𒎙</td>
  </tr>
  <tr>
    <td>𒑜&thinsp;𒃻&thinsp;𒁹&thinsp;𒌑</td>
    <td>𒑪𒐙</td>
    <td>𒅆𒉡</td>
  </tr>
</table>
</div>
</body>
</html>
```

Exporting cuneiform to LaTeX is notoriously difficult due to encoding issues. MesoMath solves this by using **Hexadecimal Escaping**. Instead of exporting the glyphs directly (which often break in the clipboard), it exports ASCII-safe Unicode point references.

**Workflow for Overleaf/XeLaTeX:**

1. **Generate the file:**
```python
bl.metrolatex(cuneiform=True, full_page=True, file="my_table")

```


2. **Upload the Font:** Upload `NotoSansCuneiform-Regular.ttf` to your Overleaf project.
3. **Compile with XeLaTeX:** Set the compiler to XeLaTeX in the project settings.
4. **The Result:** MesoMath uses `\symbol{"XXXXX}` commands. This ensures that even if you can't "see" the signs in the editor, they will render perfectly in the PDF.

```latex
\documentclass{article}
\usepackage{booktabs}
\usepackage{fontspec}
% Make sure to upload NotoSansCuneiform.ttf to Overleaf
\newfontfamily\cuneifont{NotoSansCuneiform.ttf}[Path = .//]
\begin{document}
\begin{table}[h]
  \centering
  \begin{tabular}{lll}
    \toprule
    Measurement & {\cuneifont Sexag. ({\cuneifont \symbol{"120FB}}) & Reciprocal} \\
    \midrule
    {\cuneifont \symbol{"12079}\,\symbol{"12311}} & {\cuneifont \symbol{"12419}} & {\cuneifont \symbol{"1230B}\symbol{"12416}} \\
    {\cuneifont \symbol{"12461}\,\symbol{"120FB}\,\symbol{"12079}\,\symbol{"12311}} & {\cuneifont \symbol{"1230B}\symbol{"12419}} & {\cuneifont \symbol{"12418}} \\
    {\cuneifont \symbol{"1245A}\,\symbol{"120FB}\,\symbol{"12079}\,\symbol{"12311}} & {\cuneifont \symbol{"12399}\symbol{"12419}} & {\cuneifont \symbol{"12416}\,\symbol{"12399}\symbol{"12418}} \\
    {\cuneifont \symbol{"12226}\,\symbol{"120FB}\,\symbol{"12079}\,\symbol{"12311}} & {\cuneifont \symbol{"1230D}\symbol{"12419}} & {\cuneifont \symbol{"12146}\symbol{"12261}} \\
    {\cuneifont \symbol{"1245B}\,\symbol{"120FB}\,\symbol{"12079}\,\symbol{"12311}} & {\cuneifont \symbol{"12469}\symbol{"12419}} & {\cuneifont \symbol{"12415}\,\symbol{"12399}} \\
    {\cuneifont \symbol{"1245C}\,\symbol{"120FB}\,\symbol{"12079}\,\symbol{"12311}} & {\cuneifont \symbol{"1246A}\symbol{"12419}} & {\cuneifont \symbol{"12146}\symbol{"12261}} \\
    \bottomrule
  \end{tabular}
\end{table}
\end{document}
```
Please see the options for {meth}`.metrolist()<.metrolist>`, {meth}`.metrohtml()<.metrohtml>`, {meth}`.metrolatex()<.metrolatex>`.

𒍻



### 𒍻 4. Troubleshooting "Tofu"

If you see empty boxes:

* **In HTML:** Ensure you have an active internet connection to load the Google Font.
* **In LaTeX:** Check that the `.ttf` filename in your project matches exactly what is defined in the `\newfontfamily` command in your `.tex` file.

---

<center>

<strong><big> 𒍻 jccsvq 𒁾𒊬  𒐞𒐞𒐞 𒐗 𒐏 𒐋 </big></strong>

</center>

---

## Appendices


(catalog-of-metrological-expressions)=
### Appendix B: Catalog of metrological expressions

#### class: Blen  

    (1 u 7 dis) danna (9 dis) 1/2 UŠ (5 dis) 5/6 ninda (1 dis) 1/3 kuš3 (4 dis) šu-si
    (1 u 7 dis) danna (9 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi
    17 danna 9 us 35 ninda 11 kus 14 susi
    17 1/6 danna 4 1/2 UŠ 5 5/6 ninda 1 1/3 kuš3 4 šu-si
    17 danna 9 1/2 UŠ 5 5/6 ninda 1 1/3 kuš3 4 šu-si
    17 danna 9 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi
    (1 u 7 dis) 1/6 danna (4 dis) 1/2 UŠ (5 dis) 5/6 ninda (1 dis) 1/3 kuš3 (4 dis) šu-si
    (1 u 7 dis) danna (9 dis) us (3 u 5 dis) ninda (1 u 1 dis) kus (1 u 4 dis) susi
    (1 u 7 dis) 1/6 danna (4 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi
    17 1/6 danna 4 1/2 us 5 5/6 ninda 1 1/3 kus 4 susi

#### class: Bsur  

    (1 ese 4 iku) GAN2 (3 u 9 dis) sar (1 u 1 dis) 5/6 gin2 (1 u 4 dis) še
    (1 ese 4 iku) gan (3 u 9 dis) sar (1 u 1 dis) gin (9 bur 2 iku) se
    10 gan 39 sar 11 gin 164 se
    10 GAN2 39 sar 11 5/6 gin2 14 še
    10 gan 39 1/6 sar 1 5/6 gin 14 se
    (1 ese 4 iku) gan (3 u 9 dis) 1/6 sar (1 dis) 5/6 gin (1 u 4 dis) se
    (1 ese 4 iku) gan (3 u 9 dis) sar (1 u 1 dis) 5/6 gin (1 u 4 dis) se
    10 gan 39 sar 11 5/6 gin 14 se
    (1 ese 4 iku) GAN2 (3 u 9 dis) 1/6 sar (1 dis) 5/6 gin2 (1 u 4 dis) še
    10 GAN2 39 1/6 sar 1 5/6 gin2 14 še

#### class: Bvol  

    (1 ese 4 iku) GAN2 (3 u 9 dis) sar (1 u 1 dis) 5/6 gin2 (1 u 4 dis) še
    (1 ese 4 iku) gan (3 u 9 dis) sar (1 u 1 dis) gin (9 bur 2 iku) se
    10 gan 39 sar 11 gin 164 se
    10 GAN2 39 sar 11 5/6 gin2 14 še
    10 gan 39 1/6 sar 1 5/6 gin 14 se
    (1 ese 4 iku) gan (3 u 9 dis) 1/6 sar (1 dis) 5/6 gin (1 u 4 dis) se
    (1 ese 4 iku) gan (3 u 9 dis) sar (1 u 1 dis) 5/6 gin (1 u 4 dis) se
    10 gan 39 sar 11 5/6 gin 14 se
    (1 ese 4 iku) GAN2 (3 u 9 dis) 1/6 sar (1 dis) 5/6 gin2 (1 u 4 dis) še
    10 GAN2 39 1/6 sar 1 5/6 gin2 14 še

#### class: Bcap  

    (3 as) gur (2 as) 1/6 bariga 1/2 ban (4 dis) 1/6 sila (1 dis) 5/6 gin (1 u 4 dis) se
    (3 as) gur (2 as) bariga (1 dis) ban (9 dis) sila (1 u 1 dis) gin (2 ges 4 u 4 as) se
    3 gur 2 1/6 bariga 1/2 ban2 4 1/6 sila3 1 5/6 gin2 14 še
    (3 as) gur (2 as) bariga (1 dis) 1/2 ban2 (4 dis) sila3 (1 u 1 dis) 5/6 gin2 (1 u 4 dis) še
    (3 as) gur (2 as) bariga (1 dis) 1/2 ban (4 dis) sila (1 u 1 dis) 5/6 gin (1 u 4 dis) se
    3 gur 2 bariga 1 ban 9 sila 11 gin 164 se
    3 gur 2 1/6 bariga 1/2 ban 4 1/6 sila 1 5/6 gin 14 se
    3 gur 2 bariga 1 1/2 ban2 4 sila3 11 5/6 gin2 14 še
    (3 as) gur (2 as) 1/6 bariga 1/2 ban2 (4 dis) 1/6 sila3 (1 dis) 5/6 gin2 (1 u 4 dis) še
    3 gur 2 bariga 1 1/2 ban 4 sila 11 5/6 gin 14 se

#### class: Bwei  

    (1 u 7 as) gu (1 u 9 dis) mana (1 u 1 dis) gin (2 ges 4 u 4 as) se
    17 1/6 gu 9 1/6 mana 1 5/6 gin 14 se
    (1 u 7 as) 1/6 gu (9 dis) 1/6 mana (1 dis) 5/6 gin (1 u 4 dis) se
    17 gu 19 mana 11 gin 164 se
    (1 u 7 as) gu (1 u 9 dis) mana (1 u 1 dis) 5/6 gin (1 u 4 dis) se
    (1 u 7 as) gu2 (1 u 9 dis) ma-na (1 u 1 dis) 5/6 gin2 (1 u 4 dis) še
    17 gu2 19 ma-na 11 5/6 gin2 14 še
    17 gu 19 mana 11 5/6 gin 14 se
    (1 u 7 as) 1/6 gu2 (9 dis) 1/6 ma-na (1 dis) 5/6 gin2 (1 u 4 dis) še
    17 1/6 gu2 9 1/6 ma-na 1 5/6 gin2 14 še

#### class: Bbri  

    (1 ese 4 iku) GAN2 (3 u 9 dis) sar (1 u 1 dis) 5/6 gin2 (1 u 4 dis) še
    (1 ese 4 iku) gan (3 u 9 dis) sar (1 u 1 dis) gin (9 bur 2 iku) se
    10 gan 39 sar 11 gin 164 se
    10 GAN2 39 sar 11 5/6 gin2 14 še
    10 gan 39 1/6 sar 1 5/6 gin 14 se
    (1 ese 4 iku) gan (3 u 9 dis) 1/6 sar (1 dis) 5/6 gin (1 u 4 dis) se
    (1 ese 4 iku) gan (3 u 9 dis) sar (1 u 1 dis) 5/6 gin (1 u 4 dis) se
    10 gan 39 sar 11 5/6 gin 14 se
    (1 ese 4 iku) GAN2 (3 u 9 dis) 1/6 sar (1 dis) 5/6 gin2 (1 u 4 dis) še
    10 GAN2 39 1/6 sar 1 5/6 gin2 14 še

#### class: BsyS  

    51 5/6 šar2-gal 1/2 šaru 2 1/2 šar2 1/2 gešu 2/3 geš 4 aš
    51 sargal 5 saru 7 sar 3 gesu 5 ges 4 u 4 as
    (5 u 1 dis) 5/6 šar2-gal 1/2 šaru (2 dis) 1/2 šar2 1/2 gešu 2/3 geš (4 dis) aš
    51 5/6 sargal 1/2 saru 2 1/2 sar 1/2 gesu 2/3 ges 4 as

#### class: BsyG  

    (17 u 3 dis) šar2-gal (1 dis) šaru (1 dis) 5/6 šar2 1/2 buru (4 dis) bur3 1/3 eše3
    173 šar2-gal 1 šaru 1 5/6 šar2 1/2 buru 4 bur3 1/3 eše3
    173 1/6 sargal 1 5/6 sar 1/2 buru 4 bur 1/3 ese
    (17 u 3 dis) 1/6 šar2-gal (1 dis) 5/6 šar2 1/2 buru (4 dis) bur3 1/3 eše3
    (17 u 3 dis) sargal (1 dis) saru (1 dis) 5/6 sar 1/2 buru (4 dis) bur 1/3 ese
    2:53 sargal 1 saru 1 sar 5 buru 9 bur 2 iku
    (17 u 3 dis) 1/6 sargal (1 dis) 5/6 sar 1/2 buru (4 dis) bur 1/3 ese
    173 sargal 1 saru 1 sar 5 buru 9 bur 2 iku
    173 1/6 šar2-gal 1 5/6 šar2 1/2 buru 4 bur3 1/3 eše3
    173 sargal 1 saru 1 5/6 sar 1/2 buru 4 bur 1/3 ese

(commodities-list)=
### Appendix C: List of Commodities

|Category|Commodity|Glyphs|Comment|
|---|---|---|---|
| Metals & Value|ku_babbar|𒆬𒌓| Silver (kù-babbar)|
||urudu|𒍏| Copper (urudu)|
||ku3_sig17|𒆬𒄀| Gold (kù-sig17)|
||    |||
| Crops & Liquids|se|𒊺| Barley (še)|
||ziz2|𒀾| Emmer wheat (zíz)|
||i3_gis|𒉌𒄑| Sesame oil (ì-giš)|
||kas|𒁉| Beer (kaš / bi) - Standard vessel sign|
||    |||
| Land & Livestock|a_sa|𒀀𒊮| Field (a-šà)|
||kiri6|𒊬| Orchard/Garden (kiri6)|
||gu4|𒄞| Ox (gu4)|
||udu|𒇻| Sheep (udu)|
||    |||
| Textiles & Fibers|siki|𒋠| Wool (siki)|
||gada|𒃰| Linen (gada)|
||siki_gi|𒋠𒄀| Native/Standard wool (siki-gi)|
||    |||
| Fruits & Provisions|zu2_lum|𒍪𒈝| Dates (zú-lum)|
||ges_tin|𒃾| Wine (geštin)|
||ga_ar3|𒂵𒄯| Cheese/Curd (ga-àr)|
||i3_nun|𒉌𒉣| Ghee/Butter (ì-nun)|
||    |||
| Building & Resources|esir|𒀀𒂍| Bitumen (esir2 / A.E2) - The most standard form|
||ges|𒄑| Wood/Beam (geš)|
||sig4|𒋞| Brick (sig4)|
||na4|𒉌| Stone (na4)|
||    |||
| Personnel (Contextual)|lu2|𒇽| Man/Worker (lú)|
||geme2|𒊩| Female worker (gemé)|
||er3|𒀴| Slave/Servant (er3)|
||    |||
| Mathematical States|igi_nu|𒅆𒉡| Reciprocal not found (igi-nu)|
||igi_nu_du8|𒅆𒉡𒂃| Reciprocal does not open (igi-nu-du8)|


### Appendix D: Custom Style Sheet (CSS)


```css
/* 1. FONT LOADING
   Import Noto Sans Cuneiform from Google Fonts for cross-platform glyph support.
*/
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Cuneiform&display=swap');

/* 2. GLOBAL TYPOGRAPHY 
   Ensures Cuneiform support is available globally across headers and body text.
*/
body, h1, h2, h3, p {
    font-family: 'Helvetica', 'Arial', 'Noto Sans Cuneiform', sans-serif !important;
}

/* 3. CODE & TERMINAL RENDERING
   Optimizes how cuneiform signs behave inside code blocks and REPL outputs.
*/
/* 1. We clean the margin of the first line in the main container */
.highlight pre {
    text-indent: 0 !important;
    padding-left: 10px !important;
    display: block !important;
}

/* 2. CRITICAL RULE: We only apply inline-block if there is cuneiform content. 
    For the rest of the text (like "-->"), we use 'inline' so that there are no 
    phantom shifts. */
code span,
pre span {
    display: inline !important; /* Volvemos al estándar por defecto */
    min-width: auto !important;
}



/* 4. THE CLAY TABLET CONTAINER 
   Visual simulation of a physical Mesopotamian artifact.
*/
div.tablet {
    /* Fine-grain clay texture using radial and linear gradients */
    background-color: #e2c08d !important;
    background-image:
        repeating-radial-gradient(circle at 0 0, rgba(0, 0, 0, 0.02) 0px, rgba(0, 0, 0, 0.02) 1px, transparent 1px, transparent 10px),
        linear-gradient(135deg, #ebcd9f 0%, #d4ae7b 100%) !important;
    
    border: 1px solid #c59d6a !important;
    border-radius: 16px !important;
    padding: 25px !important;
    margin: 20px 0;
    
    box-shadow: 6px 6px 18px rgba(0, 0, 0, 0.3) !important;
    display: inline-block;
    
    /* Physical object "tilt" for realism */
    transform: rotate(-0.5deg);
}

/* Tablet Caption styling - Forced for both Light/Dark modes */
div.tablet caption {
    font-family: 'Helvetica', 'Arial', sans-serif !important;
    font-weight: bold !important;
    font-variant: small-caps !important;
    color: #5d4037 !important; /* Fixed dark brown, even in Dark Mode */
    margin-bottom: 10px !important;
    caption-side: top !important;
    text-align: left !important;
    background: transparent !important; /* Avoids theme background blocks */
}

/* 5. TABLET CONTENT & INCISED EFFECT
   Overrides standard theme styles to create the "incised" look on clay.
*/
div.tablet table,
div.tablet tr,
div.tablet th,
div.tablet td {
    background: transparent !important;
    border: none !important;
    color: #55361b !important; /* Dark brown "incised" color */
    font-family: 'Noto Sans Cuneiform', serif !important;
    font-size: 120% !important;
    font-weight: 900 !important;
    line-height: 0.85 !important; /* Optimized for glyph density */
    text-align: left;
}

/* Sculptural depth effect using dual-tone shadows (light/dark) */
div.tablet td,
div.tablet th {
    padding: 10px 15px !important;
    text-shadow: 1px 1px 0px rgba(255, 255, 255, 0.3),
                -1px -1px 0px rgba(0, 0, 0, 0.2) !important;
}

/* Subtle header underline representing a scribal ruling */
div.tablet th {
    border-bottom: 2px solid rgba(62, 39, 19, 0.3) !important;
    text-transform: uppercase;
    font-size: 0.8em !important;
    letter-spacing: 1px;
}

/* 6. COMPATIBILITY & OVERRIDES
   Cleans up theme-specific artifacts from Sphinx or ReadTheDocs.
*/
div.tablet .pst-scrollable-table-container {
    background-color: transparent !important;
    border: none !important;
}

div.tablet table {
    margin: 10px auto !important;
    border-collapse: separate !important;
    border-spacing: 0 5px !important;
}

/* Compact version for smaller side-tables */
.tablet.mini table,
.tablet.mini td,
.tablet.mini th {
    font-size: 90% !important;
}

```



### Test Details

<details>
<summary>📋 Capacities (Proust §8.1)</summary>

| §8.1 Capacities (še) | MesoMath | MesoMath (Cun.) |
|---|---|---|
| 1(diš) gin2 še | (1 diš) gin2 se | 𒀸 𒂆 𒊺 |
|  | (1 diš) gin2 (3 u) še | 𒀸 𒂆 𒌍 𒊺 |
| 1(diš) 1/3 gin2 | (1 diš) 1/3 gin2 | 𒀸 𒑚 𒂆 |
| 1(diš) 1/2 gin2 | (1 diš) 1/2 gin2 | 𒀸 𒈦 𒂆 |
| 1(diš) 2/3 gin2 | (1 diš) 2/3 gin2 | 𒀸 𒑛 𒂆 |
| 1(diš) 5/6 gin2 | (1 diš) 5/6 gin2 | 𒀸 𒑜 𒂆 |
| 2(diš) gin2 | (2 diš) gin2 | 𒐀 𒂆 |
|  | (2 diš) gin2 (3 u) še | 𒐀 𒂆 𒌍 𒊺 |
| 2(diš) 1/3 gin2 | (2 diš) 1/3 gin2 | 𒐀 𒑚 𒂆 |
| 2(diš) 1/2 gin2 | (2 diš) 1/2 gin2 | 𒐀 𒈦 𒂆 |
| 2(diš) 2/3 gin2 | (2 diš) 2/3 gin2 | 𒐀 𒑛 𒂆 |
| 2(diš) 5/6 gin2 | (2 diš) 5/6 gin2 | 𒐀 𒑜 𒂆 |
| 3(diš) gin2 | (3 diš) gin2 | 𒐁 𒂆 |
| 4(diš) gin2 | (4 diš) gin2 se | 𒐂 𒂆 𒊺 |
| 5(diš) gin2 | (5 diš) gin2 | 𒐃 𒂆 |
| 6(diš) gin2 | (6 diš) gin2 | 𒐄 𒂆 |
| 7(diš) gin2 | (7 diš) gin2 | 𒐅 𒂆 |
| 8(diš) gin2 | (8 diš) gin2 | 𒐆 𒂆 |
| 9(diš) gin2 | (9 diš) gin2 | 𒐇 𒂆 |
| 1(u) gin2 | (1 u) gin2 | 𒌋 𒂆 |
| 1(u) 1(diš) gin2 | (1 u 1 diš) gin2 | 𒌋 𒀸 𒂆 |
| 1(u) 2(diš) gin2 | (1 u 2 diš) gin2 | 𒌋 𒐀 𒂆 |
| 1(u) 3(diš) gin2 | (1 u 3 diš) gin2 | 𒌋 𒐁 𒂆 |
| 1(u) 4(diš) gin2 | (1 u 4 diš) gin2 | 𒌋 𒐂 𒂆 |
| 1(u) 5(diš) gin2 | (1 u 5 diš) gin2 | 𒌋 𒐃 𒂆 |
| 1(u) 6(diš) gin2 | (1 u 6 diš) gin2 | 𒌋 𒐄 𒂆 |
| 1(u) 7(diš) gin2 | (1 u 7 diš) gin2 | 𒌋 𒐅 𒂆 |
| 1(u) 8(diš) gin2 | (1 u 8 diš) gin2 | 𒌋 𒐆 𒂆 |
| 1(u) 9(diš) gin2 | (1 u 9 diš) gin2 | 𒌋 𒐇 𒂆 |
| 1/3 sila3 | 1/3 sila3 | 𒑚 𒋡 |
| 1/2 sila3 | 1/2 sila3 se | 𒈦 𒋡 𒊺 |
| 2/3 sila3 | 2/3 sila3 | 𒑛 𒋡 |
| 5/6 sila3 | 5/6 sila3 | 𒑜 𒋡 |
| 1(diš) sila3 | (1 diš) sila3 | 𒀸 𒋡 |
|  | (1 diš) sila3 (1 u) gin2 | 𒀸 𒋡 𒌋 𒂆 |
| 1(diš) 1/3 sila3 | (1 diš) 1/3 sila3 | 𒀸 𒑚 𒋡 |
| 1(diš) 1/2 sila3 | (1 diš) 1/2 sila3 | 𒀸 𒈦 𒋡 |
| 1(diš) 2/3 sila3 | (1 diš) 2/3 sila3 | 𒀸 𒑛 𒋡 |
| 1(diš) 5/6 sila3 | (1 diš) 5/6 sila3 | 𒀸 𒑜 𒋡 |
| 2(diš) sila3 | (2 diš) sila3 | 𒐀 𒋡 |
| 3(diš) sila3 | (3 diš) sila3 se | 𒐁 𒋡 𒊺 |
| 4(diš) sila3 | (4 diš) sila3 | 𒐂 𒋡 |
| 5(diš) sila3 | 1/2 ban2 | 𒈦 𒑏 |
| 6(diš) sila3 | 1/2 ban2 (1 diš) sila3 | 𒈦 𒑏 𒀸 𒋡 |
| 7(diš) sila3 | 1/2 ban2 (2 diš) sila3 | 𒈦 𒑏 𒐀 𒋡 |
| 8(diš) sila3 | 1/2 ban2 (3 diš) sila3 | 𒈦 𒑏 𒐁 𒋡 |
| 9(diš) sila3 | 1/2 ban2 (4 diš) sila3 | 𒈦 𒑏 𒐂 𒋡 |
| 1(ban2) še | (1 diš) ban2 | 𒀸 𒑏 |
| 1(ban2) 1(diš) sila3 | (1 diš) ban2 (1 diš) sila3 | 𒀸 𒑏 𒀸 𒋡 |
| 1(ban2) 2(diš) sila3 | (1 diš) ban2 (2 diš) sila3 | 𒀸 𒑏 𒐀 𒋡 |
| 1(ban2) 3(diš) sila3 | (1 diš) ban2 (3 diš) sila3 | 𒀸 𒑏 𒐁 𒋡 |
| 1(ban2) 4(diš) sila3 | (1 diš) ban2 (4 diš) sila3 | 𒀸 𒑏 𒐂 𒋡 |
| 1(ban2) 5(diš) sila3 | (1 diš) 1/2 ban2 | 𒀸 𒈦 𒑏 |
| 1(ban2) 6(diš) sila3 | (1 diš) 1/2 ban2 (1 diš) sila3 | 𒀸 𒈦 𒑏 𒀸 𒋡 |
| 1(ban2) 7(diš) sila3 | (1 diš) 1/2 ban2 (2 diš) sila3 | 𒀸 𒈦 𒑏 𒐀 𒋡 |
| 1(ban2) 8(diš) sila3 | (1 diš) 1/2 ban2 (3 diš) sila3 | 𒀸 𒈦 𒑏 𒐁 𒋡 |
| 1(ban2) 9(diš) sila3 | (1 diš) 1/2 ban2 (4 diš) sila3 | 𒀸 𒈦 𒑏 𒐂 𒋡 |
| 2(ban2) še | 1/3 bariga | 𒑚 𒉿 |
| 2(ban2) 5(diš) sila3 | 1/3 bariga 1/2 ban2 se | 𒑚 𒉿 𒈦 𒑏 𒊺 |
| 3(ban2) še | 1/2 bariga | 𒈦 𒉿 |
| 3(ban2) 5(diš) sila3 | 1/2 bariga 1/2 ban2 | 𒈦 𒉿 𒈦 𒑏 |
| 4(ban2) še | 2/3 bariga | 𒑛 𒉿 |
| 4(ban2) 5(diš) sila3 | 2/3 bariga 1/2 ban2 | 𒑛 𒉿 𒈦 𒑏 |
| 5(ban2) še | 5/6 bariga | 𒑜 𒉿 |
| 5(ban2) 5(diš) sila3 | 5/6 bariga 1/2 ban2 | 𒑜 𒉿 𒈦 𒑏 |
| 1(barig) še | (1 aš) bariga | 𒀸 𒉿 |
| 1(barig) 1(ban2) še | (1 aš) bariga (1 diš) ban2 se | 𒀸 𒉿 𒀸 𒑏 𒊺 |
| 1(barig) 2(ban2) še | (1 aš) 1/3 bariga | 𒀸 𒑚 𒉿 |
| 1(barig) 3(ban2) še | (1 aš) 1/2 bariga | 𒀸 𒈦 𒉿 |
| 1(barig) 4(ban2) še | (1 aš) 2/3 bariga | 𒀸 𒑛 𒉿 |
| 1(barig) 5(ban2) še | (1 aš) 5/6 bariga | 𒀸 𒑜 𒉿 |
| 2(barig) še | (2 aš) bariga | 𒐀 𒉿 |
| 2(barig) 1(ban2) še | (2 aš) bariga (1 diš) ban2 | 𒐀 𒉿 𒀸 𒑏 |
| 2(barig) 2(ban2) še | (2 aš) 1/3 bariga | 𒐀 𒑚 𒉿 |
| 2(barig) 3(ban2) še | (2 aš) 1/2 bariga | 𒐀 𒈦 𒉿 |
| 2(barig) 4(ban2) še | (2 aš) 2/3 bariga | 𒐀 𒑛 𒉿 |
| 2(barig) 5(ban2) še | (2 aš) 5/6 bariga | 𒐀 𒑜 𒉿 |
| 3(barig) še | (3 aš) bariga | 𒐁 𒉿 |
| 3(barig) 1(ban2) še | (3 aš) bariga (1 diš) ban2 | 𒐁 𒉿 𒀸 𒑏 |
| 3(barig) 2(ban2) še | (3 aš) 1/3 bariga | 𒐁 𒑚 𒉿 |
| 3(barig) 3(ban2) še | (3 aš) 1/2 bariga | 𒐁 𒈦 𒉿 |
| 3(barig) 4(ban2) še | (3 aš) 2/3 bariga | 𒐁 𒑛 𒉿 |
| 3(barig) 5(ban2) še | (3 aš) 5/6 bariga | 𒐁 𒑜 𒉿 |
| 4(barig) še | (4 aš) bariga | 𒐂 𒉿 |
| 4(barig) 1(ban2) še | (4 aš) bariga (1 diš) ban2 | 𒐂 𒉿 𒀸 𒑏 |
| 4(barig) 2(ban2) še | (4 aš) 1/3 bariga | 𒐂 𒑚 𒉿 |
| 4(barig) 3(ban2) še | (4 aš) 1/2 bariga | 𒐂 𒈦 𒉿 |
| 4(barig) 4(ban2) še | (4 aš) 2/3 bariga | 𒐂 𒑛 𒉿 |
| 4(barig) 5(ban2) še | (4 aš) 5/6 bariga | 𒐂 𒑜 𒉿 |
| 1(aš) gur | (1 aš) gur | 𒀸 𒄥 |
| 1(aš) 1(barig) gur | (1 aš) gur (1 aš) bariga se | 𒀸 𒄥 𒀸 𒉿 𒊺 |
| 1(aš) 2(barig) gur | (1 aš) gur (2 aš) bariga | 𒀸 𒄥 𒐀 𒉿 |
| 1(aš) 3(barig) gur | (1 aš) gur (3 aš) bariga | 𒀸 𒄥 𒐁 𒉿 |
| 1(aš) 4(barig) gur | (1 aš) gur (4 aš) bariga | 𒀸 𒄥 𒐂 𒉿 |
| 2(aš) gur | (2 aš) gur | 𒐀 𒄥 |
| 3(aš) gur | (3 aš) gur se | 𒐁 𒄥 𒊺 |
| 4(aš) gur | (4 aš) gur | 𒐂 𒄥 |
| 5(aš) gur | (5 aš) gur | 𒐃 𒄥 |
| 6(aš) gur | (6 aš) gur | 𒐄 𒄥 |
| 7(diš) gur | (7 aš) gur | 𒐅 𒄥 |
| 8(aš) gur | (8 aš) gur | 𒐆 𒄥 |
| 9(aš) gur | (9 aš) gur | 𒐇 𒄥 |
| 1(u) gur | (1 u) gur | 𒌋 𒄥 |
| 1(u) 1(aš) gur | (1 u 1 aš) gur | 𒌋 𒀸 𒄥 |
| 1(u) 2(aš) gur | (1 u 2 aš) gur | 𒌋 𒐀 𒄥 |
| 1(u) 3(aš) gur | (1 u 3 aš) gur | 𒌋 𒐁 𒄥 |
| 1(u) 4(aš) gur | (1 u 4 aš) gur | 𒌋 𒐂 𒄥 |
| 1(u) 5(aš) gur | (1 u 5 aš) gur | 𒌋 𒐃 𒄥 |
| 1(u) 6(aš) gur | (1 u 6 aš) gur | 𒌋 𒐄 𒄥 |
| 1(u) 7(diš) gur | (1 u 7 aš) gur | 𒌋 𒐅 𒄥 |
| 1(u) 8(aš) gur | (1 u 8 aš) gur | 𒌋 𒐆 𒄥 |
| 1(u) 9(aš) gur | (1 u 9 aš) gur | 𒌋 𒐇 𒄥 |
| 2(u) gur | (2 u) gur | 𒎙 𒄥 |
| 3(u) gur | (3 u) gur se | 𒌍 𒄥 𒊺 |
| 4(u) gur | (4 u) gur | 𒐏 𒄥 |
| 5(u) gur | (5 u) gur | 𒐐 𒄥 |
| 1(geš2) gur | (1 geš) gur | 𒐕 𒄥 |
| 1(geš2) 1(u) gur | (1 geš 1 u) gur | 𒐕 𒌋 𒄥 |
| 1(geš2) 2(u) gur | (1 geš 2 u) gur | 𒐕 𒎙 𒄥 |
| 1(geš2) 3(u) gur | (1 geš 3 u) gur | 𒐕 𒌍 𒄥 |
| 1(geš2) 4(u) gur | (1 geš 4 u) gur | 𒐕 𒐏 𒄥 |
| 1(geš2) 5(u) gur | (1 geš 5 u) gur | 𒐕 𒐐 𒄥 |
| 2(geš2) gur | (2 geš) gur | 𒐖 𒄥 |
| 3(geš2) gur | (3 geš) gur se | 𒐗 𒄥 𒊺 |
| 4(geš2) gur | (4 geš) gur | 𒐘 𒄥 |
| 5(geš2) gur | (5 geš) gur | 𒐙 𒄥 |
| 6(geš2) gur | (6 geš) gur | 𒐚 𒄥 |
| 7(geš2) gur | (7 geš) gur | 𒐛 𒄥 |
| 8(geš2) gur | (8 geš) gur | 𒐜 𒄥 |
| 9(geš2) gur | (9 geš) gur | 𒐝 𒄥 |
| 1(geš’u) gur | (1 geš'u) gur | 𒐞 𒄥 |
| 1(geš’u) 1(geš2) gur | (1 geš'u 1 geš) gur | 𒐞 𒐕 𒄥 |
| 1(geš’u) 2(geš2) gur | (1 geš'u 2 geš) gur | 𒐞 𒐖 𒄥 |
| 1(geš’u) 3(geš2) gur | (1 geš'u 3 geš) gur | 𒐞 𒐗 𒄥 |
| 1(geš’u) 4(geš2) gur | (1 geš'u 4 geš) gur | 𒐞 𒐘 𒄥 |
| 1(geš’u) 5(geš2) gur | (1 geš'u 5 geš) gur | 𒐞 𒐙 𒄥 |
| 1(geš’u) 6(geš2) gur | (1 geš'u 6 geš) gur | 𒐞 𒐚 𒄥 |
| 1(geš’u) 7(geš2) gur | (1 geš'u 7 geš) gur | 𒐞 𒐛 𒄥 |
| 1(geš’u) 8(geš2) gur | (1 geš'u 8 geš) gur | 𒐞 𒐜 𒄥 |
| 1(geš’u) 9(geš2) gur | (1 geš'u 9 geš) gur | 𒐞 𒐝 𒄥 |
| 2(geš’u) gur | (2 geš'u) gur | 𒐟 𒄥 |
| 3(geš’u) gur | (3 geš'u) gur se | 𒐠 𒄥 𒊺 |
| 4(geš’u) gur | (4 geš'u) gur | 𒐡 𒄥 |
| 5(geš’u) gur | (5 geš'u) gur | 𒐢 𒄥 |
| 1(šar2) gur | (1 šar2) gur | 𒊹 𒄥 |
| 1(šar2) 1(geš’u) gur | (1 šar2 1 geš'u) gur | 𒊹 𒐞 𒄥 |
| 1(šar2) 2(geš’u) gur | (1 šar2 2 geš'u) gur | 𒊹 𒐟 𒄥 |
| 1(šar2) 3(geš’u) gur | (1 šar2 3 geš'u) gur | 𒊹 𒐠 𒄥 |
| 1(šar2) 4(geš’u) gur | (1 šar2 4 geš'u) gur | 𒊹 𒐡 𒄥 |
| 1(šar2) 5(geš’u) gur | (1 šar2 5 geš'u) gur | 𒊹 𒐢 𒄥 |
| 2(šar2) gur | (2 šar2) gur | 𒐣 𒄥 |
| 3(šar2) gur | (3 šar2) gur se | 𒐤 𒄥 𒊺 |
| 4(šar2) gur | (4 šar2) gur | 𒐦 𒄥 |
| 5(šar2) gur | (5 šar2) gur | 𒐧 𒄥 |
| 6(šar2) gur | (6 šar2) gur | 𒐨 𒄥 |
| 7(šar2) gur | (7 šar2) gur | 𒐩 𒄥 |
| 8(šar2) gur | (8 šar2) gur | 𒐪 𒄥 |
| 9(šar2) gur | (9 šar2) gur | 𒐫 𒄥 |
| 1(šar’u) gur | (1 šar'u) gur | 𒐬 𒄥 |
| 1(šar’u) 1(šar2) gur | (1 šar'u 1 šar2) gur | 𒐬 𒊹 𒄥 |
| 1(šar’u) 2(šar2) gur | (1 šar'u 2 šar2) gur | 𒐬 𒐣 𒄥 |
| 1(šar’u) 3(šar2) gur | (1 šar'u 3 šar2) gur | 𒐬 𒐤 𒄥 |
| 1(šar’u) 4(šar2) gur | (1 šar'u 4 šar2) gur | 𒐬 𒐦 𒄥 |
| 1(šar’u) 5(šar2) gur | (1 šar'u 5 šar2) gur | 𒐬 𒐧 𒄥 |
| 1(šar’u) 6(šar2) gur | (1 šar'u 6 šar2) gur | 𒐬 𒐨 𒄥 |
| 1(šar’u) 7(šar2) gur | (1 šar'u 7 šar2) gur | 𒐬 𒐩 𒄥 |
| 1(šar’u) 8(šar2) gur | (1 šar'u 8 šar2) gur | 𒐬 𒐪 𒄥 |
| 1(šar’u) 9(šar2) gur | (1 šar'u 9 šar2) gur | 𒐬 𒐫 𒄥 |
| 2(šar’u) gur | (2 šar'u) gur | 𒐭 𒄥 |
| 3(šar’u) gur | (3 šar'u) gur se | 𒐮 𒄥 𒊺 |
| 4(šar’u) gur | (4 šar'u) gur | 𒐰 𒄥 |
| 5(šar’u) gur | (5 šar'u) gur | 𒐱 𒄥 |
| 1(šargal)gal gur | (1 šar2-gal) gur | 𒐲 𒄥 |
| 1(šargal)gal šu-nu-tag gur |  |  |


</details>

<details>

<summary>📋 Weights (Proust §8.1)</summary>

| §8.2. Weights (ku3-babbar) | MesoMath | cd |
|---|---|---|
| 1/2 še ku3-babbar |  |  |
| 1(diš) še | (1 diš) še ku_babbar | 𒀸 𒊺 𒆬 𒌓 |
| 1(diš) 1/2 še |  |  |
| 2(diš) še | (2 diš) še | 𒐀 𒊺 |
| 2(diš) 1/2 še |  |  |
| 3(diš) še | (3 diš) še | 𒐁 𒊺 |
| 4(diš) še | (4 diš) še | 𒐂 𒊺 |
| 5(diš) še | (5 diš) še | 𒐃 𒊺 |
| 6(diš) še | (6 diš) še | 𒐄 𒊺 |
| 7(diš) še | (7 diš) še | 𒐅 𒊺 |
| 8(diš) še | (8 diš) še | 𒐆 𒊺 |
| 9(diš) še | (9 diš) še | 𒐇 𒊺 |
| 1(u) še | (1 u) še | 𒌋 𒊺 |
| 1(u) 1(diš) še | (1 u 1 diš) še | 𒌋 𒀸 𒊺 |
| 1(u) 2(diš) še | (1 u 2 diš) še | 𒌋 𒐀 𒊺 |
| 1(u) 3(diš) še | (1 u 3 diš) še | 𒌋 𒐁 𒊺 |
| 1(u) 4(diš) še | (1 u 4 diš) še | 𒌋 𒐂 𒊺 |
| 1(u) 5(diš) še | (1 u 5 diš) še | 𒌋 𒐃 𒊺 |
| 1(u) 6(diš) še | (1 u 6 diš) še | 𒌋 𒐄 𒊺 |
| 1(u) 7(diš) še | (1 u 7 diš) še | 𒌋 𒐅 𒊺 |
| 1(u) 8(diš) še | (1 u 8 diš) še | 𒌋 𒐆 𒊺 |
| 1(u) 9(diš) še | (1 u 9 diš) še | 𒌋 𒐇 𒊺 |
| 2(u) še | (2 u) še | 𒎙 𒊺 |
| 2(u) 1(diš) še | (2 u 1 diš) še | 𒎙 𒀸 𒊺 |
| 2(u) 2(diš) še | (2 u 2 diš) še | 𒎙 𒐀 𒊺 |
| 2(u) 3(diš) še | (2 u 3 diš) še | 𒎙 𒐁 𒊺 |
| 2(u) 4(diš) še | (2 u 4 diš) še | 𒎙 𒐂 𒊺 |
| 2(u) 5(diš) še | (2 u 5 diš) še | 𒎙 𒐃 𒊺 |
| 2(u) 6(diš) še | (2 u 6 diš) še | 𒎙 𒐄 𒊺 |
| 2(u) 7(diš) še | (2 u 7 diš) še | 𒎙 𒐅 𒊺 |
| 2(u) 8(diš) še | (2 u 8 diš) še | 𒎙 𒐆 𒊺 |
| 2(u) 9(diš) še | (2 u 9 diš) še | 𒎙 𒐇 𒊺 |
| igi 6(diš)-gal2 gin2 | 1/6 gin2 | 𒑡 𒂆 |
| igi 6(diš)-gal2 gin2 1(u) še | 1/6 gin2 (1 u) še ku_babbar | 𒑡 𒂆 𒌋 𒊺 𒆬 𒌓 |
| igi 4(diš)-gal2 gin2 | 1/6 gin2 (1 u 5 diš) še ku_babbar | 𒑡 𒂆 𒌋 𒐃 𒊺 𒆬 𒌓 |
| igi 4(diš)-gal2 gin2 5(diš) še | 1/6 gin2 (2 u) še ku_babbar | 𒑡 𒂆 𒎙 𒊺 𒆬 𒌓 |
| 1/3 gin2 | 1/3 gin2 ku_babbar | 𒑚 𒂆 𒆬 𒌓 |
| 1/2 gin2 | 1/2 gin2 ku_babbar | 𒈦 𒂆 𒆬 𒌓 |
| 1/2 gin2 1(u) še | 1/2 gin2 (1 u) še ku_babbar | 𒈦 𒂆 𒌋 𒊺 𒆬 𒌓 |
| 1/2 gin2 1(u) 5(diš) še | 1/2 gin2 (1 u 5 diš) še ku_babbar | 𒈦 𒂆 𒌋 𒐃 𒊺 𒆬 𒌓 |
|  | 1/2 gin2 (2 u) še ku_babbar | 𒈦 𒂆 𒎙 𒊺 𒆬 𒌓 |
| 1/2 gin2 2(u) 5(diš) še | 1/2 gin2 (2 u 5 diš) še | 𒈦 𒂆 𒎙 𒐃 𒊺 |
| 2/3 gin2 | 2/3 gin2 ku_babbar | 𒑛 𒂆 𒆬 𒌓 |
| 2/3 gin2 1(u) še | 2/3 gin2 (1 u) še ku_babbar | 𒑛 𒂆 𒌋 𒊺 𒆬 𒌓 |
| 2/3 gin2 1(u) 5(diš) še | 2/3 gin2 (1 u 5 diš) še ku_babbar | 𒑛 𒂆 𒌋 𒐃 𒊺 𒆬 𒌓 |
|  | 2/3 gin2 (2 u) še ku_babbar | 𒑛 𒂆 𒎙 𒊺 𒆬 𒌓 |
| 2/3 gin2 2(u) 5(diš) še | 2/3 gin2 (2 u 5 diš) še | 𒑛 𒂆 𒎙 𒐃 𒊺 |
| 5/6 gin2 | 5/6 gin2 ku_babbar | 𒑜 𒂆 𒆬 𒌓 |
| 5/6 gin2 1(u) še | 5/6 gin2 (1 u) še ku_babbar | 𒑜 𒂆 𒌋 𒊺 𒆬 𒌓 |
| 5/6 gin2 1(u) 5(diš) še | 5/6 gin2 (1 u 5 diš) še ku_babbar | 𒑜 𒂆 𒌋 𒐃 𒊺 𒆬 𒌓 |
|  | 5/6 gin2 (2 u) še ku_babbar | 𒑜 𒂆 𒎙 𒊺 𒆬 𒌓 |
| 5/6 gin2 2(u) 5(diš) še | 5/6 gin2 (2 u 5 diš) še | 𒑜 𒂆 𒎙 𒐃 𒊺 |
| 1(diš) gin2 | (1 diš) gin2 ku_babbar | 𒀸 𒂆 𒆬 𒌓 |
|  | (1 diš) 1/6 gin2 ku_babbar | 𒀸 𒑡 𒂆 𒆬 𒌓 |
| 1(diš) 1/3 gin2 | (1 diš) 1/3 gin2 | 𒀸 𒑚 𒂆 |
| 1(diš) 1/2 gin2 | (1 diš) 1/2 gin2 | 𒀸 𒈦 𒂆 |
| 1(diš) 2/3 gin2 | (1 diš) 2/3 gin2 | 𒀸 𒑛 𒂆 |
| 1(diš) 5/6 gin2 | (1 diš) 5/6 gin2 | 𒀸 𒑜 𒂆 |
| 2(diš) gin2 | (2 diš) gin2 | 𒐀 𒂆 |
| 3(diš) gin2 | (3 diš) gin2 ku_babbar | 𒐁 𒂆 𒆬 𒌓 |
| 4(diš) gin2 | (4 diš) gin2 | 𒐂 𒂆 |
| 5(diš) gin2 | (5 diš) gin2 | 𒐃 𒂆 |
| 6(diš) gin2 | (6 diš) gin2 | 𒐄 𒂆 |
| 7(diš) gin2 | (7 diš) gin2 | 𒐅 𒂆 |
| 8(diš) gin2 | (8 diš) gin2 | 𒐆 𒂆 |
| 9(diš) gin2 | (9 diš) gin2 | 𒐇 𒂆 |
| 1(u) gin2 | 1/6 ma-na | 𒑡 𒈠 𒈾 |
| 1(u) 1(diš) gin2 | 1/6 ma-na (1 diš) gin2 | 𒑡 𒈠 𒈾 𒀸 𒂆 |
| 1(u) 2(diš) gin2 | 1/6 ma-na (2 diš) gin2 | 𒑡 𒈠 𒈾 𒐀 𒂆 |
| 1(u) 3(diš) gin2 | 1/6 ma-na (3 diš) gin2 | 𒑡 𒈠 𒈾 𒐁 𒂆 |
| 1(u) 4(diš) gin2 | 1/6 ma-na (4 diš) gin2 | 𒑡 𒈠 𒈾 𒐂 𒂆 |
| 1(u) 5(diš) gin2 | 1/6 ma-na (5 diš) gin2 | 𒑡 𒈠 𒈾 𒐃 𒂆 |
| 1(u) 6(diš) gin2 | 1/6 ma-na (6 diš) gin2 | 𒑡 𒈠 𒈾 𒐄 𒂆 |
| 1(u) 7(diš) gin2 | 1/6 ma-na (7 diš) gin2 | 𒑡 𒈠 𒈾 𒐅 𒂆 |
| 1(u) 8(diš) gin2 | 1/6 ma-na (8 diš) gin2 | 𒑡 𒈠 𒈾 𒐆 𒂆 |
| 1(u) 9(diš) gin2 | 1/6 ma-na (9 diš) gin2 | 𒑡 𒈠 𒈾 𒐇 𒂆 |
| 1/3 ma-na | 1/3 ma-na | 𒑚 𒈠 𒈾 |
| 1/2 ma-na | 1/2 ma-na ku_babbar | 𒈦 𒈠 𒈾 𒆬 𒌓 |
| 2/3 ma-na | 2/3 ma-na | 𒑛 𒈠 𒈾 |
| 5/6 ma-na | 5/6 ma-na | 𒑜 𒈠 𒈾 |
| 1(diš) ma-na | (1 diš) ma-na | 𒀸 𒈠 𒈾 |
|  | (1 diš) 1/6 ma-na | 𒀸 𒑡 𒈠 𒈾 |
| 1(diš) 1/3 ma-na | (1 diš) 1/3 ma-na | 𒀸 𒑚 𒈠 𒈾 |
| 1(diš) 1/2 ma-na | (1 diš) 1/2 ma-na | 𒀸 𒈦 𒈠 𒈾 |
| 1(diš) 2/3 ma-na | (1 diš) 2/3 ma-na | 𒀸 𒑛 𒈠 𒈾 |
| 1(diš) 5/6 ma-na | (1 diš) 5/6 ma-na | 𒀸 𒑜 𒈠 𒈾 |
| 2(diš) ma-na | (2 diš) ma-na | 𒐀 𒈠 𒈾 |
| 3(diš) ma-na | (3 diš) ma-na ku_babbar | 𒐁 𒈠 𒈾 𒆬 𒌓 |
| 4(diš) ma-na | (4 diš) ma-na | 𒐂 𒈠 𒈾 |
| 5(diš) ma-na | (5 diš) ma-na | 𒐃 𒈠 𒈾 |
| 6(diš) ma-na | (6 diš) ma-na | 𒐄 𒈠 𒈾 |
| 7(diš) ma-na | (7 diš) ma-na | 𒐅 𒈠 𒈾 |
| 8(diš) ma-na | (8 diš) ma-na | 𒐆 𒈠 𒈾 |
| 9(diš) ma-na | (9 diš) ma-na | 𒐇 𒈠 𒈾 |
| 1(u) ma-na | 1/6 gu2 | 𒑡 𒄘 |
| 1(u) 1(diš) ma-na | 1/6 gu2 (1 diš) ma-na | 𒑡 𒄘 𒀸 𒈠 𒈾 |
| 1(u) 2(diš) ma-na | 1/6 gu2 (2 diš) ma-na | 𒑡 𒄘 𒐀 𒈠 𒈾 |
| 1(u) 3(diš) ma-na | 1/6 gu2 (3 diš) ma-na | 𒑡 𒄘 𒐁 𒈠 𒈾 |
| 1(u) 4(diš) ma-na | 1/6 gu2 (4 diš) ma-na | 𒑡 𒄘 𒐂 𒈠 𒈾 |
| 1(u) 5(diš) ma-na | 1/6 gu2 (5 diš) ma-na | 𒑡 𒄘 𒐃 𒈠 𒈾 |
| 1(u) 6(diš) ma-na | 1/6 gu2 (6 diš) ma-na | 𒑡 𒄘 𒐄 𒈠 𒈾 |
| 1(u) 7(diš) ma-na | 1/6 gu2 (7 diš) ma-na | 𒑡 𒄘 𒐅 𒈠 𒈾 |
| 1(u) 8(diš) ma-na | 1/6 gu2 (8 diš) ma-na | 𒑡 𒄘 𒐆 𒈠 𒈾 |
| 1(u) 9(diš) ma-na | 1/6 gu2 (9 diš) ma-na | 𒑡 𒄘 𒐇 𒈠 𒈾 |
| 2(u) ma-na | 1/3 gu2 | 𒑚 𒄘 |
| 2(u) 1(diš) ma-na | 1/3 gu2 (1 diš) ma-na | 𒑚 𒄘 𒀸 𒈠 𒈾 |
| 2(u) 2(diš) ma-na | 1/3 gu2 (2 diš) ma-na | 𒑚 𒄘 𒐀 𒈠 𒈾 |
| 2(u) 3(diš) ma-na | 1/3 gu2 (3 diš) ma-na | 𒑚 𒄘 𒐁 𒈠 𒈾 |
| 2(u) 4(diš) ma-na | 1/3 gu2 (4 diš) ma-na | 𒑚 𒄘 𒐂 𒈠 𒈾 |
| 2(u) 5(diš) ma-na | 1/3 gu2 (5 diš) ma-na | 𒑚 𒄘 𒐃 𒈠 𒈾 |
| 2(u) 6(diš) ma-na | 1/3 gu2 (6 diš) ma-na | 𒑚 𒄘 𒐄 𒈠 𒈾 |
| 2(u) 7(diš) ma-na | 1/3 gu2 (7 diš) ma-na | 𒑚 𒄘 𒐅 𒈠 𒈾 |
| 2(u) 8(diš) ma-na | 1/3 gu2 (8 diš) ma-na | 𒑚 𒄘 𒐆 𒈠 𒈾 |
| 2(u) 9(diš) ma-na | 1/3 gu2 (9 diš) ma-na | 𒑚 𒄘 𒐇 𒈠 𒈾 |
| 3(u) ma-na | 1/2 gu2 | 𒈦 𒄘 |
| 4(u) ma-na | 2/3 gu2 ku_babbar | 𒑛 𒄘 𒆬 𒌓 |
| 5(u) ma-na | 5/6 gu2 | 𒑜 𒄘 |
| 1(aš) gu2 ku3-babbar | (1 aš) gu2 | 𒀸 𒄘 |
| 1(aš) gu2 1(u) ma-na | (1 aš) 1/6 gu2 | 𒀸 𒑡 𒄘 |
| 1(aš) gu2 2(u) ma-na | (1 aš) 1/3 gu2 | 𒀸 𒑚 𒄘 |
| 1(aš) gu2 3(u) ma-na | (1 aš) 1/2 gu2 | 𒀸 𒈦 𒄘 |
| 1(aš) gu2 4(u) ma-na | (1 aš) 2/3 gu2 | 𒀸 𒑛 𒄘 |
| 1(aš) gu2 5(u) ma-na | (1 aš) 5/6 gu2 | 𒀸 𒑜 𒄘 |
| 2(aš) gu2 | (2 aš) gu2 | 𒐀 𒄘 |
| 3(aš) gu2 | (3 aš) gu2 ku_babbar | 𒐁 𒄘 𒆬 𒌓 |
| 4(aš) gu2 | (4 aš) gu2 | 𒐂 𒄘 |
| 5(aš) gu2 | (5 aš) gu2 | 𒐃 𒄘 |
| 6(aš) gu2 | (6 aš) gu2 | 𒐄 𒄘 |
| 7(aš) gu2 | (7 aš) gu2 | 𒐅 𒄘 |
| 8(aš) gu2 | (8 aš) gu2 | 𒐆 𒄘 |
| 9(aš) gu2 | (9 aš) gu2 | 𒐇 𒄘 |
| 1(u) gu2 | (1 u) gu2 | 𒌋 𒄘 |
| 1(u) 1(aš) gu2 | (1 u 1 aš) gu2 | 𒌋 𒀸 𒄘 |
| 1(u) 2(aš) gu2 | (1 u 2 aš) gu2 | 𒌋 𒐀 𒄘 |
| 1(u) 3(aš) gu2 | (1 u 3 aš) gu2 | 𒌋 𒐁 𒄘 |
| 1(u) 4(aš) gu2 | (1 u 4 aš) gu2 | 𒌋 𒐂 𒄘 |
| 1(u) 5(aš) gu2 | (1 u 5 aš) gu2 | 𒌋 𒐃 𒄘 |
| 1(u) 6(aš) gu2 | (1 u 6 aš) gu2 | 𒌋 𒐄 𒄘 |
| 1(u) 7(aš) gu2 | (1 u 7 aš) gu2 | 𒌋 𒐅 𒄘 |
| 1(u) 8(aš) gu2 | (1 u 8 aš) gu2 | 𒌋 𒐆 𒄘 |
| 1(u) 9(aš) gu2 | (1 u 9 aš) gu2 | 𒌋 𒐇 𒄘 |
| 2(u) gu2 | (2 u) gu2 | 𒎙 𒄘 |
| 3(u) gu2 | (3 u) gu2 ku_babbar | 𒌍 𒄘 𒆬 𒌓 |
| 4(u) gu2 | (4 u) gu2 | 𒐏 𒄘 |
| 5(u) gu2 | (5 u) gu2 | 𒐐 𒄘 |
| 1(geš2) gu2 | (1 geš) gu2 | 𒐕 𒄘 |
|  | (1 geš 1 u) gu2 | 𒐕 𒌋 𒄘 |
| 1(geš2) 2(u) gu2 | (1 geš 2 u) gu2 | 𒐕 𒎙 𒄘 |
| 1(geš2) 3(u) gu2 | (1 geš 3 u) gu2 | 𒐕 𒌍 𒄘 |
| 1(geš2) 4(u) gu2 | (1 geš 4 u) gu2 | 𒐕 𒐏 𒄘 |
| 1(geš2) 5(u) gu2 | (1 geš 5 u) gu2 | 𒐕 𒐐 𒄘 |
| 2(geš2) gu2 | (2 geš) gu2 | 𒐖 𒄘 |
| 3(geš2) gu2 | (3 geš) gu2 ku_babbar | 𒐗 𒄘 𒆬 𒌓 |
| 4(geš2) gu2 | (4 geš) gu2 | 𒐘 𒄘 |
| 5(geš2) gu2 | (5 geš) gu2 | 𒐙 𒄘 |
| 6(geš2) gu2 | (6 geš) gu2 | 𒐚 𒄘 |
| 7(geš2) gu2 | (7 geš) gu2 | 𒐛 𒄘 |
| 8(geš2) gu2 | (8 geš) gu2 | 𒐜 𒄘 |
| 9(geš2) gu2 | (9 geš) gu2 | 𒐝 𒄘 |
| 1(geš’u) gu2 | (1 geš'u) gu2 | 𒐞 𒄘 |
| 2(geš’u) gu2 | (2 geš'u) gu2 ku_babbar | 𒐟 𒄘 𒆬 𒌓 |
| 3(geš’u) gu2 | (3 geš'u) gu2 | 𒐠 𒄘 |
| 4(geš’u) gu2 | (4 geš'u) gu2 | 𒐡 𒄘 |
| 5(geš’u) gu2 | (5 geš'u) gu2 | 𒐢 𒄘 |
| 1(šar2) gu2 | (1 šar2) gu2 | 𒊹 𒄘 |
| 2(šar2) gu2 | (2 šar2) gu2 ku_babbar | 𒐣 𒄘 𒆬 𒌓 |
| 3(šar2) gu2 | (3 šar2) gu2 | 𒐤 𒄘 |
| 4(šar2) gu2 | (4 šar2) gu2 | 𒐦 𒄘 |
| 5(šar2) gu2 | (5 šar2) gu2 | 𒐧 𒄘 |
| 6(šar2) gu2 | (6 šar2) gu2 | 𒐨 𒄘 |
| 7(šar2) gu2 | (7 šar2) gu2 | 𒐩 𒄘 |
| 8(šar2) gu2 | (8 šar2) gu2 | 𒐪 𒄘 |
| 9(šar2) gu2 | (9 šar2) gu2 | 𒐫 𒄘 |
| 1(šar’u) gu2 | (1 šar'u) gu2 | 𒐬 𒄘 |
| 2(šar’u) gu2 | (2 šar'u) gu2 ku_babbar | 𒐭 𒄘 𒆬 𒌓 |
| 3(šar’u) gu2 | (3 šar'u) gu2 | 𒐮 𒄘 |
| 4(šar’u) gu2 | (4 šar'u) gu2 | 𒐰 𒄘 |
| 5(šar’u) gu2 | (5 šar'u) gu2 | 𒐱 𒄘 |
| 1(šargal)gal gu2 | (1 šar2-gal) gu2 | 𒐲 𒄘 |
|  | 180000 gu2 |  |
|  | 216000 gu2 |  |

</details>

<details>

<summary>📋 Surfaces (Proust §8.3)</summary>

| §8.3. Surfaces (a-ša3) | MesoMath | MesoMath (Cun.) |
|---|---|---|
| 1/3 sar a-ša3 | 1/3 sar ku_babbar | 𒑚 𒊬 𒀀𒊮 |
| 1/2 sar | 1/2 sar | 𒈦 𒊬 |
| 2/3 sar | 2/3 sar | 𒑛 𒊬 |
| 5/6 sar | 5/6 sar | 𒑜 𒊬 |
| 1(diš) sar | (1 diš) sar | 𒀸 𒊬 |
|  | (1 diš) 1/6 sar | 𒀸 𒑡 𒊬 |
| 1(diš) 1/3 sar | (1 diš) 1/3 sar | 𒀸 𒑚 𒊬 |
| 1(diš) 1/2 sar | (1 diš) 1/2 sar | 𒀸 𒈦 𒊬 |
| 1(diš) 2/3 sar | (1 diš) 2/3 sar | 𒀸 𒑛 𒊬 |
| 1(diš) 5/6 sar | (1 diš) 5/6 sar | 𒀸 𒑜 𒊬 |
| 2(diš) sar | (2 diš) sar | 𒐀 𒊬 |
| 3(diš) sar | (3 diš) sar ku_babbar | 𒐁 𒊬 𒀀𒊮 |
| 4(diš) sar | (4 diš) sar | 𒐂 𒊬 |
| 5(diš) sar | (5 diš) sar | 𒐃 𒊬 |
| 6(aš) sar | (6 diš) sar | 𒐄 𒊬 |
| 7(diš) sar | (7 diš) sar | 𒐅 𒊬 |
| 8(diš) sar | (8 diš) sar | 𒐆 𒊬 |
| 9(diš) sar | (9 diš) sar | 𒐇 𒊬 |
| 1(u) sar | (1 u) sar | 𒌋 𒊬 |
| 1(u) 1(diš) sar | (1 u 1 diš) sar | 𒌋 𒀸 𒊬 |
| 1(u) 2(diš) sar | (1 u 2 diš) sar | 𒌋 𒐀 𒊬 |
| 1(u) 3(diš) sar | (1 u 3 diš) sar | 𒌋 𒐁 𒊬 |
| 1(u) 4(diš) sar | (1 u 4 diš) sar | 𒌋 𒐂 𒊬 |
| 1(u) 5(diš) sar | (1 u 5 diš) sar | 𒌋 𒐃 𒊬 |
| 1(u) 6(aš) sar | (1 u 6 diš) sar | 𒌋 𒐄 𒊬 |
| 1(u) 7(diš) sar | (1 u 7 diš) sar | 𒌋 𒐅 𒊬 |
| 1(u) 8(diš) sar | (1 u 8 diš) sar | 𒌋 𒐆 𒊬 |
| 1(u) 9(diš) sar | (1 u 9 diš) sar | 𒌋 𒐇 𒊬 |
| 2(u) sar | (2 u) sar | 𒎙 𒊬 |
| 3(u) sar | (3 u) sar ku_babbar | 𒌍 𒊬 𒀀𒊮 |
| 4(u) sar | (4 u) sar | 𒐏 𒊬 |
| 1(ubu) GAN2 | 1/2 GAN2 | 𒈦 𒃷 |
| 1(ubu) GAN2 1(u) sar | 1/2 GAN2 (1 u) sar | 𒈦 𒃷 𒌋 𒊬 |
| 1(ubu) GAN2 2(u) sar | 1/2 GAN2 (2 u) sar | 𒈦 𒃷 𒎙 𒊬 |
| 1(ubu) GAN2 3(u) sar | 1/2 GAN2 (3 u) sar | 𒈦 𒃷 𒌍 𒊬 |
| 1(ubu) GAN2 4(u) sar | 1/2 GAN2 (4 u) sar | 𒈦 𒃷 𒐏 𒊬 |
| 1(iku) GAN2 | (1 iku) GAN2 | 𒀸 𒃷 |
| 1(iku) 1(ubu) GAN2 | (1 iku) 1/2 GAN2 ku_babbar | 𒀸 𒈦 𒃷 𒀀𒊮 |
| 2(iku) GAN2 | (2 iku) GAN2 | 𒐀 𒃷 |
| 2(iku) 1(ubu) GAN2 | (2 iku) 1/2 GAN2 | 𒐀 𒈦 𒃷 |
| 3(iku) GAN2 | (3 iku) GAN2 | 𒐁 𒃷 |
| 3(iku) 1(ubu) GAN2 | (3 iku) 1/2 GAN2 | 𒐁 𒈦 𒃷 |
| 4(iku) GAN2 | (4 iku) GAN2 | 𒐂 𒃷 |
| 4(iku) 1(ubu) GAN2 | (4 iku) 1/2 GAN2 | 𒐂 𒈦 𒃷 |
| 5(iku) GAN2 | (5 iku) GAN2 | 𒐃 𒃷 |
| 5(iku) 1(ubu) GAN2 | (5 iku) 1/2 GAN2 | 𒐃 𒈦 𒃷 |
| 1(eše3) GAN2 | (1 eše3) GAN2 | 𒑘 𒃷 |
| 1(eše3) 1(iku) GAN2 | (1 eše3 1 iku) GAN2 ku_babbar | 𒑘 𒀸 𒃷 𒀀𒊮 |
| 1(eše3) 2(iku) GAN2 | (1 eše3 2 iku) GAN2 | 𒑘 𒐀 𒃷 |
| 1(eše3) 3(iku) GAN2 | (1 eše3 3 iku) GAN2 | 𒑘 𒐁 𒃷 |
| 1(eše3) 4(iku) GAN2 | (1 eše3 4 iku) GAN2 | 𒑘 𒐂 𒃷 |
| 1(eše3) 5(iku) GAN2 | (1 eše3 5 iku) GAN2 | 𒑘 𒐃 𒃷 |
| 2(eše3) GAN2 | (2 eše3) GAN2 | 𒑙 𒃷 |
| 2(eše3) 1(iku) GAN2 | (2 eše3 1 iku) GAN2 | 𒑙 𒀸 𒃷 |
| 2(eše3) 2(iku) GAN2 | (2 eše3 2 iku) GAN2 | 𒑙 𒐀 𒃷 |
| 2(eše3) 3(iku) GAN2 | (2 eše3 3 iku) GAN2 | 𒑙 𒐁 𒃷 |
| 2(eše3) 4(iku) GAN2 | (2 eše3 4 iku) GAN2 | 𒑙 𒐂 𒃷 |
| 2(eše3) 5(iku) GAN2 | (2 eše3 5 iku) GAN2 | 𒑙 𒐃 𒃷 |
| 1(bur3) GAN2 | (1 bur3) GAN2 | 𒌋 𒃷 |
| 1(bur3) 1(eše3) GAN2 | (1 bur3 1 eše3) GAN2 ku_babbar | 𒌋 𒑘 𒃷 𒀀𒊮 |
| 1(bur3) 2(eše3) GAN2 | (1 bur3 2 eše3) GAN2 | 𒌋 𒑙 𒃷 |
| 2(bur3) GAN2 | (2 bur3) GAN2 | 𒎙 𒃷 |
| 3(bur3) GAN2 | (3 bur3) GAN2 ku_babbar | 𒌍 𒃷 𒀀𒊮 |
| 4(bur3) GAN2 | (4 bur3) GAN2 | 𒐏 𒃷 |
| 5(bur3) GAN2 | (5 bur3) GAN2 | 𒐐 𒃷 |
| 6(bur3) GAN2 | (6 bur3) GAN2 | 𒐑 𒃷 |
| 7(bur3) GAN2 | (7 bur3) GAN2 | 𒐒 𒃷 |
| 8(bur3) GAN2 | (8 bur3) GAN2 | 𒐓 𒃷 |
| 9(bur3) GAN2 | (9 bur3) GAN2 | 𒐔 𒃷 |
| 1(bur’u) GAN2 | (1 bur'u) GAN2 | 𒐴 𒃷 |
| 1(bur’u) 1(bur3) GAN2 | (1 bur'u 1 bur3) GAN2 | 𒐴 𒌋 𒃷 |
| 1(bur’u) 2(bur3) GAN2 | (1 bur'u 2 bur3) GAN2 | 𒐴 𒎙 𒃷 |
| 1(bur’u) 3(bur3) GAN2 | (1 bur'u 3 bur3) GAN2 | 𒐴 𒌍 𒃷 |
| 1(bur’u) 4(bur3) GAN2 | (1 bur'u 4 bur3) GAN2 | 𒐴 𒐏 𒃷 |
| 1(bur’u) 5(bur3) GAN2 | (1 bur'u 5 bur3) GAN2 | 𒐴 𒐐 𒃷 |
| 1(bur’u) 6(bur3) GAN2 | (1 bur'u 6 bur3) GAN2 | 𒐴 𒐑 𒃷 |
| 1(bur’u) 7(bur3) GAN2 | (1 bur'u 7 bur3) GAN2 | 𒐴 𒐒 𒃷 |
| 1(bur’u) 8(bur3) GAN2 | (1 bur'u 8 bur3) GAN2 | 𒐴 𒐓 𒃷 |
| 1(bur’u) 9(bur3) GAN2 | (1 bur'u 9 bur3) GAN2 | 𒐴 𒐔 𒃷 |
| 2(bur’u) GAN2 | (2 bur'u) GAN2 | 𒐵 𒃷 |
| 3(bur’u) GAN2 | (3 bur'u) GAN2 ku_babbar | 𒐶 𒃷 𒀀𒊮 |
| 4(bur’u) GAN2 | (4 bur'u) GAN2 | 𒐸 𒃷 |
| 5(bur’u) GAN2 | (5 bur'u) GAN2 | 𒐹 𒃷 |
| 1(šar2) GAN2 | (1 šar2) GAN2 |  |
| 1(šar2) 1(bur’u) GAN2 | (1 šar2 1 bur'u) GAN2 |  |
| 1(šar2) 2(bur’u) GAN2 | (1 šar2 2 bur'u) GAN2 |  |
| 1(šar2) 3(bur’u) GAN2 | (1 šar2 3 bur'u) GAN2 |  |
| 1(šar2) 4(bur’u) GAN2 | (1 šar2 4 bur'u) GAN2 | 𒊹 𒃷 |
| 1(šar2) 5(bur’u) GAN2 | (1 šar2 5 bur'u) GAN2 | 𒊹 𒐴 𒃷 |
| 2(šar2) GAN2 | (2 šar2) GAN2 | 𒊹 𒐵 𒃷 |
| 3(šar2) GAN2 | (3 šar2) GAN2 ku_babbar | 𒊹 𒃷 𒀀𒊮 |
| 4(šar2) GAN2 | (4 šar2) GAN2 | 𒐣 𒐸 𒃷 |
| 5(šar2) GAN2 | (5 šar2) GAN2 | 𒐤 𒃷 |
| 6(šar2) GAN2 | (6 šar2) GAN2 | 𒐤 𒃷 |
| 7(šar2) GAN2 | (7 šar2) GAN2 | 𒐦 𒐵 𒃷 |
| 8(šar2) GAN2 | (8 šar2) GAN2 | 𒐦 𒃷 |
| 9(šar2) GAN2 | (9 šar2) GAN2 | 𒐧 𒐸 𒃷 |
| 1(šar’u) GAN2 | (1 šar'u) GAN2 | 𒐨 𒃷 |
| 1(šar’u) 1(šar2) GAN2 | (1 šar'u 1 šar2) GAN2 | 𒐨 𒃷 |
| 1(šar’u) 2(šar2) GAN2 | (1 šar'u 2 šar2) GAN2 | 𒐩 𒐵 𒃷 |
| 1(šar’u) 3(šar2) GAN2 | (1 šar'u 3 šar2) GAN2 | 𒐩 𒃷 |
| 1(šar’u) 4(šar2) GAN2 | (1 šar'u 4 šar2) GAN2 | 𒐪 𒐸 𒃷 |
| 1(šar’u) 5(šar2) GAN2 | (1 šar'u 5 šar2) GAN2 | 𒐫 𒃷 |
| 1(šar’u) 6(šar2) GAN2 | (1 šar'u 6 šar2) GAN2 | 𒐫 𒃷 |
| 1(šar’u) 7(šar2) GAN2 | (1 šar'u 7 šar2) GAN2 | 𒐬 𒐵 𒃷 |
| 1(šar’u) 8(šar2) GAN2 | (1 šar'u 8 šar2) GAN2 | 𒐬 𒃷 |
| 1(šar’u) 9(šar2) GAN2 | (1 šar'u 9 šar2) GAN2 | 𒐬 𒊹 𒐸 𒃷 |
| 2(šar’u) GAN2 | (2 šar'u) GAN2 | 𒐬 𒐣 𒃷 |
| 3(šar’u) GAN2 | (3 šar'u) GAN2 ku_babbar | 𒐬 𒐪 𒃷 𒀀𒊮 |
| 4(šar’u) GAN2 | (4 šar'u) GAN2 | 𒐭 𒐦 𒃷 |
| 5(šar’u) GAN2 | (5 šar'u) GAN2 | 𒐮 𒃷 |
| 1(šargal)gal GAN2 | (1 šar2-gal) GAN2 | 𒐮 𒐨 𒃷 |
| 1(šargal)gal šu-nu-tag GAN2 |  |  |

</details>

<details>

<summary>📋 Lengths (Proust §8.4)</summary>

| §8.4. Lengths (uš, sag,dagal) | MesoMath | MesoMath (Cun.) |
|---|---|---|
| 1(diš) šu-si | (1 diš) šu-si gid | 𒀸 𒋗 𒋛 𒁍 |
| 2(diš) šu-si | (2 diš) šu-si | 𒐀 𒋗 𒋛 |
| 3(diš) šu-si | (3 diš) šu-si | 𒐁 𒋗 𒋛 |
| 4(diš) šu-si | (4 diš) šu-si | 𒐂 𒋗 𒋛 |
| 5(diš) šu-si | (5 diš) šu-si | 𒐃 𒋗 𒋛 |
| 6(aš) šu-si | (6 diš) šu-si | 𒐄 𒋗 𒋛 |
| 7(diš) šu-si | (7 diš) šu-si | 𒐅 𒋗 𒋛 |
| 8(diš) šu-si | (8 diš) šu-si | 𒐆 𒋗 𒋛 |
| 9(diš) šu-si | (9 diš) šu-si | 𒐇 𒋗 𒋛 |
| 1/3 kuš3 | 1/3 kuš3 | 𒑚 𒌑 |
| 1/3 kuš3 1(diš) šu-si | 1/3 kuš3 (1 diš) šu-si | 𒑚 𒌑 𒀸 𒋗 𒋛 |
| 1/3 kuš3 2(diš) šu-si | 1/3 kuš3 (2 diš) šu-si | 𒑚 𒌑 𒐀 𒋗 𒋛 |
| 1/3 kuš3 3(diš) šu-si | 1/3 kuš3 (3 diš) šu-si | 𒑚 𒌑 𒐁 𒋗 𒋛 |
| 1/3 kuš3 4(diš) šu-si | 1/3 kuš3 (4 diš) šu-si | 𒑚 𒌑 𒐂 𒋗 𒋛 |
| 1/2 kuš3 | 1/2 kuš3 | 𒈦 𒌑 |
| 1/2 kuš3 1(diš) šu-si | 1/2 kuš3 (1 diš) šu-si | 𒈦 𒌑 𒀸 𒋗 𒋛 |
| 1/2 kuš3 2(diš) šu-si | 1/2 kuš3 (2 diš) šu-si | 𒈦 𒌑 𒐀 𒋗 𒋛 |
| 1/2 kuš3 3(diš) šu-si | 1/2 kuš3 (3 diš) šu-si | 𒈦 𒌑 𒐁 𒋗 𒋛 |
| 1/2 kuš3 4(diš) šu-si | 1/2 kuš3 (4 diš) šu-si | 𒈦 𒌑 𒐂 𒋗 𒋛 |
| 2/3 kuš3 | 2/3 kuš3 | 𒑛 𒌑 |
| 2/3 kuš3 1(diš) šu-si | 2/3 kuš3 (1 diš) šu-si | 𒑛 𒌑 𒀸 𒋗 𒋛 |
| 2/3 kuš3 2(diš) šu-si | 2/3 kuš3 (2 diš) šu-si | 𒑛 𒌑 𒐀 𒋗 𒋛 |
| 2/3 kuš3 3(diš) šu-si | 2/3 kuš3 (3 diš) šu-si | 𒑛 𒌑 𒐁 𒋗 𒋛 |
| 2/3 kuš3 4(diš) šu-si | 2/3 kuš3 (4 diš) šu-si | 𒑛 𒌑 𒐂 𒋗 𒋛 |
| 5/6 kuš3 | 5/6 kuš3 | 𒑜 𒌑 |
| 5/6 kuš3 1(diš) šu-si | 5/6 kuš3 (1 diš) šu-si | 𒑜 𒌑 𒀸 𒋗 𒋛 |
| 5/6 kuš3 2(diš) šu-si | 5/6 kuš3 (2 diš) šu-si | 𒑜 𒌑 𒐀 𒋗 𒋛 |
| 5/6 kuš3 3(diš) šu-si | 5/6 kuš3 (3 diš) šu-si | 𒑜 𒌑 𒐁 𒋗 𒋛 |
| 5/6 kuš3 4(diš) šu-si | 5/6 kuš3 (4 diš) šu-si | 𒑜 𒌑 𒐂 𒋗 𒋛 |
| 1(diš) kuš3 | (1 diš) kuš3 | 𒀸 𒌑 |
|  | (1 diš) kuš3 (5 diš) šu-si gid | 𒀸 𒌑 𒐃 𒋗 𒋛 𒁍 |
| 1(diš) 1/3 kuš3 | (1 diš) 1/3 kuš3 | 𒀸 𒑚 𒌑 |
| 1(diš) 1/2 kuš3 | (1 diš) 1/2 kuš3 | 𒀸 𒈦 𒌑 |
| 1(diš) 2/3 kuš3 | (1 diš) 2/3 kuš3 | 𒀸 𒑛 𒌑 |
|  | (1 diš) 5/6 kuš3 | 𒀸 𒑜 𒌑 |
| 2(diš) kuš3 | (2 diš) kuš3 | 𒐀 𒌑 |
| 3(diš) kuš3 | (3 diš) kuš3 gid | 𒐁 𒌑 𒁍 |
| 4(diš) kuš3 | 1/3 ninda | 𒑚 𒃻 |
| 5(diš) kuš3 | 1/3 ninda (1 diš) kuš3 | 𒑚 𒃻 𒀸 𒌑 |
| 1/2 ninda | 1/2 ninda | 𒈦 𒃻 |
| 1/2 ninda 1(diš) kuš3 | 1/2 ninda (1 diš) kuš3 | 𒈦 𒃻 𒀸 𒌑 |
| 1/2 ninda 2(diš) kuš3 | 2/3 ninda | 𒑛 𒃻 |
| 1/2 ninda 3(diš) kuš3 | 2/3 ninda (1 diš) kuš3 | 𒑛 𒃻 𒀸 𒌑 |
| 1/2 ninda 4(diš) kuš3 | 5/6 ninda | 𒑜 𒃻 |
| 1/2 ninda 5(diš) kuš3 | 5/6 ninda (1 diš) kuš3 | 𒑜 𒃻 𒀸 𒌑 |
| 1(diš) ninda | (1 diš) ninda | 𒀸 𒃻 |
| 1(diš) 1/2 ninda | (1 diš) 1/2 ninda gid | 𒀸 𒈦 𒃻 𒁍 |
| 2(diš) ninda | (2 diš) ninda | 𒐀 𒃻 |
| 2(diš) 1/2 ninda | (2 diš) 1/2 ninda | 𒐀 𒈦 𒃻 |
| 3(diš) ninda | (3 diš) ninda | 𒐁 𒃻 |
| 3(diš) 1/2 ninda | (3 diš) 1/2 ninda | 𒐁 𒈦 𒃻 |
| 4(diš) ninda | (4 diš) ninda | 𒐂 𒃻 |
| 4(diš) 1/2 ninda | (4 diš) 1/2 ninda | 𒐂 𒈦 𒃻 |
| 5(diš) ninda | (5 diš) ninda | 𒐃 𒃻 |
| 5(diš) 1/2 ninda | (5 diš) 1/2 ninda | 𒐃 𒈦 𒃻 |
| 6(diš) ninda | (6 diš) ninda | 𒐄 𒃻 |
| 6(diš) 1/2 ninda | (6 diš) 1/2 ninda | 𒐄 𒈦 𒃻 |
| 7(diš) ninda | (7 diš) ninda | 𒐅 𒃻 |
| 7(diš) 1/2 ninda | (7 diš) 1/2 ninda | 𒐅 𒈦 𒃻 |
| 8(diš) ninda | (8 diš) ninda | 𒐆 𒃻 |
| 8(diš) 1/2 ninda | (8 diš) 1/2 ninda | 𒐆 𒈦 𒃻 |
| 9(diš) ninda | (9 diš) ninda | 𒐇 𒃻 |
| 9(diš) 1/2 ninda | (9 diš) 1/2 ninda | 𒐇 𒈦 𒃻 |
| 1(u) ninda | (1 u) ninda | 𒌋 𒃻 |
| 2(u) ninda | 1/3 UŠ gid | 𒑚 𒍑 𒁍 |
| 3(u) ninda | 1/2 UŠ | 𒈦 𒍑 |
| 4(u) ninda | 2/3 UŠ | 𒑛 𒍑 |
| 4(u) 5(diš) ninda | 2/3 UŠ (5 diš) ninda gid | 𒑛 𒍑 𒐃 𒃻 𒁍 |
| 5(u) ninda | 5/6 UŠ | 𒑜 𒍑 |
| 5(u) 5(diš) ninda | 5/6 UŠ (5 diš) ninda | 𒑜 𒍑 𒐃 𒃻 |
| 1(diš) UŠ | (1 diš) UŠ | 𒀸 𒍑 |
| 1(diš) UŠ 1(u) ninda | (1 diš) UŠ (1 u) ninda gid | 𒀸 𒍑 𒌋 𒃻 𒁍 |
| 1(diš) UŠ 2(u) ninda | (1 diš) 1/3 UŠ | 𒀸 𒑚 𒍑 |
| 1(diš) UŠ 3(u) ninda | (1 diš) 1/2 UŠ | 𒀸 𒈦 𒍑 |
| 1(diš) UŠ 4(u) ninda | (1 diš) 2/3 UŠ | 𒀸 𒑛 𒍑 |
| 1(diš) UŠ 5(u) ninda | (1 diš) 5/6 UŠ | 𒀸 𒑜 𒍑 |
| 2(diš) UŠ | (2 diš) UŠ | 𒐀 𒍑 |
| 3(diš) UŠ | (3 diš) UŠ gid | 𒐁 𒍑 𒁍 |
| 4(diš) UŠ | (4 diš) UŠ | 𒐂 𒍑 |
| 5(diš) UŠ | (5 diš) UŠ | 𒐃 𒍑 |
| 6(diš) UŠ | (6 diš) UŠ | 𒐄 𒍑 |
| 7(diš) UŠ | (7 diš) UŠ | 𒐅 𒍑 |
| 8(diš) UŠ | (8 diš) UŠ | 𒐆 𒍑 |
| 9(diš) UŠ | (9 diš) UŠ | 𒐇 𒍑 |
| 1(u) UŠ | 1/3 danna | 𒑚 𒆜 𒁍 |
| 1(u) 1(diš) UŠ | 1/3 danna (1 diš) UŠ | 𒑚 𒆜 𒁍 𒀸 𒍑 |
| 1(u) 2(diš) UŠ | 1/3 danna (2 diš) UŠ | 𒑚 𒆜 𒁍 𒐀 𒍑 |
| 1(u) 3(diš) UŠ | 1/3 danna (3 diš) UŠ | 𒑚 𒆜 𒁍 𒐁 𒍑 |
| 1(u) 4(diš) UŠ | 1/3 danna (4 diš) UŠ | 𒑚 𒆜 𒁍 𒐂 𒍑 |
| 1/2 danna | 1/2 danna | 𒈦 𒆜 𒁍 |
| 1/2 danna 1(diš) UŠ | 1/2 danna (1 diš) UŠ | 𒈦 𒆜 𒁍 𒀸 𒍑 |
| 1/2 danna 2(diš) UŠ | 1/2 danna (2 diš) UŠ | 𒈦 𒆜 𒁍 𒐀 𒍑 |
| 1/2 danna 3(diš) UŠ | 1/2 danna (3 diš) UŠ | 𒈦 𒆜 𒁍 𒐁 𒍑 |
| 1/2 danna 4(diš) UŠ | 1/2 danna (4 diš) UŠ | 𒈦 𒆜 𒁍 𒐂 𒍑 |
| 2/3 danna | 2/3 danna | 𒑛 𒆜 𒁍 |
| 2/3 danna 1(diš) UŠ | 2/3 danna (1 diš) UŠ | 𒑛 𒆜 𒁍 𒀸 𒍑 |
| 2/3 danna 2(diš) UŠ | 2/3 danna (2 diš) UŠ | 𒑛 𒆜 𒁍 𒐀 𒍑 |
| 2/3 danna 3(diš) UŠ | 2/3 danna (3 diš) UŠ | 𒑛 𒆜 𒁍 𒐁 𒍑 |
| 2/3 danna 4(diš) UŠ | 2/3 danna (4 diš) UŠ | 𒑛 𒆜 𒁍 𒐂 𒍑 |
| 5/6 danna | 5/6 danna | 𒑜 𒆜 𒁍 |
| 5/6 danna 1(diš) UŠ | 5/6 danna (1 diš) UŠ | 𒑜 𒆜 𒁍 𒀸 𒍑 |
| 5/6 danna 2(diš) UŠ | 5/6 danna (2 diš) UŠ | 𒑜 𒆜 𒁍 𒐀 𒍑 |
| 5/6 danna 3(diš) UŠ | 5/6 danna (3 diš) UŠ | 𒑜 𒆜 𒁍 𒐁 𒍑 |
| 5/6 danna 4(diš) UŠ | 5/6 danna (4 diš) UŠ | 𒑜 𒆜 𒁍 𒐂 𒍑 |
| 1(diš) danna | (1 diš) danna | 𒀸 𒆜 𒁍 |
|  | (1 diš) danna (5 diš) UŠ gid | 𒀸 𒆜 𒁍 𒐃 𒍑 𒁍 |
|  | (1 diš) 1/3 danna | 𒀸 𒑚 𒆜 𒁍 |
| 1(diš) 1/2 danna | (1 diš) 1/2 danna | 𒀸 𒈦 𒆜 𒁍 |
| 1(diš) 2/3 danna | (1 diš) 2/3 danna | 𒀸 𒑛 𒆜 𒁍 |
| 1(diš) 5/6 danna | (1 diš) 5/6 danna | 𒀸 𒑜 𒆜 𒁍 |
| 2(diš) danna | (2 diš) danna | 𒐀 𒆜 𒁍 |
| 2(diš) 1/2 danna | (2 diš) 1/2 danna gid | 𒐀 𒈦 𒆜 𒁍 𒁍 |
| 3(diš) danna | (3 diš) danna | 𒐁 𒆜 𒁍 |
| 3(diš) 1/2 danna | (3 diš) 1/2 danna | 𒐁 𒈦 𒆜 𒁍 |
| 4(diš) danna | (4 diš) danna | 𒐂 𒆜 𒁍 |
| 4(diš) 1/2 danna | (4 diš) 1/2 danna | 𒐂 𒈦 𒆜 𒁍 |
| 5(diš) danna | (5 diš) danna | 𒐃 𒆜 𒁍 |
| 5(diš) 1/2 danna | (5 diš) 1/2 danna | 𒐃 𒈦 𒆜 𒁍 |
| 6(diš) danna | (6 diš) danna | 𒐄 𒆜 𒁍 |
| 6(diš) 1/2 danna | (6 diš) 1/2 danna | 𒐄 𒈦 𒆜 𒁍 |
| 7(diš) danna | (7 diš) danna | 𒐅 𒆜 𒁍 |
| 7(diš) 1/2 danna | (7 diš) 1/2 danna | 𒐅 𒈦 𒆜 𒁍 |
| 8(diš) danna | (8 diš) danna | 𒐆 𒆜 𒁍 |
| 8(diš) 1/2 danna | (8 diš) 1/2 danna | 𒐆 𒈦 𒆜 𒁍 |
| 9(diš) danna | (9 diš) danna | 𒐇 𒆜 𒁍 |
| 9(diš) 1/2 danna | (9 diš) 1/2 danna | 𒐇 𒈦 𒆜 𒁍 |
| 1(u) danna | (1 u) danna | 𒌋 𒆜 𒁍 |
| 1(u) 1/2 danna | (1 u) 1/2 danna | 𒌋 𒈦 𒆜 𒁍 |
| 1(u) 1(diš) danna | (1 u 1 diš) danna | 𒌋 𒀸 𒆜 𒁍 |
| 1(u) 1(diš) 1/2 danna | (1 u 1 diš) 1/2 danna | 𒌋 𒀸 𒈦 𒆜 𒁍 |
| 1(u) 2(diš) danna | (1 u 2 diš) danna | 𒌋 𒐀 𒆜 𒁍 |
| 1(u) 2(diš) 1/2 danna | (1 u 2 diš) 1/2 danna | 𒌋 𒐀 𒈦 𒆜 𒁍 |
| 1(u) 3(diš) danna | (1 u 3 diš) danna | 𒌋 𒐁 𒆜 𒁍 |
| 1(u) 3(diš) 1/2 danna | (1 u 3 diš) 1/2 danna | 𒌋 𒐁 𒈦 𒆜 𒁍 |
| 1(u) 4(diš) danna | (1 u 4 diš) danna | 𒌋 𒐂 𒆜 𒁍 |
| 1(u) 4(diš) 1/2 danna | (1 u 4 diš) 1/2 danna | 𒌋 𒐂 𒈦 𒆜 𒁍 |
| 1(u) 5(diš) danna | (1 u 5 diš) danna | 𒌋 𒐃 𒆜 𒁍 |
| 1(u) 5(diš) 1/2 danna | (1 u 5 diš) 1/2 danna | 𒌋 𒐃 𒈦 𒆜 𒁍 |
| 1(u) 6(diš) danna | (1 u 6 diš) danna | 𒌋 𒐄 𒆜 𒁍 |
| 1(u) 6(diš) 1/2 danna | (1 u 6 diš) 1/2 danna | 𒌋 𒐄 𒈦 𒆜 𒁍 |
| 1(u) 7(diš) danna | (1 u 7 diš) danna | 𒌋 𒐅 𒆜 𒁍 |
| 1(u) 7(diš) 1/2 danna | (1 u 7 diš) 1/2 danna | 𒌋 𒐅 𒈦 𒆜 𒁍 |
| 1(u) 8(diš) danna | (1 u 8 diš) danna | 𒌋 𒐆 𒆜 𒁍 |
| 1(u) 8(diš) 1/2 danna | (1 u 8 diš) 1/2 danna | 𒌋 𒐆 𒈦 𒆜 𒁍 |
| 1(u) 9(diš) danna | (1 u 9 diš) danna | 𒌋 𒐇 𒆜 𒁍 |
| 1(u) 9(diš) 1/2 danna | (1 u 9 diš) 1/2 danna | 𒌋 𒐇 𒈦 𒆜 𒁍 |
| 2(u) danna | (2 u) danna | 𒎙 𒆜 𒁍 |
| 2(u) 1(diš) danna | (2 u 1 diš) danna gid | 𒎙 𒀸 𒆜 𒁍 𒁍 |
| 2(u) 2(diš) danna | (2 u 2 diš) danna | 𒎙 𒐀 𒆜 𒁍 |
| 2(u) 3(diš) danna | (2 u 3 diš) danna | 𒎙 𒐁 𒆜 𒁍 |
| 2(u) 4(diš) danna | (2 u 4 diš) danna | 𒎙 𒐂 𒆜 𒁍 |
| 2(u) 5(diš) danna | (2 u 5 diš) danna | 𒎙 𒐃 𒆜 𒁍 |
| 2(u) 6(diš) danna | (2 u 6 diš) danna | 𒎙 𒐄 𒆜 𒁍 |
| 2(u) 7(diš) danna | (2 u 7 diš) danna | 𒎙 𒐅 𒆜 𒁍 |
| 2(u) 8(diš) danna | (2 u 8 diš) danna | 𒎙 𒐆 𒆜 𒁍 |
| 2(u) 9(diš) danna | (2 u 9 diš) danna | 𒎙 𒐇 𒆜 𒁍 |
| 3(u) danna | (3 u) danna | 𒌍 𒆜 𒁍 |
| 3(u) 5(diš) danna | (3 u 5 diš) danna gid | 𒌍 𒐃 𒆜 𒁍 𒁍 |
| 4(u) danna | (4 u) danna | 𒐏 𒆜 𒁍 |
| 4(u) 5(diš) danna | (4 u 5 diš) danna | 𒐏 𒐃 𒆜 𒁍 |
| 5(u) danna | (5 u) danna | 𒐐 𒆜 𒁍 |
| 1(geš2) danna | (1 geš) danna gid | 𒐕 𒆜 𒁍 𒁍 |

</details>