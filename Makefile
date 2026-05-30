# Makefile for the Babylonian Chronology Laboratory
# Author: Researcher
# Goal: Automated reconstruction of the database from the SQL dump

# Configuration of directories and files
DB_DIR = src/mesotimes/db
DB_FILE = $(DB_DIR)/mesotimes.sqlite
SQL_FILE = db_data/PD71/sql/mesotimes.sql

# Phony targets: commands that do not generate a real file with their name
.PHONY: all clean rebuild verify

# By default, "make" builds the database if it is missing or if the SQL has changed
all: $(DB_FILE)

# Rule to build the database
$(DB_FILE): $(SQL_FILE)
	@mkdir -p $(DB_DIR)
	@echo "--- Building database from $(SQL_FILE)... ---"
	sqlite3 $(DB_FILE) < $(SQL_FILE)
	@echo "--- Database generated successfully: $(DB_FILE) ---"

# Verify that the data was loaded correctly
verify: $(DB_FILE)
	@echo "--- Verifying data integrity ---"
	@sqlite3 $(DB_FILE) "SELECT 'Total kings: ' || count(*) FROM kings;"
	@sqlite3 $(DB_FILE) "SELECT 'Total records: ' || count(*) FROM kingdates;"

# Clean the database (useful for a fresh start)
clean:
	@rm -f $(DB_FILE)
	@echo "--- Database deleted. ---"

# Full reconstruction (removes and recreates)
rebuild: clean all
