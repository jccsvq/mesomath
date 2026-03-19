"""This module contains the cuneiform glyphs necessary for writing metrological
measurements from the Old Babylonian period. You will need to have a TrueType font
such as Noto Sans Cuneiform or similar installed on your system for proper display.
"""

from wcwidth import wcswidth


def pad_cuneiform(text: str, width: int):
    """Calculate the actual visual width of the cuneiform text
    and justify to left


    Ejemplo de uso:
        cell = f"|{pad_cuneiform(meass, 25)}|"

    :param text: input string
    :type text: str
    :param width: width of the output string
    :type width: int
    :return: padded string
    :rtype: str
    """
    visual_width = wcswidth(text)
    if visual_width == -1:  # Caracteres no imprimibles
        visual_width = len(text)

    padding = width - visual_width
    return text + (" " * padding)

def pad_cuneiform_right(text: str, width: int):
    """Calculate the actual visual width of the cuneiform text
    and justify to right


    Ejemplo de uso:
        cell = f"|{pad_cuneiform(meass, 25)}|"

    :param text: input string
    :type text: str
    :param width: width of the output string
    :type width: int
    :return: padded string
    :rtype: str
    """
    visual_width = wcswidth(text)
    if visual_width == -1:  # Caracteres no imprimibles
        visual_width = len(text)

    padding = width - visual_width
    return (" " * padding) + text





# Ejemplo de uso
# celda = f"|{pad_cuneiform(medida, 25)}|"

# Arithmograms:

#: aš
l_as = ["𒀸", "𒐀", "𒐁", "𒐂", "𒐃", "𒐄", "𒐅", "𒐆", "𒐇"]
#: buru
l_buru = ["𒐴", "𒐵", "𒐶", "𒐸", "𒐹"]
#: diš
l_dis = ["𒁹", "𒐖", "𒐈", "𒐉", "𒐊", "𒐋", "𒐌", "𒐍", "𒐎"]
#: eše3
l_ese3 = ["𒑘", "𒑙"]
#: geš
l_ges = ["𒐕", "𒐖", "𒐗", "𒐘", "𒐙", "𒐚", "𒐛", "𒐜", "𒐝"]
# gešu
l_gesu = ["𒐞", "𒐟", "𒐠", "𒐡", "𒐢"]
#: iku
l_iku = ["𒀸", "𒐀", "𒐁", "𒐂", "𒐃"]
#: šar2
l_sar2 = ["𒊹", "𒐣", "𒐤", "𒐦", "𒐧", "𒐨", "𒐩", "𒐪", "𒐫"]
#: šar2-gal
l_sar2_gal = ["𒐲"]
#: šaru
l_saru = ["𒐬", "𒐭", "𒐮", "𒐰", "𒐱"]
#: u
l_u = ["𒌋", "𒎙", "𒌍", "𒐏", "𒐐", "𒐑", "𒐒", "𒐓", "𒐔"]
#: bur3
l_bur3 = l_u.copy()

# Metrograms:

unit_dict = {
    #: ban2
    "ban": ["𒑏", "𒑐", "𒑑", "𒑒", "𒑔"],
    #: bariga
    "bariga": ["𒁹", "𒑖", "𒑗", "𒐉"],
    #: danna
    "danna": "𒆜𒁍",
    #: GAN2
    "gan": "𒃷",
    #: gin2
    "gin": "𒂆",
    #: gu2
    "gu": "𒄘",
    #: gur
    "gur": "𒄥",
    #: kuš3
    "kus": "𒌑",
    #: ma-na
    "mana": "𒈠𒈾",
    #: ninda
    "ninda": "𒃻",
    #: sar
    "sar": "𒊬",
    #: še
    "se": "𒊺",
    #: sila3
    "sila": "𒋡",
    #: šu-si
    "susi": "𒋗𒋛",
    # US
    "us": "𒍑",
}

# Klasmatograms

#: Fractions:
fglyphdict = {
    "1/6": "𒑡",  # option: 𒅆𒐋
    "1/3": "𒑚",
    "1/2": "𒈦",
    "2/3": "𒑛",
    "5/6": "𒑜",
}

MAP_FRACTIONS = fglyphdict

# Substance Symbols:

