import csv
from juliandate import from_julian as to_JD

def moon_age(jd: float, offset: float = 0.0) -> int:
    """
    Days elapsed since last New Moon

    :param jd: Julian Day
    :type jd: float
    :param offset: Allows adjustment to sunset, previous sunset, etc., defaults to 0.0
    :type offset: float, optional
    :return: Moon age in days
    :rtype: int
    """
    from math import floor
    
    # Verify that jd is in the range of P&P 1971 chronology
    assert jd >= 1492870.5 and jd <= 1748872.5, "Julian Day out of range of P&P 1971 chronology"

    # Lunar Month (according to Five Millenium Cannon of Solar Eclipses)
    M = 29.530598917100200000
    # M^-1
    M_inv = 0.033863180448880300
    moon0 = -83017.290642228700000000
    _ = moon0 + (jd + offset) * M_inv
    moon = _ - floor(_)
    age = M * moon
    return round(age)

with open('processed/tempo.csv') as csvfile:
    reader = csv.reader(csvfile)
    line = 0
    print("ID, king_code, king_year, king_month, jyear, jmonth, jday, JDat00h, moon_age")
    for row in reader:
        #jd = to_JD(int(row[3]), int(row[4]), int(row[5]))
        #print(', '.join(row) + f", {str(jd)}")

        jd = to_JD(int(row[3]), int(row[4]), int(row[5]), 0, 0, 0)
        print(f"{line}," + ",".join(row) + f",{str(jd)},{str(moon_age(jd))}")
            
        line += 1
