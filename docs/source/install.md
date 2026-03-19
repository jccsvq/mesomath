
(installation)=
# Installing MesoMath

## Prerequisites

* **Python:** Version 3.10 or higher.
* **[`pip`](https://pypi.org/project/pip/)** or **[`pipx`](https://pipx.pypa.io/stable/):** Latest version recommended.

## Standard Installation Using `pip` or `pipx`

### `pipx` (Recommended for most users)

This is the simplest way to install **MesoMath** as a standalone tool without worrying about Python environments.

```bash
$ pipx install mesomath

```

This will install the four MesoMath commands in your system's PATH:

* **`babcalc`**: The interactive Mesopotamian calculator.
* **`mtlookup`**: Tool for consulting metrological tables.
* **`metrotable`**: Tool for printing metrological tables.
* **`bmultable`**: Sexagesimal multiplication table generator.

If you cannot run the commands after installation, try:

```bash
$ pipx ensurepath

```

To uninstall the package at any time, simply run:

```bash
$ pipx uninstall mesomath

```

### `pip` (Virtual Environment)

If you prefer using standard `pip`, it is highly recommended to use a virtual environment:

```bash
$python -m venv myenv$ source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
$ pip install mesomath

```

Once installed, you can run any of the tools directly (e.g., `$ babcalc`).

(install-font)=
## Font Configuration (Unicode Cuneiform)

MesoMath requires a font compatible with the Unicode Cuneiform standard to correctly display the glyphs. We recommend Google's **Noto Sans Cuneiform**.

### 1. Font Download

1. Visit [Google Noto Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+Cuneiform).

2. Click on **Download Family**.

3. Unzip the `.zip` file to obtain the `NotoSansCuneiform-Regular.ttf` file.

---

### 2. Installation by Operating System

#### 🐧 Linux

On most distributions, simply move the file to your local fonts directory:

1. Create the directory if it doesn't exist: `mkdir -p ~/.local/share/fonts` (or `~/.fonts` on older systems).

2. Copy the file: `cp NotoSansCuneiform-Regular.ttf ~/.local/share/fonts/`
3. Update the font cache: `fc-cache -f -v`

#### 🪟 [W] Windows

Windows offers two methods, one of which does not require administrator privileges:

1. **Quick Method:** Right-click on the `.ttf` file.

2. Select **"Install for all users"** (requires Admin privileges) or simply **"Install"** (for the current user).

3. Alternatively, you can drag the file to the `C:\Windows\Fonts` folder.

#### 🍎 macOS

The process on Mac is very intuitive using the Font Catalog:

1. Double-click the `NotoSansCuneiform-Regular.ttf` file.

2. A preview window will open. Click the **Install Font** button.

3. The font will be automatically saved to `~/Library/Fonts` and will be available to all your applications (including Terminal).

---

### 3. Verification

Once installed, restart your terminal or IDE and run this test command in Python to confirm that the system recognizes the glyphs:

```python
# Quick Render Test
print("\n\t𒄘 ╼60╾ 𒈠𒈾 ╼60╾ 𒂆\n")

```

If you see the cuneiform characters clearly (and not rectangles), the installation was a success!

<div class="tablet">

| 𒁲 |  |
| --- | --- |
| **Status** | **Environment Ready** |
|  | 𒁲 |

</div>


### ⚙️ Editor Configuration (Optional)

If you're using a code editor, make sure to add 'Noto Sans Cuneiform' to your font family list so the internal console displays MesoMath results correctly.

#### VS Code

1. Go to `Settings` (Ctrl + ,).

2. Search for `Editor: Font Family`.

3. Add `'Noto Sans Cuneiform'` to the beginning of the list (e.g., `'Noto Sans Cuneiform', 'Consoles', 'Courier New'`).

#### PyCharm

1. Go to `Settings` > `Editor` > `Font`.

2. Make sure the **"Enable ligatures"** box is checked and add the font as a **"Fallback font"** or primary font.

## Developer Installation from Sources

1. Clone the repository:
```bash
$ git clone https://github.com/jccsvq/mesomath.git
$ cd mesomath

```


2. We recommend using [`hatch`](https://hatch.pypa.io/latest/) for development:
```bash
$ hatch shell

```


This creates an isolated environment with all dependencies (including `typing-extensions`) and installs `mesomath` in editable mode.

## Verification

To verify the installation, check the version of the calculator:

```bash
$ babcalc --help
babcalc 1.3.0 - Command Line Interface

Usage:
  babcalc                 Launch interactive REPL
  babcalc <script.py>     Execute a script
  babcalc -i <script.py>  Execute a script and stay in interactive mode
  babcalc -m <module>     Run a library module (Reserved for future use)
  babcalc --help          Show this message

```


## Troubleshooting

If you encounter issues during installation or while running the tools, check the following common solutions:

### "Command not found" after installation

This usually happens when your Python script directory is not in your system's `PATH`.

* **If using `pipx**`: Run `pipx ensurepath` to automatically add the necessary directories to your profile.
* **If using `pip**`: Ensure you have activated your virtual environment (`source myenv/bin/activate`) before running the commands.
* **Manual Check**: Verify that the scripts listed in `pyproject.toml` (like `babcalc` or `mtlookup`) are present in your environment's `bin` (Linux/macOS) or `Scripts` (Windows) folder.

### Python Version Mismatch

**MesoMath** requires **Python 3.10 or higher**.

* Check your version by running `$ python --version`.
* If your system's default `python` is an older version (e.g., 3.8), try using `python3` instead:
```bash
$ python3 -m venv myenv

```


* The package uses `typing-extensions` to ensure compatibility with modern type hints on older supported versions of Python.

### Conflicts with other packages

If you see errors related to dependency versions:

* **Isolated Environment**: We strongly recommend using a virtual environment or `pipx` to avoid conflicts with other installed Python tools.
* **Hatch Users**: If `hatch shell` fails, try cleaning the environment first:
```bash
$ hatch env prune

```



### SyntaxWarnings in Documentation (Developers)

If you see a `SyntaxWarning: invalid escape sequence` when building the docs, ensure your `conf.py` uses a **raw string** for the copy button prompt:

```python
# Correct way:
copybutton_prompt_text = r"--> |\.\.\. |\$ "

```
