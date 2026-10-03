# Smart Fitness Session Analyzer

## Python Programming Assignment II - Option A

**Student:** Victoria Ludvigsen  
**Student number:** 421969

## Project description

This project implements Option A: Smart Fitness Session Analyzer.

The project extends Assignment I into a file-based application. The program reads participant profiles and fitness session observations from CSV files, validates the data, groups observations into sessions, analyzes usable measurements, classifies the sessions, and writes the results to output files.

Invalid rows are rejected without stopping the program and are recorded with the source file, row number, field, and reason.

## Project structure

```text
ACIT4420_Assignment2/
├── data/
│   ├── fitness_sessions.csv
│   ├── fitness_sessions_invalid.csv
│   └── participants.csv
├── fitness_analyzer/
│   ├── __init__.py
│   ├── analysis.py
│   ├── data_loader.py
│   ├── exceptions.py
│   ├── models.py
│   ├── reporting.py
│   └── validation.py
├── output/
│   ├── analysis_report.txt
│   ├── analysis_summary.csv
│   └── rejected_records.txt
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
└── tests.py
```

`main.py` runs the application and handles command-line arguments.  
`tests.py` contains tests for validation, file loading, classification, and output files.  
`data/` contains the instructor-supplied CSV files.  
`fitness_analyzer/` contains the application modules.  
`output/` contains the generated reports.

## Class design

### Participant

Stores the participant ID, name, and personal reference values for heart rate, skin response, and temperature.

### Observation

Represents one fitness observation containing timestamp, heart rate, skin response, temperature, activity level, and signal quality.

### Session

Contains a `Participant` object and a list of `Observation` objects.

### Analyzer

Analyzes the observations in a session, calculates summaries, compares measurements with participant reference values, detects recovery, classifies the session, and returns the result as a dictionary.

## Object-oriented design

### Composition

`Session` uses composition because it contains a `Participant` object and multiple `Observation` objects.

### Encapsulation

The participant's baseline heart rate is stored in the protected-style attribute `_baseline_heart_rate` and controlled through a property and setter.

### Custom exceptions

The project defines two custom exceptions:

- `InvalidIdentifierError`
- `InvalidRecordError`

They are used to report invalid identifiers and invalid CSV records.

## Input files

The program uses the instructor-supplied files:

- `data/participants.csv`
- `data/fitness_sessions.csv`
- `data/fitness_sessions_invalid.csv`

The original CSV files are not modified.

## Data and validation

Participant IDs must follow the format:

```text
P001
```

Session IDs must follow the format:

```text
FIT-2026-001
```

Regular expressions are used to validate both identifier formats.

The program also validates:

- missing required values
- unexpected row lengths
- failed numerical conversions
- unknown participant IDs
- timestamp values
- heart rate
- skin response
- temperature
- activity level
- signal quality

Valid measurement ranges are:

- timestamp: zero or greater
- heart rate: 35 to 205 bpm
- skin response: zero or greater
- temperature: 25 to 42 degrees Celsius
- activity level: 0 to 1
- signal quality: 0 to 1

Measurements with signal quality below `0.5` are rejected as poor-quality data. The minimum accepted signal quality of `0.5` is a project assumption.

Rejected records are written to `output/rejected_records.txt` with the source file, row number, field, and reason.

## Analysis and classification

For usable observations, the program calculates average, minimum, and maximum values for heart rate, activity level, temperature, and skin response.

Average heart rate, temperature, and skin response are also compared with the participant's reference values.

Classification rules:

- **Insufficient data:** fewer than three usable observations.
- **Resting:** average activity is below `0.25` and average heart rate is no more than `20 bpm` above baseline.
- **High activity:** average activity is at least `0.70` or average heart rate is at least `60 bpm` above baseline.
- **Moderate activity:** the session does not meet the other activity conditions.
- **Recovering:** activity and heart rate decrease after a clear activity peak and heart rate returns toward the participant's baseline value.

The exact classification thresholds are project assumptions.

## Error handling

The program handles file and data errors without stopping unnecessarily.

Examples include:

- `FileNotFoundError`
- `PermissionError`
- `csv.Error`
- `ValueError`
- `KeyError`
- `InvalidIdentifierError`
- `InvalidRecordError`

Invalid session rows are recorded and skipped so the remaining data can still be processed.

## Running the program

The project uses only the Python standard library.

Clone the repository:

```bash
git clone https://github.com/victorialudvigsen/ACIT4420_Assignment2.git
```

Move into the project folder:

```bash
cd ACIT4420_Assignment2
```

Run with the default file paths:

```bash
python main.py
```

The program can also be run with explicit command-line arguments:

```bash
python main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv data/fitness_sessions_invalid.csv --output output
```

If the system uses `python3`, replace `python` with `python3`.

## Output files

The program creates:

- `output/analysis_summary.csv`
- `output/analysis_report.txt`
- `output/rejected_records.txt`

The files are overwritten when the program is run again so repeated runs give predictable output.

## Running the tests

```bash
python tests.py
```

Expected result:

```text
Valid identifier test passed.
Invalid participant ID test passed.
Invalid session ID test passed.
Missing file test passed.
Boundary value test passed.
Invalid measurement test passed.
Valid session file test passed.
Invalid session file test passed.
Session classification test passed.
Output file test passed.

All tests passed.
```

## Requirements

The project uses only the Python standard library. No external packages are required.

## Known limitations

- Validation and classification depend on defined numerical thresholds.
- The minimum accepted signal quality of `0.5` is a project assumption.
- Recovery detection uses defined activity and heart-rate thresholds rather than a complete trend analysis.
- The application does not use external APIs, databases, graphical interfaces, or machine-learning models.
