"""This module contains the cuneiform glyphs necessary for writing metrological
measurements from the Old Babylonian period. You will need to have a TrueType font
such as Noto Sans Cuneiform or similar installed on your system for proper display.
"""


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
#: gešu
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

#: Metrograms:
unit_dict = {
    #: ban2
    "ban": ["𒑏", "𒑐", "𒑑", "𒑒", "𒑔"],
    #: bariga
    "bariga": ["𒁹", "𒑖", "𒑗", "𒐉"],
    #: danna
    "danna": "𒆜 𒁍",
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
    "mana": "𒈠 𒈾",
    #: ninda
    "ninda": "𒃻",
    #: sar
    "sar": "𒊬",
    #: še
    "se": "𒊺",
    #: sila3
    "sila": "𒋡",
    #: šu-si
    "susi": "𒋗 𒋛",
    # US
    "us": "𒍑",
}

#: Klasmatograms
fglyphdict = {
    "1/6": "𒑡",  # option: 𒅆𒐋
    "1/3": "𒑚",
    "1/2": "𒈦",
    "2/3": "𒑛",
    "5/6": "𒑜",
}

MAP_FRACTIONS = fglyphdict

#: Substance Symbols and others:
subsdict = {
    # Metals & Value
    "ku_babbar": "𒆬 𒌓",  # Silver (kù-babbar), also "weight"
    "urudu": "𒍏",  # Copper (urudu)
    "ku3_sig17": "𒆬 𒄀",  # Gold (kù-sig17)
    # Crops & Liquids
    "se": "𒊺",  # Barley (še), also "capacity"
    "ziz2": "𒀾",  # Emmer wheat (zíz)
    "i3_gis": "𒉌 𒄑",  # Sesame oil (ì-giš)
    "kas": "𒁉",  # Beer (kaš / bi) - Standard vessel sign
    # Land & Livestock
    "a_sa": "𒀀 𒊮",  # Field (a-šà), also "surface"
    "kiri6": "𒊬",  # Orchard/Garden (kiri6)
    "gu4": "𒄞",  # Ox (gu4)
    "udu": "𒇻",  # Sheep (udu)
    # Textiles & Fibers
    "siki": "𒋠",  # Wool (siki)
    "gada": "𒃰",  # Linen (gada)
    "siki_gi": "𒋠 𒄀",  # Native/Standard wool (siki-gi)
    # Fruits & Provisions
    "zu2_lum": "𒍪 𒈝",  # Dates (zú-lum)
    "ges_tin": "𒃾",  # Wine (geštin)
    "ga_ar3": "𒂵 𒄯",  # Cheese/Curd (ga-àr)
    "i3_nun": "𒉌 𒉣",  # Ghee/Butter (ì-nun)
    # Building & Resources
    "esir": "𒀀 𒂍",  # Bitumen (esir2 / A.E2) - The most standard form
    "ges": "𒄑",  # Wood/Beam (geš)
    "sig4": "𒋞",  # Brick (sig4)
    "na4": "𒉌",  # Stone (na4)
    # Personnel (Contextual)
    "lu2": "𒇽",  # Man/Worker (lú)
    "geme2": "𒊩",  # Female worker (gemé)
    "er3": "𒀴",  # Slave/Servant (er3)
    # Mathematical States (for Metrotable)
    "igi_nu": "𒅆 𒉡",  # Reciprocal not found (igi-nu)
    "igi_nu_du8": "𒅆 𒉡 𒂃",  # Reciprocal does not open (igi-nu-du8)
    "a_ra2": "𒀀 𒁺",  # Times (a-rá)
    
    # geometry
    # 1. Main Dimensions
    "sag": "𒊕",     # Front / Width (Literally "head", used for the frontal dimension or the width of a rectangle, thickness of walls or bricks).
    "dagal": "𒂼",   # Breadth / Width (Used for the extent of an object or surface).
    "sag_dagal": "𒊕 𒂼",
    # 2. Other Geometric Dimensions
    "us": "𒍑",      # Length / Long (It is the companion of SAG; in a rectangle, UŠ is the long side and SAG the short side).
    "sukud": "𒊩𒆪",  # Height (Used for the height of a wall or a tower).
    "bur": "𒌋",      # Depth (bùr) (In cuneiform:  𒁓)?  (Common in texts about excavation of canals or wells).
    "da": "𒁕",      # Side / Flank (Refers to the edge or lateral line of a figure).
    "gid": "𒁍",    # Length / Extension (Means "long" or "stretch", sometimes used as a linear measure).
    "ki_la2": "𒆠 𒆷", # "Excavation area" or "Volume." It is the technical term for the hole left in the ground.
    "sahar": "𒅖",   # "Earth / Dust." It is the determinant that almost always accompanies excavation volumes.
    "gam": "𒃵",     # Depth, curvature (GAM)
}

