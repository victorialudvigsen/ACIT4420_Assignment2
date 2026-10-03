import csv
from pathlib import Path


def create_output_directory(output_path):
    """Creates the output directory if it does not already exist."""

    path = Path(output_path)

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def format_number(value):
    """Rounds a numerical value to two decimals."""

    if value is None:
        return ""

    return round(value, 2)


def write_analysis_summary(results, output_path):
    """Writes one summary row for each analyzed fitness session."""

    file_path = output_path / "analysis_summary.csv"

    fieldnames = [
        "session_id",
        "participant_id",
        "participant_name",
        "usable_observations",
        "classification",
        "reason",
        "average_heart_rate",
        "average_activity",
        "average_temperature",
        "average_skin_response"
    ]

    with open(
        file_path,
        mode="w",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:
            writer.writerow({
                "session_id": result["session_id"],
                "participant_id": result["participant_id"],
                "participant_name": result["participant_name"],
                "usable_observations": result["usable_observations"],
                "classification": result["classification"],
                "reason": result["reason"],
                "average_heart_rate": format_number(
                    result["heart_rate"]["average"]
                ),
                "average_activity": format_number(
                    result["activity_level"]["average"]
                ),
                "average_temperature": format_number(
                    result["temperature"]["average"]
                ),
                "average_skin_response": format_number(
                    result["skin_response"]["average"]
                )
            })

    return file_path


def write_analysis_report(results, output_path):
    """Writes a readable text report for all analyzed sessions."""

    file_path = output_path / "analysis_report.txt"

    with open(
        file_path,
        mode="w",
        encoding="utf-8"
    ) as file:

        for result in results:
            file.write("=" * 50 + "\n")
            file.write(f"Session: {result['session_id']}\n")
            file.write(
                f"Participant: {result['participant_name']} "
                f"({result['participant_id']})\n"
            )
            file.write(
                f"Usable observations: "
                f"{result['usable_observations']}\n"
            )
            file.write(
                f"Classification: {result['classification']}\n"
            )
            file.write(
                f"Reason: {result['reason']}\n"
            )

            if result["usable_observations"] > 0:
                file.write("\nHeart rate:\n")
                file.write(
                    f"  Average: "
                    f"{format_number(result['heart_rate']['average'])}\n"
                )
                file.write(
                    f"  Minimum: "
                    f"{format_number(result['heart_rate']['minimum'])}\n"
                )
                file.write(
                    f"  Maximum: "
                    f"{format_number(result['heart_rate']['maximum'])}\n"
                )

                file.write("\nActivity level:\n")
                file.write(
                    f"  Average: "
                    f"{format_number(result['activity_level']['average'])}\n"
                )

                file.write("\nTemperature:\n")
                file.write(
                    f"  Average: "
                    f"{format_number(result['temperature']['average'])}\n"
                )

                file.write("\nSkin response:\n")
                file.write(
                    f"  Average: "
                    f"{format_number(result['skin_response']['average'])}\n"
                )

                comparison = result["reference_comparison"]

                file.write("\nDifference from reference values:\n")
                file.write(
                    f"  Heart rate: "
                    f"{format_number(comparison['heart_rate_difference'])}\n"
                )
                file.write(
                    f"  Temperature: "
                    f"{format_number(comparison['temperature_difference'])}\n"
                )
                file.write(
                    f"  Skin response: "
                    f"{format_number(comparison['skin_response_difference'])}\n"
                )

            else:
                file.write(
                    "\nNo usable measurements were available.\n"
                )

            file.write("\n")

    return file_path


def write_rejected_records(rejected_records, output_path):
    """Writes rejected CSV rows and their error details to a text file."""

    file_path = output_path / "rejected_records.txt"

    with open(
        file_path,
        mode="w",
        encoding="utf-8"
    ) as file:

        # Write error details for each rejected row
        for record in rejected_records:
            file.write(
                f"File: {record['source_file']}\n"
            )
            file.write(
                f"Row: {record['row_number']}\n"
            )
            file.write(
                f"Field: {record['field']}\n"
            )
            file.write(
                f"Reason: {record['reason']}\n"
            )
            file.write("-" * 50 + "\n")

    return file_path