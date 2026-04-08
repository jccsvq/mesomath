"""This module contains some utility functions for MesoMath"""

from wcwidth import wcswidth


def cunei_ljust(text: str, width: int):
    """Calculate the actual visual width of the cuneiform text
    and justify it to left

    :param text: input string
    :type text: str
    :param width: width of the output string
    :type width: int
    :return: padded string
    :rtype: str
    """
    visual_width = wcswidth(text)
    if visual_width == -1:  # Non-printable characters
        visual_width = len(text)

    padding = width - visual_width
    return text + (" " * padding)


def cunei_rjust(text: str, width: int):
    """Calculate the actual visual width of the cuneiform text
    and justify it to right

    :param text: input string
    :type text: str
    :param width: width of the output string
    :type width: int
    :return: padded string
    :rtype: str
    """
    visual_width = wcswidth(text)
    if visual_width == -1:  # Non-printable characters
        visual_width = len(text)

    padding = width - visual_width
    return (" " * padding) + text


def gen_multi_range(met: type, minv, limits, increments):
    """
    Memory-efficient generator for metrological ranges.
    Yields tuple with decimal values, line number, subtotal and start of section one by one.

    :param met: metrological class
    :type met: type
    :param minv: starting value
    :type minv: str
    :param limits: final value of the sections
    :type limits: str
    :param increments: increments for each section
    :type increments: str
    :raises ValueError: if the number of limits does not match the number of increments.
    :return: decimal values of the metrological class, line number, subtotal and start of section
    :rtype: tuple (int, int, int, bool)
    """

    def to_list(x):
        if isinstance(x, (list, tuple)):
            return x
        return (
            [item.strip() for item in str(x).split(",")] if isinstance(x, str) else [x]
        )

    limit_list = to_list(limits)
    inc_list = to_list(increments)
    subtotal = linenumber = 0

    # Valor inicial
    current_dec = met(minv).dec
    linenumber += 1
    subtotal += current_dec
    yield (current_dec, linenumber, subtotal, True)

    for i in range(len(limit_list)):
        target_dec = met(limit_list[i]).dec
        step_dec = met(inc_list[i]).dec

        # OJO AQUÍ: Solo marcamos 'True' si NO es el primer tramo
        # o si hay un salto real por alineación.
        is_new_section = i > 0

        # --- ALIGNMENT LOGIC ---
        if current_dec % step_dec != 0:
            current_dec = ((current_dec // step_dec) + 1) * step_dec
            if current_dec > target_dec:
                current_dec = target_dec

            linenumber += 1
            subtotal += current_dec
            yield (current_dec, linenumber, subtotal, True)  # Salto = Nueva sección
            is_new_section = False

        while current_dec < target_dec:
            current_dec += step_dec
            if current_dec > target_dec:
                current_dec = target_dec

            linenumber += 1
            subtotal += current_dec
            yield (current_dec, linenumber, subtotal, is_new_section)
            is_new_section = False

        current_dec = target_dec


def to_latex_hex(text: str) -> str:
    """Encode glyphs for LaTeX

    :param text: text to encode
    :type text: str
    :return: encoded text
    :rtype: str
    """
    if not text:
        return ""
    res = []
    for char in text:
        cp = ord(char)
        if cp >= 0x12000:
            res.append(f'\\symbol{{"{cp:X}}}')
        elif char == "\u2009":
            res.append(r"\,")
        else:
            res.append(char)
    return "".join(res)


def translit_to_cunei(text: str) -> str:
    """Translate transliteration to cuneiform

    :param text: transliteration to translate
    :type text: str
    :return: cuneiform string
    :rtype: str
    """
    from mesomath.glyphs import translit_dict

    def search_token(token: str) -> str:
        return translit_dict.get(token, "(?)")

    tt = text.split()

    return "\u2009".join([search_token(t) for t in tt])