# Determinatives
DETERM = {
    "gi": "𒄀",    # Reed, Crucial for alternative length measurements (*gi* = 1/2 ninda).
    "ku3": "𒆬",   #Precious/Pure. It precedes metals.
    "dug": "𒂁",   #Vessel. It precedes liquids."
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
    "MA-NA": "𒈠 𒈾",
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
    "danna": "𒆜 𒁍",
    "gan": "𒃷",
    "gin": "𒂆",
    "gu": "𒄘",
    "gur": "𒄥",
    "kus": "𒌑",
    "mana": "𒈠 𒈾",
    "ninda": "𒃻",
    "sar": "𒊬",
    "se": "𒊺",
    "sila": "𒋡",
    "susi": "𒋗 𒋛",
    "us": "𒍑",
    "u": "𒌋",
    "bur": "𒌋",
    "buru": "𒐴",
    "dis": "𒁹",
    "ese": "𒑘",
    "iku": "𒀸",
} | UNIT_LOGOGRAMS

#: For colophons
MAP_ADMIN = {
    "su_ningin_gal": "𒋗 𒆸 𒃲",  # Total if sections
    "mu_sid_bi": "𒈬 𒋃 𒁉",  # Your number of lines
    "dub": "𒁾",  # Clay tablet
    "mu-kux": "𒈬 𒁺",  # mu-kux(DU) Delivery. Indicates goods that enter the institution or warehouse.
    "zi-ga": " 𒍣 𒂵",  # Expense. Indicates what has been withdrawn or spent from the inventory.
    "la-ia": " 𒇲 𒉌",  # Deficit. (lá-ia3) It was used to indicate what was missing in an account or what an official still had to deliver.
    "nig-ka": "𒃻 𒅗",  # Balance, the general term for the "account statement" or the process of auditing a ledger.
    "iti": "𒌗",  # Date. Month / Time of creation.
    "dub-sar": "𒁾 𒊬",  # Scribe
    "nu_til": "𒉡 𒌀",  # Not finished. 
    "ba_til": "𒁀 𒌀",  # Finished.
    "mu": "𒈬", # Used for "year" in administrative dating contexts.
    "su_ti_a": "𒋗 𒋾 𒀀",  # Received (šu-ti-a)
    "ib2_tag4": "𒅁 𒋳",  # Remainder / Balance (ib2-tag4)
    "sa10": "𒌓",  # Price / Equivalent (sa10 / sham)"
}

