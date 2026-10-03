import re

from .exceptions import InvalidIdentifierError, InvalidRecordError


def validate_participant_id(participant_id):
    """Validates the format of a participant ID."""

    # Participant IDs must start with P followed by three digits
    if not isinstance(participant_id, str) or not re.fullmatch(
        r"P\d{3}", participant_id
    ):
        raise InvalidIdentifierError(
            f"Invalid participant ID: {participant_id}"
        )

    return participant_id


def validate_session_id(session_id):
    """Validates the format of a fitness session ID."""

    # Session IDs must follow the format FIT-YYYY-NNN
    if not isinstance(session_id, str) or not re.fullmatch(
        r"FIT-\d{4}-\d{3}", session_id
    ):
        raise InvalidIdentifierError(
            f"Invalid session ID: {session_id}"
        )

    return session_id


def validate_measurements(
    timestamp,
    heart_rate,
    skin_response,
    temperature,
    activity_level,
    signal_quality
):
    """Validates numerical values from one fitness observation."""

    if timestamp < 0:
        raise InvalidRecordError(
            "Timestamp must be zero or greater.",
            field="timestamp"
        )

    if not 35 <= heart_rate <= 205:
        raise InvalidRecordError(
            "Heart rate must be between 35 and 205 bpm.",
            field="heart_rate"
        )

    if skin_response < 0:
        raise InvalidRecordError(
            "Skin response cannot be negative.",
            field="skin_response"
        )

    if not 25 <= temperature <= 42:
        raise InvalidRecordError(
            "Temperature must be between 25 and 42 degrees Celsius.",
            field="temperature"
        )

    if not 0 <= activity_level <= 1:
        raise InvalidRecordError(
            "Activity level must be between 0 and 1.",
            field="activity_level"
        )

    if not 0 <= signal_quality <= 1:
        raise InvalidRecordError(
            "Signal quality must be between 0 and 1.",
            field="signal_quality"
        )

    # Reject measurements with very poor signal quality
    if signal_quality < 0.5:
        raise InvalidRecordError(
            "Signal quality is below the minimum accepted level of 0.5.",
            field="signal_quality"
        )


    
def convert_to_int(value, field):
    """Converts a CSV value to int or raises a clear record error."""

    if value is None or value == "":
        raise InvalidRecordError(
            "Required value is missing.",
            field=field
        )

    try:
        return int(value)

    except ValueError:
        raise InvalidRecordError(
            f"Value must be a whole number: {value}",
            field=field
        )


def convert_to_float(value, field):
    """Converts a CSV value to float or raises a clear record error."""

    if value is None or value == "":
        raise InvalidRecordError(
            "Required value is missing.",
            field=field
        )

    try:
        return float(value)

    except ValueError:
        raise InvalidRecordError(
            f"Value must be numeric: {value}",
            field=field
        )