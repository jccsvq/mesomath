PRAGMA synchronous = OFF;
PRAGMA journal_mode = MEMORY;

-- 1. Total cleaning (Idempotence)
DROP VIEW IF EXISTS meton_cycle;
DROP VIEW IF EXISTS meton_cycle_century;
DROP VIEW IF EXISTS king_period_start;
DROP VIEW IF EXISTS kishecl;
DROP TABLE IF EXISTS kingdates;
DROP TABLE IF EXISTS kings;
DROP TABLE IF EXISTS kishlun;
DROP TABLE IF EXISTS kishsol;

-- 2. Table Structure (Explicit)
CREATE TABLE kings (
    ID TEXT,
    king_code TEXT PRIMARY KEY,
    king TEXT
);

CREATE TABLE kingdates (
    ID INTEGER PRIMARY KEY,
    king_code TEXT,
    king_year INTEGER,
    king_month INTEGER,
    jyear INTEGER,
    jmonth INTEGER,
    jday INTEGER,
    jdat00h REAL,
    moon_age_offset INTEGER,
    FOREIGN KEY(king_code) REFERENCES kings(king_code)
);

-- 3. Importation (Now with guaranteed scheme)
.mode csv
.import orig/kings.csv kings --skip 1
.import pdchron71.csv kingdates --skip 1

-- 4. Indexes
CREATE INDEX idx_jd ON kingdates(JDat00h);
CREATE INDEX idx_king_date ON kingdates(king_code, king_year, king_month);

-- 5. Views
CREATE VIEW king_period_start AS 
WITH RankedDates AS (
    SELECT 
        king_code, jyear, jmonth, jday,
        ROW_NUMBER() OVER (PARTITION BY king_code ORDER BY jyear, jmonth, jday) as rn
    FROM kingdates
)
SELECT k.king_code, k.king, rd.jyear, rd.jmonth, rd.jday
FROM kings k
JOIN RankedDates rd ON k.king_code = rd.king_code
WHERE rd.rn = 1;

CREATE VIEW meton_cycle AS
    SELECT jyear,
           (((jyear + 472) % 19 + 19) % 19) + 1 AS meton_cycle_number,
           COUNT(*) AS months_in_year
      FROM kingdates
     GROUP BY jyear
    HAVING months_in_year = 13
     ORDER BY jyear ASC;

CREATE VIEW meton_cycle_century AS
    SELECT (jyear / 100) * 100 AS century,
           meton_cycle_number,
           COUNT(*) AS cantidad
      FROM (
              SELECT jyear,
                     (((jyear + 472) % 19 + 19) % 19) + 1 AS meton_cycle_number
                FROM kingdates
               WHERE jyear IN (SELECT jyear FROM meton_cycle)
           )
     GROUP BY century, meton_cycle_number
     ORDER BY century ASC, meton_cycle_number ASC;

-- 6. Historical Periods Table
CREATE TABLE periods (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER NOT NULL,
    category TEXT, -- 'Dynasty', 'Climate', 'Regnal', etc.
    description TEXT
);

CREATE INDEX idx_periods_years ON periods(start_year, end_year);