#: Transliteration to cuneiform dictionary
translit_dict = {
    "1/2": "𒈦",
    "1/3": "𒑚",
    "1(aš)": "𒀸",
    "1(ban2)": "𒑏",
    "1(barig)": "𒁹",
    "1(bur3)": "𒌋",
    "1(bur’u)": "𒐴",
    "1(diš)": "𒁹",
    "1(eše3)": "𒑘",
    "1(geš2)": "𒐕",
    "1(geš’u)": "𒐞",
    "1(iku)": "𒀸",
    "1(šar2)": "𒊹",
    "1(šargal)gal": "𒊹 𒃲",
    "1(šar’u)": "𒐬",
    "1(u)": "𒌋",
    "1(ubu)": "𒀹",  # ?
    "2/3": "𒑛",
    "2(aš)": "𒐀",
    "2(ban2)": "𒑐",
    "2(barig)": "𒑖",
    "2(bur3)": "𒎙",
    "2(bur’u)": "𒐵",
    "2(diš)": "𒐖",
    "2(eše3)": "𒑙",
    "2(geš2)": "𒐖",
    "2(geš’u)": "𒐟",
    "2(iku)": "𒐀",
    "2(šar2)": "𒐣",
    "2(šar’u)": "𒐭",
    "2(u)": "𒎙",
    "3(aš)": "𒐁",
    "3(ban2)": "𒑑",
    "3(barig)": "𒑗",
    "3(bur3)": "𒌍",
    "3(bur’u)": "𒐶",
    "3(diš)": "𒐈",
    "3(geš2)": "𒐗",
    "3(geš’u)": "𒐠",
    "3(iku)": "𒐁",
    "3(šar2)": "𒐤",
    "3(šar’u)": "𒐮",
    "3(u)": "𒌍",
    "4(aš)": "𒐂",
    "4(ban2)": "𒑒",
    "4(barig)": "𒐉",
    "4(bur3)": "𒐏",
    "4(bur’u)": "𒐸",
    "4(diš)": "𒐉",
    "4(diš)gal2": "𒐉 𒅅", # ??? esto es para 1/4 con igi delante
    "4(geš2)": "𒐘",
    "4(geš’u)": "𒐡",
    "4(iku)": "𒐂",
    "4(šar2)": "𒐦",
    "4(šar’u)": "𒐰",
    "4(u)": "𒐏",
    "5/6": "𒑜",
    "5(aš)": "𒐃",
    "5(ban2)": "𒑔",
    "5(bur3)": "𒐐",
    "5(bur’u)": "𒐹",
    "5(diš)": "𒐊",
    "5(geš2)": "𒐙",
    "5(geš’u)": "𒐢",
    "5(iku)": "𒐃",
    "5(šar2)": "𒐧",
    "5(šar’u)": "𒐱",
    "5(u)": "𒐐",
    "6(aš)": "𒐄",
    "6(bur3)": "𒐑",
    "6(diš)": "𒐋",
    "6(diš)gal2": "𒐋 𒅅", # ??? esto es para 1/6 con igi delante
    "6(geš2)": "𒐚",
    "6(šar2)": "𒐨",
    "7(aš)": "𒐅",
    "7(bur3)": "𒐒",
    "7(diš)": "𒐌",
    "7(geš2)": "𒐛",
    "7(šar2)": "𒐩",
    "8(aš)": "𒐆",
    "8(bur3)": "𒐓",
    "8(diš)": "𒐍",
    "8(geš2)": "𒐜",
    "8(šar2)": "𒐪",
    "9(aš)": "𒐇",
    "9(bur3)": "𒐔",
    "9(diš)": "𒐎",
    "9(geš2)": "𒐝",
    "9(šar2)": "𒐫",
    "a-ša3": "𒀀 𒊮",
    "danna": "𒆜 𒁍",
    "gal2": "𒅅",
    "GAN2": "𒃷",
    "gin2": "𒂆",
    "gu2": "𒄘",
    "gur": "𒄥",
    "igi": "𒅆",
    "ku3-babbar": "𒆬 𒌓",
    "kuš3": "𒌑",
    "ma-na": "𒈠 𒈾",
    "ninda": "𒃻",
    "sar": "𒊬",
    "še": "𒊺",
    "sila3": "𒋡",
    "šu-nu-tag": "𒋗 𒉡 𒋳", # ?
    "šu-si": "𒋗 𒋛",
    "UŠ": "𒍑",
}


CUNEIFORM_LABEL_GLYPHS = "𒉆 𒁾 𒊬"
CUNEIFORM_LABEL_HEX = r'\symbol{"12240}\symbol{"1207E}\symbol{"122AC}'

TIMES_LABEL = "𒀀 𒁺"
IGI_NU = "𒅆 𒉡" # igi nu-ub-tuku
TINI_SPACE = " "
