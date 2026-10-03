# ACIT4420 Assignment II

## Smart Fitness Session Analyzer

This project extends the Smart Fitness Session Analyzer from Assignment I.

The program reads participant and fitness session data from CSV files, validates the data, analyzes valid observations, classifies fitness sessions, and writes the results to output files.

## Project structure

- `main.py` - runs the application
- `tests.py` - contains tests for validation, file loading and analysis
- `data/` - contains the provided CSV input files
- `fitness_analyzer/` - contains the program modules
- `output/` - contains generated report files

## Input files

The program uses the following provided files:

- `data/participants.csv`
- `data/fitness_sessions.csv`
- `data/fitness_sessions_invalid.csv`

The original CSV files are not modified.

## Validation

The program validates:

- participant IDs
- session IDs
- missing values
- numerical values
- allowed measurement ranges
- unknown participants
- unexpected CSV row lengths
- signal quality

Measurements with a signal quality below `0.5` are rejected as poor-quality data.

Rejected rows are recorded with the source file, row number, field and reason.

## Running the program

From the project root, run:

```bash
python main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv data/fitness_sessions_invalid.csv --output output
```
