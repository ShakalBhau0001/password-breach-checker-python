import getpass

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from core.checker import check_multiple, check_password, mask_password

console = Console()

def print_banner():
    console.clear()
    banner = Text()
    banner.append("██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗\n", style="bold cyan",)
    banner.append("██╔══██╗██║    ██║████╗  ██║██╔════╝██╔══██╗\n", style="bold cyan",)
    banner.append("██████╔╝██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║\n", style="bold blue",)
    banner.append("██╔═══╝ ██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║\n", style="bold blue",)
    banner.append("██║     ╚███╔███╔╝██║ ╚████║███████╗██████╔╝\n\n", style="bold magenta",)
    banner.append(" Password Breach Checker • HaveIBeenPwned ", style="dim white",)
    console.print(
        Panel(
            Align.center(banner),
            border_style="cyan",
            box=box.DOUBLE_EDGE,
        )
    )


def divider(title=""):
    console.print(
        Rule(
            title,
            style="cyan",
        )
    )


def success(message):
    console.print(f"\n[bold green]✔[/bold green] {message}\n")


def error(message):
    console.print(f"\n[bold red]✘[/bold red] {message}\n")


def info(message):
    console.print(f"[bold yellow]ℹ[/bold yellow] {message}")


def print_result(label, count):
    if count > 0:
        console.print(
            Panel(
                f"[bold red]🔴 BREACHED[/bold red] — {label} seen "
                f"[bold red]{count:,}[/bold red] times in known data breaches",
                border_style="red",
                box=box.ROUNDED,
            )
        )
    else:
        console.print(
            Panel(
                f"[bold green]✅ SAFE[/bold green] — {label} not found in known breaches",
                border_style="green",
                box=box.ROUNDED,
            )
        )


def menu():
    table = Table(
        title="Main Menu",
        title_style="bold cyan",
        box=box.DOUBLE_EDGE,
        border_style="cyan",
        padding=(0, 2),
    )
    table.add_column(
        "Option",
        justify="center",
        style="bold yellow",
    )
    table.add_column("Action", style="green",)
    table.add_row("1", "🔍 Check a Single Password",)
    table.add_row("2", "📄 Check Passwords from a File",)
    table.add_row("3", "ℹ About",)
    table.add_row("0", "🚪 Exit",)
    console.print(table)


def single_menu():
    divider("🔍 Check a Single Password")
    password = getpass.getpass("Enter password (hidden): ")
    if not password:
        error("No password entered.")
        return
    try:
        count = check_password(password)
        print_result(mask_password(password), count)
    except RuntimeError as e:
        error(str(e))


def file_menu():
    divider("📄 Check Passwords from a File")
    path = Prompt.ask("[bold cyan]Enter file path[/bold cyan]").strip()
    try:
        with open(path, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]

        if not passwords:
            info("File is empty — nothing to check.")
            return

        results = check_multiple(passwords)
        for pw, count in results.items():
            print_result(mask_password(pw), count)
    except FileNotFoundError:
        error("File not found.")
    except RuntimeError as e:
        error(str(e))


def about():
    divider("ℹ About Toolkit")
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
        border_style="cyan",
    )
    table.add_column("Property", style="yellow",)
    table.add_column("Value", style="green",)
    table.add_row("Purpose", "Password Breach Checking",)
    table.add_row("Data Source", "HaveIBeenPwned",)
    table.add_row("Privacy Model", "k-Anonymity (partial hash only)",)
    table.add_row("Input Modes", "Single password / File (one per line)",)
    table.add_row("Password Input", "Hidden (getpass)",)
    table.add_row("Language", "Python",)
    table.add_row("UI", "Rich CLI",)
    console.print(table)


def main():
    while True:
        print_banner()
        menu()
        choice = Prompt.ask(
            "\n[bold cyan]Select Option[/bold cyan]",
            choices=["1", "2", "3", "0"],
            default="1",
        )
        if choice == "1":
            single_menu()
        elif choice == "2":
            file_menu()
        elif choice == "3":
            about()
        elif choice == "0":
            console.print()
            console.print(
                Panel(
                    Align.center(
                        Text(
                            "See You Soon! | Stay safe, stay secure. 🕵️",
                            style="bold cyan",
                        )
                    ),
                    border_style="magenta",
                    box=box.DOUBLE_EDGE,
                )
            )
            break
        Prompt.ask(
            "\n[dim]Press Enter to return to menu…[/dim]",
            default="",
        )


if __name__ == "__main__":
    main()