subsdict = {
    # Metals & Value
    "ku_babbar": "𒆬𒌓",  # Silver (kù-babbar)
    "urudu": "𒍏",  # Copper (urudu)
    "ku3_sig17": "𒆬𒄀",  # Gold (kù-sig17)
    # Crops & Liquids
    "se": "𒊺",  # Barley (še)
    "ziz2": "𒀾",  # Emmer wheat (zíz)
    "i3_gis": "𒉌𒄑",  # Sesame oil (ì-giš)
    "kas": "𒁉",  # Beer (kaš / bi) - Standard vessel sign
    # Land & Livestock
    "a_sa": "𒀀𒊮",  # Field (a-šà)
    "kiri6": "𒊬",  # Orchard/Garden (kiri6)
    "gu4": "𒄞",  # Ox (gu4)
    "udu": "𒇻",  # Sheep (udu)
    # Textiles & Fibers
    "siki": "𒋠",  # Wool (siki)
    "gada": "𒃰",  # Linen (gada)
    "siki_gi": "𒋠𒄀",  # Native/Standard wool (siki-gi)
    # Fruits & Provisions
    "zu2_lum": "𒍪𒈝",  # Dates (zú-lum)
    "ges_tin": "𒃾",  # Wine (geštin)
    "ga_ar3": "𒂵𒄯",  # Cheese/Curd (ga-àr)
    "i3_nun": "𒉌𒉣",  # Ghee/Butter (ì-nun)
    # Building & Resources
    "esir": "𒀀𒂍",  # Bitumen (esir2 / A.E2) - The most standard form
    "ges": "𒄑",  # Wood/Beam (geš)
    "sig4": "𒋞",  # Brick (sig4)
    "na4": "𒉌",  # Stone (na4)
    # Personnel (Contextual)
    "lu2": "𒇽",  # Man/Worker (lú)
    "geme2": "𒊩",  # Female worker (gemé)
    "er3": "𒀴",  # Slave/Servant (er3)
    # Mathematical States (for Metrotable)
    "igi_nu": "𒅆𒉡",  # Reciprocal not found (igi-nu)
    "igi_nu_du8": "Assistant 𒅆𒉡𒂃",  # Reciprocal does not open (igi-nu-du8)
}

# Dictionary for quick access by unit/system name
MAP_ARITHMOGRAMS = {
    "ash": l_as,
    "dis": l_dis,
    "u": l_u,
    "ges": l_ges,
    "sar2": l_sar2,
    "saru": l_saru,
    "gesu": l_gesu,
}

# Unit dictionary
MAP_UNITS = {
    "SILA3": "𒋡",
    "GUR": "𒄥",
    "BARIGA": "\u122aB",  # 𒉿
    "GIN2": "\u1212F",  # 𒂆
    "KUŠ3": "\u12333",  # 𒌑
    "ŠU-SI": "\u122d7\u122b0",  # 𒋗𒋛
    "DANNA": "\u121a1\u1206D",  # 𒆜𒁍
    "MA-NA": "𒈠𒈾",
}

# Mapping of internal names to Unicode logograms
UNIT_LOGOGRAMS = {
    "sargal": "𒊹",
    "saru": "𒐬",
    "sar": "𒊬",  # U+122AC (SAR)
    "gesu": "𒐞",
    "ges": "𒐕",
    "as": "𒀸",
    "ninda": "𒃻",  # U+122A7 (GAR/NINDA)
    "kush3": "𒌑",
}

# for _MesoM.schema() use
MAP_UNIT_LOGOGRAMS = {
    "ban": "𒑏",
    "bariga": "𒉿",
    "danna": "𒆜𒁍",
    "gan": "𒃷",
    "gin": "𒂆",
    "gu": "𒄘",
    "gur": "𒄥",
    "kus": "𒌑",
    "mana": "𒈠𒈾",
    "ninda": "𒃻",
    "sar": "𒊬",
    "se": "𒊺",
    "sila": "𒋡",
    "susi": "𒋗𒋛",
    "us": "𒍑",
    "u": "𒌋",
    "bur": "𒌋",
    "buru": "𒐴",
    "dis": "𒁹",
    "ese": "𒑘",
    "iku": "𒀸",
} | UNIT_LOGOGRAMS


CUNEIFORM_LABEL_GLYPHS = "𒉆𒁾𒊬"
CUNEIFORM_LABEL_HEX = r'\symbol{"12240}\symbol{"1207E}\symbol{"122AC}'

TIMES_LABEL = "𒀀𒁺"