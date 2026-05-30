import csv
import re

# Mapping of columns to Babylonian months
MONTH_MAP = {
    "NIS": 1,
    "AIA": 2,
    "SIM": 3,
    "DUZ": 4,
    "ABU": 5,
    "ULU": 6,
    "UII": 6.5,  # Leap month
    "TAS": 7,
    "ARA": 8,
    "KIS": 9,
    "TEB": 10,
    "SHA": 11,
    "ADD": 12,
    "AII": 12.5,  # Leap month
}


def parse_date(date_str):
    """Convierte 'm/d' a (m, d)."""
    match = re.match(r"(\d+)/(\d+)", date_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None


def process_pd_table(input_csv, output_csv, king_code, BCE=True):
    with open(input_csv, "r") as f_in, open(output_csv, "w", newline="") as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)

        # Header for  DB
        # writer.writerow(['king_code', 'king_year', 'king_month', 'jyear', 'jmonth', 'jday'])

        for row in reader:
            king_year = row["YEAR"]
            # The base B.C. year (we assume that the first month is of this year)
            current_jyear = int(row["B.C."])

            for col_name, value in row.items():
                if col_name in ["YEAR", "B.C.", "Y1", "Y2"]:
                    # If we find an explicit year column, we update the Julian year
                    if value and value.isdigit():
                        current_jyear = int(value)
                    continue

                if value and "/" in value:
                    month_num = MONTH_MAP.get(col_name)
                    m, d = parse_date(value)

                    # Writing of the normalized row
                    if BCE:
                        writer.writerow(
                            [king_code, king_year, month_num, 1 - current_jyear, m, d]
                        )
                    else:
                        writer.writerow(
                            [king_code, king_year, month_num, current_jyear, m, d]
                        )


if __name__ == "__main__":
    process_pd_table("orig/K001.csv", "processed/K001.csv", "k001")
    process_pd_table("orig/K002.csv", "processed/K002.csv", "k002")
    process_pd_table("orig/K003.csv", "processed/K003.csv", "k003")
    process_pd_table("orig/K004.csv", "processed/K004.csv", "k004")
    process_pd_table("orig/K005.csv", "processed/K005.csv", "k005")
    process_pd_table("orig/K006.csv", "processed/K006.csv", "k006")
    process_pd_table("orig/K007.csv", "processed/K007.csv", "k007")
    process_pd_table("orig/K008.csv", "processed/K008.csv", "k008")
    process_pd_table("orig/K009.csv", "processed/K009.csv", "k009")
    process_pd_table("orig/K010.csv", "processed/K010.csv", "k010")
    process_pd_table("orig/K011.csv", "processed/K011.csv", "k011")
    process_pd_table("orig/K012.csv", "processed/K012.csv", "k012")
    process_pd_table("orig/K013.csv", "processed/K013.csv", "k013")
    process_pd_table("orig/K014.csv", "processed/K014.csv", "k014")
    process_pd_table("orig/K015.csv", "processed/K015.csv", "k015")
    process_pd_table("orig/K016.csv", "processed/K016.csv", "k016")
    process_pd_table("orig/K017.csv", "processed/K017.csv", "k017")
    process_pd_table("orig/K018.csv", "processed/K018.csv", "k018")
    process_pd_table("orig/seleuc1.csv", "processed/seleuc1.csv", "k019")
    process_pd_table("orig/seleuc2.csv", "processed/seleuc2.csv", "k019", False)
