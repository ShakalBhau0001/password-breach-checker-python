import argparse
import getpass
import json

from core.checker import check_multiple, check_password, mask_password


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password-breach-checker",
        description="Check if password(s) have appeared in known data breaches (HaveIBeenPwned).",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-p",
        "--pass",
        "--password",
        dest="password",
        action="store_true",
        help="Prompt for a single password (hidden input)",
    )
    group.add_argument(
        "-f",
        "--file",
        metavar="PATH",
        help="Path to a file containing one password per line",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of formatted text",
    )
    return parser


def run_single(as_json: bool) -> None:
    password = getpass.getpass("Enter password (hidden): ")
    count = check_password(password)
    result = {"password": mask_password(password), "breach_count": count}
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        status = "BREACHED" if count > 0 else "SAFE"
        print(f"{status} — {result['password']}: {count:,} breach hits")


def run_file(path: str, as_json: bool) -> None:
    with open(path, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]

    counts = check_multiple(passwords)
    results = [
        {"password": mask_password(pw), "breach_count": count}
        for pw, count in counts.items()
    ]

    if as_json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            status = "BREACHED" if r["breach_count"] > 0 else "SAFE"
            print(f"{status} — {r['password']}: {r['breach_count']:,} breach hits")


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.password:
            run_single(args.json)
        elif args.file:
            run_file(args.file, args.json)
    except FileNotFoundError:
        parser.error(f"File not found: {args.file}")
    except RuntimeError as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
