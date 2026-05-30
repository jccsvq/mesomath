#!/bin/bash
# Script to rebuild the chronological database
set -e  # Stop script on any error
set -u  # Stop if a variable is not defined

echo "--- Starting reconstruction process ---"

# Initial cleaning
rm -f processed/tempo.csv pdchron71.csv

# 1. Normalization
python normalize_pd.py

# 2. Initial cleaning
cat processed/K*.csv processed/seleuc*.csv > processed/tempo.csv

# 3. Astronomical processing
python process_allkings.py > pdchron71.csv

# 4. Database Construction
# We assume that createDB.sql creates the .db or .sql file
sqlite3 < createDB.sql 
mv mesotimes.sql sql/

# 5. Final build 
echo "--- Finalizing process ---"
cd ../..
make clean all
cd -

echo "Database successfully updated!"
