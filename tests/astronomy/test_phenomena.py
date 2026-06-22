import pytest
from mesotimes.astronomy.stars import BabStar
from pymeeus.Epoch import Epoch
from mesotimes.constants import BABYLONIAN_STAR_CATALOG

# Susa coordinates or identifier expected by your API
CITY_SUSA = "Susa"
YEAR_TEST = -378


@pytest.mark.parametrize(
    "star_name, expected_heliacal, expected_acronychal",
    [
        ("Sirius", (-378, 7, 23), (-378, 1, 15)),
        ("Regulus", (-378, 8, 9), (-378, 2, 1)),
        ("Vega", (-378, 11, 23), (-378, 5, 21)),
        ("Altair", (-378, 12, 20), (-378, 6, 19)),
    ],
)
def test_star_phenomena_regression(star_name, expected_heliacal, expected_acronychal):
    """Verify that calculated dates for key stars match verified historical baselines."""
    star = BabStar.from_catalog(star_name)
    start_month = BABYLONIAN_STAR_CATALOG[star_name].get("start_month", 1)
    epoch_init = Epoch(YEAR_TEST, start_month, 1)

    # --- HELIACAL RISING WITH RETRY LOGIC ---
    h_event = None
    try:
        h_event = star.heliacal_rising(epoch_init, city=CITY_SUSA, max_days=366)
    except Exception:
        # If already visible or error, shift 6 months just like in search_phenomena
        retry_month = 7 if start_month == 1 else ((start_month + 5) % 12) + 1
        epoch_retry = Epoch(YEAR_TEST, retry_month, 1)
        h_event = star.heliacal_rising(epoch_retry, city=CITY_SUSA, max_days=366)

    # Clean float tuple to integer (Year, Month, Day)
    h_date = h_event.get_date()
    actual_heliacal = (int(h_date[0]), int(h_date[1]), int(h_date[2]))
    assert actual_heliacal == expected_heliacal

    # --- ACRONYCHAL RISING WITH RETRY LOGIC ---
    a_event = None
    try:
        a_event = star.acronychal_rising(epoch_init, city=CITY_SUSA, max_days=366)
    except Exception:
        retry_month = 7 if start_month == 1 else ((start_month + 5) % 12) + 1
        epoch_retry = Epoch(YEAR_TEST, retry_month, 1)
        a_event = star.acronychal_rising(epoch_retry, city=CITY_SUSA, max_days=366)

    a_date = a_event.get_date()
    actual_acronychal = (int(a_date[0]), int(a_date[1]), int(a_date[2]))
    assert actual_acronychal == expected_acronychal


def test_extreme_horizon_exceptions():
    """Ensure circumpolar or invisible stars raise expected geometric errors gracefully."""
    # Dubhe is circumpolar and should raise an Initialization Error (already visible)
    dubhe = BabStar.from_catalog("Dubhe")
    start_month_dubhe = BABYLONIAN_STAR_CATALOG["Dubhe"].get("start_month", 1)
    epoch_dubhe = Epoch(YEAR_TEST, start_month_dubhe, 1)
    
    with pytest.raises(ValueError, match="ALREADY VISIBLE"):
        dubhe.heliacal_rising(epoch_dubhe, city=CITY_SUSA, max_days=366)

    # Canopus is below visibility limits or doesn't clear extinction window (RuntimeError)
    canopus = BabStar.from_catalog("Canopus")
    epoch_canopus = Epoch(YEAR_TEST, 1, 1)
    
    with pytest.raises(RuntimeError, match="not found within 366 days"):
        canopus.heliacal_rising(epoch_canopus, city=CITY_SUSA, max_days=366)