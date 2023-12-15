import argparse
import sys

from detect_llm_api_keys.key_detector import APIKeyDetector


def main():
    parser = argparse.ArgumentParser(
        description="Search for API keys in Python files",
    )
    parser.add_argument(
        "filename",
        nargs="+",
        help="The file to search for API keys",
    )
    args = parser.parse_args()
    filenames: list[str] = args.filename
    status = 0

    for filename in filenames:
        results = APIKeyDetector.check_file(filename)
        if results:
            for provider, line_numbers in results.items():
                for line_number in line_numbers:
                    print(f"{filename}:{line_number}:\tPotential {provider} API key")
            status = 1

    sys.exit(status)


if __name__ == "__main__":
    main()
