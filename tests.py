from pathlib import Path
from fitness_analyzer.validation import (
    validate_participant_id,
    validate_session_id,
    validate_measurements
)
from fitness_analyzer.exceptions import (
    InvalidIdentifierError,
    InvalidRecordError
)
from fitness_analyzer.data_loader import (
    load_participants,
    load_sessions
)
from fitness_analyzer.analysis import Analyzer


def test_valid_identifiers():
    """Tests valid participant and session identifiers."""

    # Valid identifiers should be returned unchanged
    assert validate_participant_id("P001") == "P001"
    assert validate_session_id("FIT-2026-001") == "FIT-2026-001"

    print("Valid identifier test passed.")


def test_invalid_identifiers():
    """Tests that invalid identifiers raise the correct exception."""

    try:
        validate_participant_id("001")

    except InvalidIdentifierError:
        print("Invalid participant ID test passed.")

    else:
        assert False, "Invalid participant ID was accepted."

    try:
        validate_session_id("FIT-26-001")

    except InvalidIdentifierError:
        print("Invalid session ID test passed.")

    else:
        assert False, "Invalid session ID was accepted."


def test_missing_file():
    """Tests that a missing profile file raises FileNotFoundError."""

    try:
        load_participants("data/does_not_exist.csv")

    except FileNotFoundError:
        print("Missing file test passed.")

    else:
        assert False, "Missing file did not raise FileNotFoundError."


def test_boundary_values():
    """Tests valid measurement values at the allowed boundaries."""

    # Values exactly on the allowed limits should be accepted
    validate_measurements(
        timestamp=0,
        heart_rate=35,
        skin_response=0,
        temperature=25,
        activity_level=0,
        signal_quality=0.5
    )

    validate_measurements(
        timestamp=0,
        heart_rate=205,
        skin_response=0,
        temperature=42,
        activity_level=1,
        signal_quality=1
    )

    print("Boundary value test passed.")


def test_invalid_measurement():
    """Tests that an out-of-range measurement is rejected."""

    try:
        validate_measurements(
            timestamp=0,
            heart_rate=250,
            skin_response=1.0,
            temperature=32,
            activity_level=0.5,
            signal_quality=0.9
        )

    except InvalidRecordError:
        print("Invalid measurement test passed.")

    else:
        assert False, "Invalid heart rate was accepted."


def test_valid_session_file():
    """Tests loading and grouping of the valid fitness session file."""

    participants, rejected_participants, participant_rows = (
        load_participants("data/participants.csv")
    )

    sessions, rejected_records, accepted_rows = load_sessions(
        "data/fitness_sessions.csv",
        participants
    )

    # The official valid file contains five sessions
    assert len(sessions) == 5
    assert accepted_rows == 24
    assert len(rejected_records) == 5

    # FIT-2026-001 contains six usable observations
    assert len(sessions["FIT-2026-001"].observations) == 6

    print("Valid session file test passed.")


def test_invalid_session_file():
    """Tests that invalid CSV rows are rejected without stopping the program."""

    participants, rejected_participants, participant_rows = (
        load_participants("data/participants.csv")
    )

    sessions, rejected_records, accepted_rows = load_sessions(
        "data/fitness_sessions_invalid.csv",
        participants
    )

    # Only one row in the intentionally invalid file should be accepted
    assert accepted_rows == 1
    assert len(rejected_records) == 10

    # Two session IDs are created from valid rows
    assert len(sessions) == 2

    # FIT-2026-101 contains the one accepted observation
    assert len(sessions["FIT-2026-101"].observations) == 1

    print("Invalid session file test passed.")


def test_session_classifications():
    """Tests the expected classifications from the valid session file."""

    participants, rejected_participants, participant_rows = (
        load_participants("data/participants.csv")
    )

    sessions, rejected_records, accepted_rows = load_sessions(
        "data/fitness_sessions.csv",
        participants
    )

    # Check the expected classification for each session
    assert Analyzer(sessions["FIT-2026-001"]).classify_session() == "resting"
    assert Analyzer(sessions["FIT-2026-002"]).classify_session() == "moderate activity"
    assert Analyzer(sessions["FIT-2026-003"]).classify_session() == "high activity"
    assert Analyzer(sessions["FIT-2026-004"]).classify_session() == "recovering"
    assert Analyzer(sessions["FIT-2026-005"]).classify_session() == "insufficient data"

    print("Session classification test passed.")


def test_output_files_exist():
    """Tests that the required output files have been created."""

    output_path = Path("output")

    # Check that all required output files exist
    assert (output_path / "analysis_summary.csv").exists()
    assert (output_path / "analysis_report.txt").exists()
    assert (output_path / "rejected_records.txt").exists()

    print("Output file test passed.")


if __name__ == "__main__":
    test_valid_identifiers()
    test_invalid_identifiers()
    test_missing_file()
    test_boundary_values()
    test_invalid_measurement()
    test_valid_session_file()
    test_invalid_session_file()
    test_session_classifications()
    test_output_files_exist()

    print("\nAll tests passed.")