-- Initial data
INSERT INTO periods (name, start_year, end_year, category, description) VALUES
('Achaemenid Empire', -549, -329, 'Dynasty', 'Achaemenid Persian Empire'),
-- Neobabylonian Period
('Nabopolassar', -625, -604, 'Regnal', 'End in 605 BC'),
('Nebuchadnezzar II', -604, -561, 'Regnal', '605 BC to 562 BC'),
('Amel-Marduk', -561, -559, 'Regnal', '562 BC to 560 BC'),
('Nergal-sharezer', -559, -555, 'Regnal', '560 BC to 556 BC'),
('Labashi-Marduk', -555, -555, 'Regnal', 'Reigned only a few months in 556 BC'),
('Nabonidus', -555, -538, 'Regnal', '556 BC to 539 BC (Fall of Babylon)'),
-- Persian Kings (as Kings of Babylon)
('Cyrus II', -538, -529, 'Regnal', '539 BC to 530 BC'),
('Cambyses II', -529, -521, 'Regnal', '530 BC to 522 BC'),
('Bardiya', -521, -521, 'Regnal', 'Smerdis (522 BC)'),
('Darius I', -521, -485, 'Regnal', '522 BC to 486 BC'),
('Xerxes I', -485, -464, 'Regnal', '486 BC to 465 BC'),
('Artaxerxes I', -464, -423, 'Regnal', '465 BC to 424 BC'),
('Darius II', -423, -404, 'Regnal', '424 BC to 405 BC'),
('Artaxerxes II', -404, -358, 'Regnal', '405 BC to 359 BC'),
('Artaxerxes III', -358, -337, 'Regnal', '359 BC to 338 BC'),
('Arses', -337, -335, 'Regnal', '338 BC to 336 BC'),
('Darius III', -335, -330, 'Regnal', '336 BC to 331 BC'),
-- Macedonian Kings
('Macedonian Era', -330, -311, 'Dynasty',''),
('Alexander III', -330, -322, 'Regnal', 'Alexander the Great'),
('Philip III Arrhidaeus', -322, -316, 'Regnal', '323 BC to 317 BC'),
('Alexander IV', -316, -311, 'Regnal', '317 BC to 312 BC'),
-- Seleucid Era (SE)
('Seleucid Era', -311, 76, 'Dynasty', 'Continuous count starting 312/311 BC'),
('Seleucus I Nicator', -304, -280, 'Regnal', 'Satrap from -311, King from -304'),
('Antiochus I Soter', -280, -260, 'Regnal', 'Co-regent from -291'),
('Antiochus II Theos', -260, -245, 'Regnal', '261 BC to 246 BC'),
('Seleucus II Callinicus', -245, -224, 'Regnal', '246 BC to 225 BC'),
('Seleucus III Ceraunus', -224, -222, 'Regnal', '225 BC to 223 BC'),
('Antiochus III the Great', -222, -186, 'Regnal', '223 BC to 187 BC'),
-- Parthian (Arsacid) Kings (Main Babylonian Sequence)
('Parthian (Arsacid) Era', -170, 228, 'Dynasty',''),
('Mithradates I', -170, -137, 'Regnal', 'Arsacid conquest of Babylon'),
('Phraates II', -137, -126, 'Regnal', '138 BC to 127 BC'),
('Artabanus II', -126, -121, 'Regnal', '127 BC to 122 BC'),
('Mithradates II', -121, -87, 'Regnal', '122 BC to 88 BC'),
('Gotarzes I', -90, -79, 'Regnal', 'Rebel/King during Arsacid dark age'),
('Orodes I', -79, -74, 'Regnal', '80 BC to 75 BC'),
('Sinatruces', -74, -69, 'Regnal', '75 BC to 70 BC'),
('Phraates III', -69, -56, 'Regnal', '70 BC to 57 BC'),
('Mithradates III', -56, -53, 'Regnal', '57 BC to 54 BC'),
('Orodes II', -56, -36, 'Regnal', 'Defeated Crassus at Carrhae'),
('Phraates IV', -36, -1, 'Regnal', '37 BC to 2 BC'),
('Phraataces', -1, 4, 'Regnal', 'Phraates V'),
('Orodes III', 4, 6, 'Regnal', 'AD 4 to AD 6'),
('Vonones I', 6, 11, 'Regnal', 'AD 6 to AD 12'),
('Artabanus III', 11, 38, 'Regnal', 'AD 12 to AD 38'),
('Gotarzes II', 38, 51, 'Regnal', 'AD 38 to AD 51. Rivalry with Vardanes I'),
('Vardanes I', 39, 47, 'Regnal', 'AD 39 to AD 47. Controlled Babylon and Seleucia'),
('Meherdates', 49, 49, 'Regnal', 'Roman-backed pretender (AD 49)'),
('Vonones II', 51, 51, 'Regnal', 'Reigned only a few months in AD 51'),
('Vologases I', 51, 78, 'Regnal', 'AD 51 to AD 78. Major cultural Iranian revival'),
('Pacorus II', 78, 110, 'Regnal', 'AD 78 to AD 110. Period of stability in Babylon'),
('Artabanus IV', 80, 81, 'Regnal', 'Rival king in Babylon and Seleucia'),
('Vologases III', 105, 147, 'Regnal', 'AD 105 to AD 147. Often identified as Vologases II in older lists'),
('Osroes I', 109, 129, 'Regnal', 'Controlled Mesopotamia; conflict with Trajan'),
('Parthamaspates', 116, 117, 'Regnal', 'Roman puppet king in Ctesiphon'),
('Mithradates V', 129, 140, 'Regnal', 'Successor of Osroes I in Mesopotamia'),
('Vologases IV', 147, 191, 'Regnal', 'Unification of the kingdom; AD 147 to AD 191'),
('Vologases V', 191, 208, 'Regnal', 'AD 191 to AD 208. Severan wars impact'),
('Vologases VI', 208, 228, 'Regnal', 'Maintained control in parts of Mesopotamia until the Sassanid conquest'),
('Artabanus V', 213, 224, 'Regnal', 'Last great Parthian king; defeated by Ardashir I'),
('Artavasdes', 224, 228, 'Regnal', 'Last Arsacid resistance in Mesopotamia and Media');

-- 7. Planetary events
-- Table of astronomical/planetary observations
CREATE TABLE planetary_events (
    id INTEGER PRIMARY KEY,
    jd REAL NOT NULL,            -- El ancla temporal
    planet TEXT NOT NULL,        -- (Jupiter, Mars, Saturn, Venus, Mercury)
    event_type TEXT NOT NULL,    -- (Heliacal Rising, Stationary, Opposition, etc.)
    constellation TEXT,          -- La posición en el zodiaco/constelación
    source_reference TEXT,       -- Ejemplo: "AD-II, p.150, obv. 12" (Tablilla, cara, línea)
    reliability_score INTEGER,   -- 1-5 (Para marcar eventos confirmados vs. calculados)
    description TEXT
);

CREATE INDEX idx_planet_jd ON planetary_events(jd, planet);
CREATE INDEX idx_planet_type ON planetary_events(planet, event_type);

-- Lunar eclipses at Kish
-- Optimized Lunar Table
CREATE TABLE kishlun (
    Year  INTEGER,
    Month INTEGER,
    Day   INTEGER,
    Type  TEXT,
    Mag   TEXT,
    PRIMARY KEY (Year, Month, Day) -- Clave primaria compuesta
) WITHOUT ROWID;

.mode csv
.import Kish_lun.csv kishlun --skip 1

-- Solar eclipses at Kish
-- Optimized Solar Table
CREATE TABLE kishsol (
    Year  INTEGER,
    Month INTEGER,
    Day   INTEGER,
    Type  TEXT,
    Mag   TEXT,
    PRIMARY KEY (Year, Month, Day)
) WITHOUT ROWID;

.mode csv
.import Kish_sol.csv kishsol --skip 1

-- Optimized view
CREATE VIEW kishecl AS
    SELECT year, month, day, 'Lunar ' || Type || ' Eclipse' AS Type, Mag
    FROM kishlun
    UNION ALL
    SELECT year, month, day, 'Solar ' || Type || ' Eclipse' AS Type, Mag
    FROM kishsol;

-- Reset security pragmas
PRAGMA synchronous = NORMAL;
-- 8. Exportation
.out mesotimes.sql
.dump
.quit
