import csv
from pathlib import Path

from .models import Participant, Observation, Session
from .exceptions import InvalidIdentifierError, InvalidRecordError
from .validation import (
    validate_participant_id,
    validate_session_id,
    validate_measurements,
    convert_to_int,
    convert_to_float
)

def create_rejected_record(filename, row_number, field, reason):
    """Creates a structured description of a rejected CSV row."""

    return {
        "source_file": filename,
        "row_number": row_number,
        "field": field,
        "reason": reason
    }


def load_participants(file_path):
    """Loads participant profiles and records rejected CSV rows."""

    participants = {}
    rejected_records = []
    accepted_rows = 0

    path = Path(file_path)

    required_fields = [
        "participant_id",
        "name",
        "baseline_heart_rate",
        "baseline_skin_response",
        "baseline_temperature"
    ]

    with open(
        path,
        mode="r",
        encoding="utf-8",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        # Data rows start on row 2 because row 1 contains the headings
        for row_number, row in enumerate(reader, start=2):

            # Extra or missing columns indicate an unexpected row length
            if None in row or any(value is None for value in row.values()):
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        "row",
                        "Unexpected number of fields."
                    )
                )
                continue

            # Check that all required fields contain a value
            missing_field = None

            for field in required_fields:
                if field not in row or row[field] == "":
                    missing_field = field
                    break

            if missing_field is not None:
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        missing_field,
                        "Required value is missing."
                    )
                )
                continue

            participant_id = row["participant_id"]

            # Validate the participant ID format
            try:
                validate_participant_id(participant_id)

            except InvalidIdentifierError as error:
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        "participant_id",
                        str(error)
                    )
                )
                continue

            # Convert and validate the participant reference values
            try:
                baseline_heart_rate = convert_to_int(
                    row["baseline_heart_rate"],
                    "baseline_heart_rate"
                )

                baseline_skin_response = convert_to_float(
                    row["baseline_skin_response"],
                    "baseline_skin_response"
                )

                baseline_temperature = convert_to_float(
                    row["baseline_temperature"],
                    "baseline_temperature"
                )

                if not 35 <= baseline_heart_rate <= 205:
                    raise InvalidRecordError(
                        "Baseline heart rate must be between 35 and 205 bpm.",
                        field="baseline_heart_rate"
                    )

                if baseline_skin_response < 0:
                    raise InvalidRecordError(
                        "Baseline skin response cannot be negative.",
                        field="baseline_skin_response"
                    )

                if not 25 <= baseline_temperature <= 42:
                    raise InvalidRecordError(
                        "Baseline temperature must be between 25 and 42 degrees Celsius.",
                        field="baseline_temperature"
                    )

            except InvalidRecordError as error:
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        error.field,
                        str(error)
                    )
                )
                continue

            # Create the participant only after the row is validated
            participant = Participant(
                participant_id=participant_id,
                name=row["name"],
                baseline_heart_rate=baseline_heart_rate,
                baseline_skin_response=baseline_skin_response,
                baseline_temperature=baseline_temperature
            )

            participants[participant_id] = participant
            accepted_rows += 1

    return participants, rejected_records, accepted_rows


def load_sessions(file_path, participants):
    """Loads fitness sessions and records rejected CSV rows."""

    sessions = {}
    rejected_records = []
    accepted_rows = 0

    path = Path(file_path)

    with open(
        path,
        mode="r",
        encoding="utf-8",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        # CSV row 1 contains the column headings, so data starts on row 2
        for row_number, row in enumerate(reader, start=2):

            # Extra or missing columns indicate an unexpected row length
            if None in row or any(value is None for value in row.values()):
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        "row",
                        "Unexpected number of fields."
                    )
                )
                continue

            session_id = row["session_id"]
            participant_id = row["participant_id"]

            # Validate the session ID format
            try:
                validate_session_id(session_id)

            except InvalidIdentifierError as error:
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        "session_id",
                        str(error)
                    )
                )
                continue

            # Validate the participant ID format
            try:
                validate_participant_id(participant_id)

            except InvalidIdentifierError as error:
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        "participant_id",
                        str(error)
                    )
                )
                continue

            # The participant must exist in participants.csv
            try:
                participant = participants[participant_id]

            except KeyError:
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        "participant_id",
                        f"Unknown participant ID: {participant_id}"
                    )
                )
                continue

            # Create the session when its ID appears for the first time
            if session_id not in sessions:
                sessions[session_id] = Session(
                    session_id,
                    participant
                )

            # Convert CSV text values and validate the measurements
            try:
                timestamp = convert_to_int(
                    row["timestamp"],
                    "timestamp"
                )

                heart_rate = convert_to_int(
                    row["heart_rate"],
                    "heart_rate"
                )

                skin_response = convert_to_float(
                    row["skin_response"],
                    "skin_response"
                )

                temperature = convert_to_float(
                    row["temperature"],
                    "temperature"
                )

                activity_level = convert_to_float(
                    row["activity_level"],
                    "activity_level"
                )

                signal_quality = convert_to_float(
                    row["signal_quality"],
                    "signal_quality"
                )

                validate_measurements(
                    timestamp,
                    heart_rate,
                    skin_response,
                    temperature,
                    activity_level,
                    signal_quality
                )

            except InvalidRecordError as error:
                rejected_records.append(
                    create_rejected_record(
                        path.name,
                        row_number,
                        error.field,
                        str(error)
                    )
                )
                continue

            observation = Observation(
                timestamp,
                heart_rate,
                skin_response,
                temperature,
                activity_level,
                signal_quality
            )

            sessions[session_id].add_observation(observation)
            accepted_rows += 1

    return sessions, rejected_records, accepted_rows