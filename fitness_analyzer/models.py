class Participant:
    """Represents a participant and their personal reference values."""

    def __init__(
        self,
        participant_id,
        name,
        baseline_heart_rate,
        baseline_skin_response,
        baseline_temperature
    ):
        self.participant_id = participant_id
        self.name = name

        # Use the property setter to validate the baseline heart rate
        self.baseline_heart_rate = baseline_heart_rate

        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

    @property
    def baseline_heart_rate(self):
        return self._baseline_heart_rate

    @baseline_heart_rate.setter
    def baseline_heart_rate(self, value):
        if value <= 0:
            raise ValueError(
                "Baseline heart rate must be greater than 0."
            )

        self._baseline_heart_rate = value


class Observation:
    """Represents one observation from a fitness session."""

    def __init__(
        self,
        timestamp,
        heart_rate,
        skin_response,
        temperature,
        activity_level,
        signal_quality
    ):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality


class Session:
    """Represents one fitness session for a participant."""

    def __init__(self, session_id, participant):
        self.session_id = session_id
        self.participant = participant
        self.observations = []

    def add_observation(self, observation):
        self.observations.append(observation)