import getpass

from core.checker import check_multiple, check_password, mask_password


def print_result(label: str, count: int) -> None:
    if count > 0:
        print(f"  🔴 BREACHED — {label} seen {count:,} times in known data breaches")
    else:
        print(f"  ✅ SAFE — {label} not found in known breaches")


def main():
    print("=" * 60)
    print("  🔐 PASSWORD BREACH CHECKER")
    print("=" * 60)
    print("\nChecks passwords against known data breaches (HaveIBeenPwned)")
    print("Your password is never sent in full — only a partial hash.\n")

    while True:
        print("-" * 60)
        print("Options:")
        print("1. Check a single password")
        print("2. Check passwords from a file (one per line)")
        print("3. Exit")

        choice = input("\nChoice (1-3): ").strip()
        if choice == "1":
            password = getpass.getpass("Enter password (hidden): ")
            if password:
                try:
                    count = check_password(password)
                    print_result(mask_password(password), count)
                except RuntimeError as e:
                    print(f"  ❌ {e}")

        elif choice == "2":
            path = input("Enter file path: ").strip()
            try:
                with open(path, "r") as f:
                    passwords = [line.strip() for line in f if line.strip()]
                results = check_multiple(passwords)
                for pw, count in results.items():
                    print()
                    print_result(mask_password(pw), count)
            except FileNotFoundError:
                print("  ❌ File not found")
            except RuntimeError as e:
                print(f"  ❌ {e}")

        elif choice == "3":
            print("\n👋 See You Soon!")
            break

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
