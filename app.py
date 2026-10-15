import csv
import os
from datetime import date

# Where we store our data
DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "worklog.csv")

# Column headers for our CSV
FIELDS = ["date", "task", "problem", "department", "time_spent", "status"]


def ensure_data_file():
    """Create the data folder and CSV file if they don't exist yet."""
    os.makedirs(DATA_FOLDER, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def ask(prompt, required=True):
    """Ask a question and return the answer. Loops if required and empty."""
    while True:
        answer = input(prompt).strip()
        if answer or not required:
            return answer
        print("  ⚠️  This field is required. Please enter something.")


def ask_status():
    """Ask for status with a limited set of options."""
    options = ["done", "pending", "blocked"]
    while True:
        answer = input("Status (done/pending/blocked): ").strip().lower()
        if answer in options:
            return answer
        print("  ⚠️  Please type one of: done, pending, blocked")


def collect_entry():
    """Ask the user all the questions and return a dict."""
    print("\n" + "=" * 50)
    print("📝  DAILY WORK LOG")
    print("=" * 50)

    entry = {
        "date": date.today().isoformat(),       # e.g. 2026-10-13
        "task": ask("What did you do today? "),
        "problem": ask("Any problem faced? (press Enter to skip) ", required=False),
        "department": ask("Department or tool involved: "),
        "time_spent": ask("Time spent (hours, e.g. 2 or 1.5): "),
        "status": ask_status(),
    }
    return entry


def save_entry(entry):
    """Append one row to the CSV file."""
    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(entry)


def main():
    ensure_data_file()

    while True:
        entry = collect_entry()
        save_entry(entry)
        print("\n✅  Entry saved to", DATA_FILE)

        again = input("\nAdd another entry? (y/n): ").strip().lower()
        if again != "y":
            print("\n👋  Done for today. Goodbye!\n")
            break


if __name__ == "__main__":
    main()