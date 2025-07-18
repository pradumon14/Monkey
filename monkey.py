"""
Monkey CLI: A Deterministic Password Generator.

This script generates complex, secure passwords on-demand without ever storing them.
All processing happens locally on your machine, ensuring maximum privacy and security.

Created with ❤️ by Pradumon Sahani.
GitHub: https://github.com/pradumon14
"""

import hashlib
import getpass
import argparse
import string
import sys
import subprocess

# --- Rich Library Import and Fallback ---
# Attempts to import the 'rich' library for enhanced terminal UI.
# If 'rich' is not available, it falls back to basic print statements.
RICH_AVAILABLE = False
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.prompt import Prompt as RichPrompt
    from rich.text import Text as RichText
    from rich.box import MINIMAL
    RICH_AVAILABLE = True
except ImportError:
    pass # rich not available, proceed with fallbacks

# Define fallback classes if rich is not available
if not RICH_AVAILABLE:
    class FallbackConsole:
        """A simple console fallback when rich is not installed."""
        def print(self, *args, **kwargs):
            text = " ".join(str(arg) for arg in args)
            # Strip rich markup for plain output
            text = text.replace("[bold yellow]", "").replace("[/bold yellow]", "") \
                       .replace("[bold green]", "").replace("[/bold green]", "") \
                       .replace("[bold blue]", "").replace("[/bold blue]", "") \
                       .replace("[dim]", "").replace("[/dim]", "") \
                       .replace("[bold red]", "").replace("[/bold red]", "") \
                       .replace("[bold magenta]", "").replace("[/bold magenta]", "") \
                       .replace("[cyan]", "").replace("[/cyan]", "") \
                       .replace("[bold orange3]", "").replace("[/bold orange3]", "") \
                       .replace("[green]", "").replace("[/green]", "") \
                       .replace("[bold green_yellow]", "").replace("[/bold green_yellow]", "") \
                       .replace("[yellow]", "").replace("[/yellow]", "") \
                       .replace("[on black]", "")
            file_arg = kwargs.pop('file', sys.stdout) # Handle 'file' argument for compatibility
            print(text, file=file_arg, **kwargs)

        def rule(self, *args, **kwargs):
            print("-" * 50) # Simple rule for fallback
        def panel(self, content, *args, **kwargs):
            title = kwargs.get('title', '')
            if title:
                print(f"\n--- {title} ---\n{content}\n------------------\n")
            else:
                print(f"\n{content}\n------------------\n")

    class FallbackPrompt:
        """A simple prompt fallback when rich is not installed."""
        def ask(self, prompt_text, **kwargs):
            return input(f"{str(prompt_text)}: ")

    class FallbackText(str):
        """A simple text fallback when rich is not installed."""
        def __new__(cls, text, style=None):
            return str.__new__(cls, text)
        def __init__(self, text, style=None):
            self.plain = text # Store plain text for compatibility

# Instantiate console, Prompt, and Text objects based on rich availability
console = Console() if RICH_AVAILABLE else FallbackConsole()
Prompt = RichPrompt if RICH_AVAILABLE else FallbackPrompt()
Text = RichText if RICH_AVAILABLE else FallbackText

# Warn user if rich is not available
if not RICH_AVAILABLE:
    console.print("\n[bold yellow]Warning: 'rich' library not found.[/bold yellow]")
    console.print("[bold yellow]Falling back to basic terminal output. For a better experience, install it:[/bold yellow]")
    console.print("[bold cyan]pip install rich[/bold cyan]\n")


# --- Global Character Sets ---
# These sets define the characters used in password generation.
SYMBOLS_DEFAULT = "!@#$%^&*()_-+=[]{}|;:,.<>?/"
LOWERCASE_BASE = string.ascii_lowercase
UPPERCASE_BASE = string.ascii_uppercase
NUMBERS_BASE = string.digits

