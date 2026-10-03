def calculate_average(values):
    """Calculates the average of a list of numerical values."""

    if len(values) == 0:
        return None

    total = 0

    for value in values:
        total += value

    return total / len(values)


def calculate_minimum(values):
    """Finds the minimum value in a list."""

    if len(values) == 0:
        return None

    minimum = values[0]

    for value in values:
        if value < minimum:
            minimum = value

    return minimum


def calculate_maximum(values):
    """Finds the maximum value in a list."""

    if len(values) == 0:
        return None

    maximum = values[0]

    for value in values:
        if value > maximum:
            maximum = value

    return maximum


def create_summary(values):
    """Creates average, minimum and maximum values."""

    return {
        "average": calculate_average(values),
        "minimum": calculate_minimum(values),
        "maximum": calculate_maximum(values)
    }


class Analyzer:
    """Analyzes the observations in one fitness session."""

    def __init__(self, session):
        self.session = session

    def get_heart_rates(self):
        """Returns all heart-rate values from the session."""

        heart_rates = []

        for observation in self.session.observations:
            heart_rates.append(observation.heart_rate)

        return heart_rates

    def get_activity_levels(self):
        """Returns all activity-level values from the session."""

        activity_levels = []

        for observation in self.session.observations:
            activity_levels.append(observation.activity_level)

        return activity_levels

    def get_temperatures(self):
        """Returns all temperature values from the session."""

        temperatures = []

        for observation in self.session.observations:
            temperatures.append(observation.temperature)

        return temperatures

    def get_skin_responses(self):
        """Returns all skin-response values from the session."""

        skin_responses = []

        for observation in self.session.observations:
            skin_responses.append(observation.skin_response)

        return skin_responses

    def get_heart_rate_summary(self):
        return create_summary(
            self.get_heart_rates()
        )

    def get_activity_summary(self):
        return create_summary(
            self.get_activity_levels()
        )

    def get_temperature_summary(self):
        return create_summary(
            self.get_temperatures()
        )

    def get_skin_response_summary(self):
        return create_summary(
            self.get_skin_responses()
        )

    def compare_with_reference(self):
        """Compares session averages with participant reference values."""

        participant = self.session.participant

        heart_rate_summary = self.get_heart_rate_summary()
        temperature_summary = self.get_temperature_summary()
        skin_response_summary = self.get_skin_response_summary()

        # Skip reference comparison when no usable observations are available
        if heart_rate_summary["average"] is None:
            return {
                "heart_rate_difference": None,
                "temperature_difference": None,
                "skin_response_difference": None
            }

        return {
            "heart_rate_difference":
                heart_rate_summary["average"]
                - participant.baseline_heart_rate,

            "temperature_difference":
                temperature_summary["average"]
                - participant.baseline_temperature,

            "skin_response_difference":
                skin_response_summary["average"]
                - participant.baseline_skin_response
        }

    def is_recovering(self):
        """Checks whether activity and heart rate fall after a clear peak."""

        observations = self.session.observations

        if len(observations) < 4:
            return False

        # Find the observation with the highest activity level
        peak_observation = observations[0]

        for observation in observations:
            if observation.activity_level > peak_observation.activity_level:
                peak_observation = observation

        last_observation = observations[-1]

        # Recovery should follow clear activity
        had_high_activity = peak_observation.activity_level >= 0.70

        activity_declined = (
            last_observation.activity_level
            <= peak_observation.activity_level - 0.30
        )

        heart_rate_declined = (
            last_observation.heart_rate
            <= peak_observation.heart_rate - 20
        )

        returned_toward_baseline = (
            last_observation.heart_rate
            <= self.session.participant.baseline_heart_rate + 25
        )

        return (
            had_high_activity
            and activity_declined
            and heart_rate_declined
            and returned_toward_baseline
        )

    def classify_session(self):
        """Classifies the fitness session."""

        observations = self.session.observations

        # Too few usable observations give an unreliable result
        if len(observations) < 3:
            return "insufficient data"

        if self.is_recovering():
            return "recovering"

        heart_rate_summary = self.get_heart_rate_summary()
        activity_summary = self.get_activity_summary()

        average_heart_rate = heart_rate_summary["average"]
        average_activity = activity_summary["average"]

        baseline_heart_rate = (
            self.session.participant.baseline_heart_rate
        )

        # Classification thresholds are project assumptions
        if (
            average_activity < 0.25
            and average_heart_rate <= baseline_heart_rate + 20
        ):
            return "resting"

        if (
            average_activity >= 0.70
            or average_heart_rate >= baseline_heart_rate + 60
        ):
            return "high activity"

        return "moderate activity"

    def get_classification_reason(self):
        """Returns a readable reason for the classification."""

        classification = self.classify_session()

        if classification == "insufficient data":
            return "Fewer than three usable observations are available."

        if classification == "recovering":
            return (
                "Heart rate and activity decreased after a period "
                "of clear activity."
            )

        if classification == "resting":
            return (
                "Average heart rate and activity are close "
                "to resting values."
            )

        if classification == "high activity":
            return (
                "Heart rate or activity level is clearly elevated."
            )

        return "Heart rate and activity indicate moderate activity."

    def analyze(self):
        """Returns the complete session analysis as a dictionary."""

        return {
            "session_id": self.session.session_id,
            "participant_id": self.session.participant.participant_id,
            "participant_name": self.session.participant.name,
            "usable_observations": len(self.session.observations),
            "classification": self.classify_session(),
            "reason": self.get_classification_reason(),
            "heart_rate": self.get_heart_rate_summary(),
            "activity_level": self.get_activity_summary(),
            "temperature": self.get_temperature_summary(),
            "skin_response": self.get_skin_response_summary(),
            "reference_comparison": self.compare_with_reference()
        }