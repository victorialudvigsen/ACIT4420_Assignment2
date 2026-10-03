import csv
import argparse
from fitness_analyzer.analysis import Analyzer
from fitness_analyzer.data_loader import (
    load_participants,
    load_sessions
)
from fitness_analyzer.reporting import (
    create_output_directory,
    write_analysis_summary,
    write_analysis_report,
    write_rejected_records
)

def parse_arguments():
    """Reads file and output paths from the command line."""

    parser = argparse.ArgumentParser(
        description="Analyze wearable fitness session data."
    )

    parser.add_argument(
        "--profiles",
        default="data/participants.csv",
        help="Path to the participant profile CSV file."
    )

    parser.add_argument(
        "--sessions",
        nargs="+",
        default=[
            "data/fitness_sessions.csv",
            "data/fitness_sessions_invalid.csv"
        ],
        help="Paths to one or more fitness session CSV files."
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Directory where report files are saved."
    )

    return parser.parse_args()


def main():
    """Loads, validates and analyzes the fitness session data."""
    # Read file and output paths from the command line
    args = parse_arguments()

    # Create the output directory if it does not already exist
    output_path = create_output_directory(args.output)

    # Load participant data and handle file errors
    try:
        participants, participant_rejected_records, participant_accepted_rows = (
            load_participants(
                args.profiles
            )
        )

    except FileNotFoundError:
        print(f"Error: {args.profiles} was not found.")
        return

    except PermissionError:
        print(f"Error: permission denied when opening {args.profiles}.")
        return

    except csv.Error as error:
        print(f"Error while reading {args.profiles}: {error}")
        return

    # Use the session files provided through the command line
    session_files = args.sessions

    all_sessions = {}
    all_rejected_records = []
    total_accepted_rows = 0

    # Add rejected participant rows to the error list
    for record in participant_rejected_records:
        all_rejected_records.append(record)

    total_accepted_rows += participant_accepted_rows

    # Load both official session files and continue if one file cannot be read
    for session_file in session_files:
        try:
            sessions, rejected_records, accepted_rows = load_sessions(
                session_file,
                participants
            )

        except FileNotFoundError:
            print(f"Error: {session_file} was not found.")
            continue

        except PermissionError:
            print(f"Error: permission denied when opening {session_file}.")
            continue

        except csv.Error as error:
            print(f"Error while reading {session_file}: {error}")
            continue

        # Add sessions from this file to all sessions
        for session_id, session in sessions.items():
            all_sessions[session_id] = session

        # Collect rejected rows from both files
        for record in rejected_records:
            all_rejected_records.append(record)

        total_accepted_rows += accepted_rows

    # Analyze every session and store the structured results
    analysis_results = []

    for session in all_sessions.values():
        analyzer = Analyzer(session)
        result = analyzer.analyze()
        analysis_results.append(result)

    # Write one summary row for each analyzed session
    summary_file = write_analysis_summary(
        analysis_results,
        output_path
    )

    # Write a readable text report for all analyzed sessions
    report_file = write_analysis_report(
        analysis_results,
        output_path
    )

    # Write rejected rows with filename, row number, field and reason
    rejected_file = write_rejected_records(
        all_rejected_records,
        output_path
    )

    # Print a short completion summary
    print("Participants loaded:", len(participants))
    print("Sessions loaded:", len(all_sessions))
    print("Accepted rows:", total_accepted_rows)
    print("Rejected rows:", len(all_rejected_records))
    print("Created:", summary_file)
    print("Created:", report_file)
    print("Created:", rejected_file)

    print("\nSession analysis:")
    print("-----------------")

    for result in analysis_results:
        print(
            result["session_id"],
            "-",
            result["participant_name"],
            "-",
            result["classification"],
            "-",
            result["usable_observations"],
            "usable observations"
        )


if __name__ == "__main__":
    main()