def copy_to_clipboard(text: str) -> bool:
    """
    Copies the given text to the system clipboard using platform-specific commands.

    Args:
        text (str): The string to copy to the clipboard.

    Returns:
        bool: True if the copy operation was successful, False otherwise.
    """
    try:
        if sys.platform == "darwin": # macOS
            subprocess.run("pbcopy", text=text, check=True, input=text)
        elif sys.platform == "win32": # Windows
            subprocess.run("clip", text=text, check=True, input=text)
        elif sys.platform.startswith("linux"): # Linux
            # Try xclip first, then xsel
            try:
                subprocess.run(["xclip", "-selection", "clipboard"], text=text, check=True, input=text)
            except FileNotFoundError:
                subprocess.run(["xsel", "-b"], text=text, check=True, input=text)
        else:
            console.print("[bold red]Clipboard copying not supported on this OS.[/bold red]")
            return False
        return True
    except FileNotFoundError:
        console.print("[bold red]Clipboard utility not found. Please install 'xclip' or 'xsel' on Linux, or ensure 'pbcopy' (macOS) / 'clip' (Windows) are available.[/bold red]")
        return False
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to copy to clipboard: {e}[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred during clipboard copy: {e}[/bold red]")
        return False

def estimate_password_strength(password: str) -> tuple[str, str, list[str]]:
    """
    Provides a basic, local estimation of password strength based on common criteria.
    This is a rule-based assessment and does not use external services.

    Args:
        password (str): The password string to evaluate.

    Returns:
        tuple[str, str, list[str]]: A tuple containing:
            - strength_level (str): e.g., "Very Weak", "Strong".
            - strength_color (str): Rich color string for terminal output.
            - feedback (list[str]): A list of suggestions or observations.
    """
    strength_score = 0
    feedback = []

    length = len(password)
    if length < 8:
        feedback.append("[red]Very short password.[/red]")
    elif length < 12:
        strength_score += 1
        feedback.append("[yellow]Good length.[/yellow]")
    else:
        strength_score += 2
        feedback.append("[green]Excellent length![/green]")

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    char_types = 0
    if has_upper: char_types += 1
    if has_lower: char_types += 1
    if has_digit: char_types += 1
    if has_symbol: char_types += 1

    if char_types < 2:
        feedback.append("[red]Lacks character diversity (try mixing types).[/red]")
    elif char_types == 2:
        strength_score += 1
        feedback.append("[yellow]Moderate character diversity.[/yellow]")
    elif char_types == 3:
        strength_score += 2
        feedback.append("[green]Good character diversity.[/green]")
    else: # char_types == 4
        strength_score += 3
        feedback.append("[green]Excellent character diversity![/green]")

    # Very basic check for repeating characters (e.g., "aaaa")
    if length > 3:
        for i in range(length - 3):
            if password[i] == password[i+1] == password[i+2] == password[i+3]:
                feedback.append("[red]Avoid repeating characters (e.g., 'aaaa').[/red]")
                strength_score -= 1
                break

    # Determine overall strength level and corresponding color
    strength_level = ""
    strength_color = ""
    if strength_score < 1:
        strength_level = "Very Weak"
        strength_color = "bold red"
    elif strength_score < 3:
        strength_level = "Weak"
        strength_color = "bold orange3"
    elif strength_score < 5:
        strength_level = "Moderate"
        strength_color = "bold yellow"
    elif strength_score < 7:
        strength_level = "Strong"
        strength_color = "bold green"
    else:
        strength_level = "Very Strong"
        strength_color = "bold green_yellow"

    return strength_level, strength_color, feedback

def generate_monkey_password(simple_password: str, unique_key: str, desired_length: int,
                             include_upper: bool, include_lower: bool, include_numbers: bool, include_symbols: bool,
                             custom_symbols_set: str, verbose: bool) -> str:
    """
    Generates a complex, secure password based on the "Monkey" algorithm.

    The algorithm is entirely deterministic: the same inputs will always
    produce the same output. No true randomness is involved.

    Args:
        simple_password (str): A user-provided simple password/phrase.
        unique_key (str): A user-provided unique key (e.g., website name, email).
        desired_length (int): The required length of the generated password.
        include_upper (bool): True if uppercase letters should be included.
        include_lower (bool): True if lowercase letters should be included.
        include_numbers (bool): True if numbers should be included.
        include_symbols (bool): True if symbols should be included.
        custom_symbols_set (str): User-defined set of symbols to use.
        verbose (bool): True to print intermediate hash for debugging/understanding.

    Returns:
        str: The deterministically generated complex password.

    Raises:
        ValueError: If no character types are enabled for generation.
    """

    symbols_to_use = custom_symbols_set if custom_symbols_set else SYMBOLS_DEFAULT

    # Create active character sets based on user's include/exclude choices.
    active_char_sets = []
    if include_upper and UPPERCASE_BASE:
        active_char_sets.append(UPPERCASE_BASE)
    if include_lower and LOWERCASE_BASE:
        active_char_sets.append(LOWERCASE_BASE)
    if include_numbers and NUMBERS_BASE:
        active_char_sets.append(NUMBERS_BASE)
    if include_symbols and symbols_to_use: # Ensure symbols_to_use is not empty if included
        active_char_sets.append(symbols_to_use)

    # Validate that at least one character type is selected.
    if not active_char_sets:
        raise ValueError("No character types are enabled or available for password generation. Please enable at least one type.")

    # --- 1. Input Combination ---
    combined_input = simple_password + str(unique_key)

    # --- 2. SHA-256 Hashing ---
    # Compute the SHA-256 hash of the combined input.
    # SHA-256 produces a 64-character hexadecimal string.
    base_hash = hashlib.sha256(combined_input.encode()).hexdigest()

    if verbose:
        console.print(f"  [dim]Combined input (truncated): '{combined_input[:10]}...{combined_input[-10:]}'[/dim]")
        console.print(f"  [dim]SHA-256 Hash: {base_hash}[/dim]")

    # --- 3. Length Adjustment & Initial Character Pool ---
    # Ensure extended_hash is long enough for all character selections and diversity injections.
    # We need at least 2 hex chars per password char for Pass 1, plus 2 hex chars per diversity injection for Pass 2.
    min_hash_needed = desired_length * 2 + len(active_char_sets) * 2
    # Extend the base hash sufficiently to cover all generation needs, plus a buffer.
    extended_hash = (base_hash * ((min_hash_needed // len(base_hash)) + 2))[:min_hash_needed + 10]

    # Initialize the list of password characters.
    transformed_password_chars = [''] * desired_length

    # --- 4. Advanced Deterministic Transformation (Pass 1) ---
    # Iterates through each position, deterministically selecting a character type
    # and a character from that type based on the SHA-256 hash.
    hash_read_idx = 0

    for i in range(desired_length):
        # Dynamically extend hash if we are running out of deterministic values
        if hash_read_idx + 1 >= len(extended_hash):
            extended_hash += base_hash.repeat(2)
            if verbose:
                console.print("[dim]  Dynamically extended hash for more deterministic values.[/dim]")

        # Get a "decision value" (0-15) from the hash to pick a character set.
        decision_val = int(extended_hash[hash_read_idx], 16)
        hash_read_idx += 1

        # Deterministically select a character set from the active ones.
        target_char_set = active_char_sets[decision_val % len(active_char_sets)]

        # Get a "character selection value" (0-15) from the hash to pick a character within the set.
        if hash_read_idx + 1 >= len(extended_hash):
            extended_hash += base_hash.repeat(2) # Re-extend if needed
        char_select_val = int(extended_hash[hash_read_idx], 16)
        hash_read_idx += 1

        # Pick the character and assign it.
        if target_char_set: # Ensure target_char_set is not empty
            transformed_password_chars[i] = target_char_set[char_select_val % len(target_char_set)]
        else:
            # Fallback if a chosen set is empty (should be rare due to initial checks)
            fallback_set = next((s for s in active_char_sets if s), None)
            if fallback_set:
                transformed_password_chars[i] = fallback_set[char_select_val % len(fallback_set)]
            else:
                transformed_password_chars[i] = '?' # Critical fallback, indicates a problem

    # --- 5. Guaranteed Diversity (Pass 2) ---
    # After initial transformations, ensures the password contains at least one
    # of each *required* character type to meet common password policies.
    current_password_string = "".join(transformed_password_chars)

    categories_to_ensure = []
    # Check if each *enabled* category is present. If not, add to categories_to_ensure.
    if include_upper and not any(c.isupper() for c in current_password_string) and UPPERCASE_BASE:
        categories_to_ensure.append(UPPERCASE_BASE)
    if include_lower and not any(c.islower() for c in current_password_string) and LOWERCASE_BASE:
        categories_to_ensure.append(LOWERCASE_BASE)
    if include_numbers and not any(c.isdigit() for c in current_password_string) and NUMBERS_BASE:
        categories_to_ensure.append(NUMBERS_BASE)
    # Check for symbols using the actual symbols_to_use, not just string.punctuation
    if include_symbols and not any(c in symbols_to_use for c in current_password_string) and symbols_to_use:
         categories_to_ensure.append(symbols_to_use)

    guarantee_hash_idx = hash_read_idx # Continue consuming hash from where Pass 1 left off

    for char_set in categories_to_ensure:
        if not char_set: # Skip if the character set itself is empty
            continue

        if guarantee_hash_idx + 1 >= len(extended_hash):
            extended_hash += base_hash.repeat(2)
            if verbose:
                console.print("[dim]  Dynamically extended hash for diversity injection.[/dim]")

        pos_val = int(extended_hash[guarantee_hash_idx % len(extended_hash)], 16)
        guarantee_hash_idx += 1
        injection_position = pos_val % desired_length

        if guarantee_hash_idx + 1 >= len(extended_hash):
            extended_hash += base_hash.repeat(2)
        char_val = int(extended_hash[guarantee_hash_idx % len(extended_hash)], 16)
        guarantee_hash_idx += 1
        char_to_inject = char_set[char_val % len(char_set)]

        transformed_password_chars[injection_position] = char_to_inject
        if verbose:
            console.print(f"[dim]  Injected '{char_to_inject}' for diversity at position {injection_position}.[/dim]")

    return "".join(transformed_password_chars)

def main():
    """
    Main function to parse command-line arguments, get secure inputs,
    generate passwords, and display results with a clean CLI.
    """
    parser = argparse.ArgumentParser(
        description="""[bold blue]Monkey CLI:[/bold blue] A deterministic password generator.

    Generates complex, secure passwords on-demand without ever storing them.
    All processing happens locally on your machine.
    """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        help="Desired length of the generated complex password (e.g., 8, 16, 32, 64, or any positive integer). If not provided, you will be prompted."
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)."
    )
    parser.add_argument(
        "--no-upper",
        action="store_true",
        help="Exclude uppercase letters from the generated password."
    )
    parser.add_argument(
        "--no-lower",
        action="store_true",
        help="Exclude lowercase letters from the generated password."
    )
    parser.add_argument(
        "--no-numbers",
        action="store_true",
        help="Exclude numbers from the generated password."
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols from the generated password."
    )
    parser.add_argument(
        "--symbols-set",
        type=str,
        help="Provide a custom set of symbols (e.g., '!@#$'). Overrides default symbols."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose output, including intermediate hash and transformation details."
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Automatically copy the generated password(s) to the clipboard."
    )
    args = parser.parse_args()

    # Welcome Panel
    console.print(Panel(
        "[bold green]Welcome to Monkey CLI Password Generator![/bold green]\n\n"
        "[dim]Your privacy is paramount: All processing happens locally. "
        "No data is ever stored or sent to a server.[/dim]",
        title="[bold blue]Monkey CLI[/bold blue]",
        border_style="blue",
        box=MINIMAL if RICH_AVAILABLE else None
    ))
    console.print(Rule(style="dim"))

    desired_length = args.length

    # Prompt for length if not provided via CLI argument
    if desired_length is None:
        while True:
            try:
                length_input_str = Prompt.ask(
                    Text("Enter desired password length", style="bold magenta") +
                    Text(" (e.g., 16, minimum 4 for diversity)", style="cyan"),
                    console=console,
                    default="16" # Default needs to be a string for Prompt.ask
                )
                desired_length = int(length_input_str) # Manual conversion to int

                if desired_length <= 0:
                    console.print("[bold red]Length must be a positive integer.[/bold red]")
                elif desired_length < 4 and not (args.no_upper and args.no_lower and args.no_numbers and args.no_symbols):
                    console.print("[bold yellow]Warning: Length less than 4 might make it hard to guarantee all character types (if enabled).[/bold yellow]")
                    break
                else:
                    break
            except ValueError: # Catch if int() conversion fails
                console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]", file=sys.stderr)
            except Exception: # Catch other exceptions like Ctrl+C
                console.print("[bold red]Operation cancelled. Exiting.[/bold red]", file=sys.stderr)
                sys.exit(1)

    # Final validation for desired_length
    if desired_length <= 0:
        console.print("[bold red]Error: Desired length must be a positive integer.[/bold red]", file=sys.stderr)
        sys.exit(1)

    # Secure Input Panel
    console.print(Panel(
        "[bold yellow]Now, let's get your secret inputs.[/bold yellow]\n"
        "[dim]They will not be visible as you type, ensuring your privacy.[/dim]",
        title="[bold blue]Secure Input[/bold blue]",
        border_style="yellow",
        box=MINIMAL if RICH_AVAILABLE else None
    ))

    try:
        # getpass.getpass takes a string prompt, so Text.plain is used
        simple_password = getpass.getpass(prompt=Text("Enter your Simple Password (e.g., 'mysecretphrase'): ", style="bold green").plain)
        unique_key = getpass.getpass(prompt=Text("Enter your Unique Key (e.g., 'facebook', 'email!'): ", style="bold green").plain)
    except Exception as e:
        console.print(f"[bold red]Error reading input: {e}[/bold red]", file=sys.stderr)
        sys.exit(1)

    # Validate inputs are not empty
    if not simple_password or not unique_key:
        console.print("[bold red]Error: Both Simple Password and Unique Key are required to generate a password.[/bold red]", file=sys.stderr)
        sys.exit(1)

    # Generation Options Summary
    console.print(Rule("[bold magenta]Generation Options[/bold magenta]", style="magenta"))
    console.print(f"  [bold]Generating:[/bold] [cyan]{args.count}[/cyan] password(s)")
    console.print(f"  [bold]Length:[/bold] [cyan]{desired_length}[/cyan]")
    if args.no_upper: console.print("  [bold red]- Excluding uppercase letters.[/bold red]")
    if args.no_lower: console.print("  [bold red]- Excluding lowercase letters.[/bold red]")
    if args.no_numbers: console.print("  [bold red]- Excluding numbers.[/bold red]")
    if args.no_symbols: console.print("  [bold red]- Excluding symbols.[/bold red]")
    if args.symbols_set: console.print(f"  [bold yellow]- Using custom symbols:[/bold yellow] '[cyan]{args.symbols_set}[/cyan]'")
    if args.copy: console.print("  [bold green]- Automatically copying to clipboard.[/bold green]")
    console.print(Rule(style="dim"))


    # Loop for generating multiple passwords
    for i in range(args.count):
        if args.count > 1:
            console.print(Rule(f"[bold blue]Password {i + 1} of {args.count}[/bold blue]", style="blue"))

        try:
            generated_password = generate_monkey_password(
                simple_password,
                unique_key,
                desired_length,
                not args.no_upper,
                not args.no_lower,
                not args.no_numbers,
                not args.no_symbols,
                args.symbols_set,
                args.verbose
            )

            # Display Generated Password
            console.print(Panel(
                Text(generated_password, style="bold green_yellow on black", justify="center"),
                title="[bold green]Generated Password[/bold green]",
                border_style="green",
                box=MINIMAL if RICH_AVAILABLE else None
            ))

            # Display Strength and Feedback
            strength_level, strength_color, feedback = estimate_password_strength(generated_password)
            console.print(f"  [bold]Strength:[/bold] [{strength_color}]{strength_level}[/{strength_color}]")
            if feedback:
                console.print(Text("Feedback:", style="bold blue"))
                for item in feedback:
                    console.print(Text(f"  - {item}"))

            # Clipboard Copy
            if args.copy:
                if copy_to_clipboard(generated_password):
                    console.print("[bold green]Password copied to clipboard![/bold green]")
                else:
                    console.print("[bold yellow]Failed to copy password to clipboard. Please copy manually.[/bold yellow]")
            else:
                console.print("[dim]Please copy and paste this password where needed. It is NOT stored.[/dim]")

        except ValueError as e:
            console.print(f"[bold red]Error during generation: {e}[/bold red]")
            if args.count > 1:
                console.print(Rule(style="red"))
            continue
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
            if args.count > 1:
                console.print(Rule(style="red"))
            continue

    # Final Security Note
    console.print(Rule(style="dim"))
    console.print(Panel(
        "[bold green]Generation Complete![/bold green]\n\n"
        "[dim]Remember: The security of your generated password depends on the strength of your 'Simple Password' and 'Unique Key'.[/dim]\n"
        "[bold yellow]Never store your 'Simple Password' or 'Unique Key' in plain text![/bold yellow]\n\n"
        "[dim]Created with ❤️ by Pradumon Sahani[/dim]", # Added attribution here
        title="[bold blue]Important Security Note[/bold blue]",
        border_style="blue",
        box=MINIMAL if RICH_AVAILABLE else None
    ))
    console.print(Rule(style="dim"))


if __name__ == "__main__":
    main()
