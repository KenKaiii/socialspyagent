"""
Sherlock Handler Module for SocialSpyAgent.

This module provides functions to interact with the Sherlock tool
to find usernames across social networks.
"""

import sys
import subprocess
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.box import DOUBLE

from terminal_ui import (
    print_title, print_subtitle, print_info, print_success, print_warning, print_error,
    get_fancy_user_input, run_with_spinner
)

def run_sherlock(username: str, output_dir: str = "Output Spy") -> Optional[subprocess.CompletedProcess]:
    """
    Run sherlock to find usernames across social networks.

    Args:
        username: The username to search for
        output_dir: Directory to save the results (default: "Output Spy")

    Returns:
        CompletedProcess object if successful, None otherwise
    """
    import os

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Try to run sherlock with the simplest approach
    try:
        # First, try the most basic command without changing directory
        def run_sherlock_basic():
            return subprocess.run(
                ["sherlock", username],
                shell=True,
                capture_output=True,
                text=True
            )

        print_info("Running sherlock...")
        result = run_with_spinner(
            run_sherlock_basic,
            f"Searching for '{username}' across social networks...",
            "sherlock",  # Custom styling
        )

        # Check if the command was successful
        if result.returncode == 0:
            # Save the output to our custom location
            output_file = os.path.join(output_dir, f"{username}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result.stdout)

            # Check if there's a file in the root directory and remove it
            root_file = f"{username}.txt"
            if os.path.exists(root_file):
                try:
                    os.remove(root_file)
                except Exception:
                    pass

            return result
    except Exception as e:
        print_error(f"Error running sherlock: {str(e)}")

    # If the first method failed, try with python -m sherlock
    try:
        def run_sherlock_module():
            return subprocess.run(
                [sys.executable, "-m", "sherlock", username],
                capture_output=True,
                text=True
            )

        print_info("Trying alternative method...")
        result = run_with_spinner(
            run_sherlock_module,
            f"Searching for '{username}' across social networks...",
            "sherlock",  # Custom styling
        )

        # Check if the command was successful
        if result.returncode == 0:
            # Save the output to our custom location
            output_file = os.path.join(output_dir, f"{username}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result.stdout)

            # Check if there's a file in the root directory and remove it
            root_file = f"{username}.txt"
            if os.path.exists(root_file):
                try:
                    os.remove(root_file)
                except Exception:
                    pass

            return result
    except Exception as e:
        print_error(f"Error running sherlock module: {str(e)}")

    # If all methods failed, show error and suggestions
    print_error("Failed to run sherlock. Please try the following:")
    print_error("1. Make sure sherlock is installed: pip install sherlock-project")
    print_error("2. Try activating your virtual environment before running the script")
    print_error("3. Try running the script from VS Code terminal")

    return None

def display_sherlock_results(result: subprocess.CompletedProcess, username: str, output_dir: str = "Output Spy") -> None:
    """
    Display the results of a sherlock search.

    Args:
        result: CompletedProcess object from running sherlock
        username: The username that was searched for
        output_dir: Directory where results are saved (default: "Output Spy")
    """
    if result.returncode == 0:
        import os

        # Check if the output file exists
        output_file = os.path.join(output_dir, f"{username}.txt")

        # Get the output content
        output_content = result.stdout

        # Debug: Print raw output to help diagnose issues
        print_info("Processing sherlock results...")

        # Parse the output to find accounts
        output_lines = output_content.strip().split('\n')

        # Sherlock output format can vary, so we need to be flexible in parsing
        # Look for lines containing "[+]" which indicates a found account
        found_accounts = []
        for line in output_lines:
            if "[+]" in line:
                found_accounts.append(line)

        # If we didn't find any accounts with "[+]", try looking for "FOUND" which is another indicator
        if not found_accounts:
            found_accounts = [line for line in output_lines if "FOUND" in line.upper()]

        # Display results
        if found_accounts:
            print_success(f"Search complete! Found {len(found_accounts)} accounts for username '{username}'")

            # Show the results in a table
            table = Table(
                title=f"Accounts found for {username}",
                border_style="bright_magenta",
                box=DOUBLE,
                header_style="bold magenta"
            )

            table.add_column("Platform", style="cyan")
            table.add_column("URL", style="green")

            for line in found_accounts:
                # Try different parsing approaches
                if "[+]" in line and ":" in line:
                    parts = line.split(":", 1)  # Split on first colon only
                    if len(parts) >= 2:
                        platform = parts[0].replace("[+]", "").strip()
                        url = parts[1].strip()
                        table.add_row(platform, url)
                elif "FOUND" in line.upper():
                    # Try to extract platform and URL from FOUND lines
                    parts = line.split()
                    if len(parts) >= 2:
                        platform = parts[0].strip()
                        # Try to find a URL in the line
                        url_parts = [part for part in parts if part.startswith("http")]
                        url = url_parts[0] if url_parts else "URL not found"
                        table.add_row(platform, url)

            # Create a console instance for printing the table
            console = Console()
            console.print(table)

            # Inform about the text file
            print_info(f"Full results saved to {output_file}")
        else:
            # If we still didn't find any accounts, check if there's any useful information in the output
            if "not found" in output_content.lower() or "not exist" in output_content.lower():
                print_warning(f"No accounts found for username '{username}'")
            else:
                # If there's output but we couldn't parse it, show a more helpful message
                print_warning(f"Sherlock completed but no accounts were identified for '{username}'")
                print_info("The full output has been saved to the file for reference.")

                # Save the raw output to help diagnose issues
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(output_content)
    else:
        print_error(f"Error running sherlock: {result.stderr if result.stderr else 'Unknown error'}")

def spy_on_username() -> None:
    """
    Run sherlock to find usernames across social networks.
    """
    try:
        print_title("Spy on Username")

        # Get username with fancy prompt
        username = get_fancy_user_input(
            "Enter username to spy on",
            "Type a username to search across social networks.\nSherlock will find accounts with this username on various platforms.",
            default=""
        )

        if not username.strip():
            print_error("Username cannot be empty.")
            return

        # Create output directories if they don't exist
        import os
        output_dir = "Output Spy"
        os.makedirs(output_dir, exist_ok=True)

        print_subtitle(f"Searching for username: {username}")

        # Run sherlock with spinner animation
        print_info("Starting search across social networks...")
        print_info("This may take a while depending on the number of sites being checked.")

        # Check for and remove any existing files in the root directory with this username
        # (to prevent duplicates from previous runs)
        root_file = f"{username}.txt"
        if os.path.exists(root_file):
            try:
                os.remove(root_file)
            except Exception:
                # Ignore errors when trying to remove old files
                pass

        # Also check for and remove any existing files in the output directory
        output_file = os.path.join(output_dir, f"{username}.txt")
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except Exception:
                # Ignore errors when trying to remove old files
                pass

        # Run sherlock
        result = run_sherlock(username, output_dir)

        if result:
            # Make sure the output file exists
            if not os.path.exists(output_file):
                # Create the file with the stdout content
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result.stdout)

            # Display the results
            display_sherlock_results(result, username, output_dir)

            # Check again for any files created in the root directory and move them to output_dir
            if os.path.exists(root_file):
                try:
                    # Move the file from root to output directory (overwrite if exists)
                    os.replace(root_file, output_file)
                except Exception:
                    # If we can't move the file, try to delete it
                    try:
                        os.remove(root_file)
                    except Exception:
                        # Ignore errors when trying to clean up
                        pass
        else:
            print_error("Failed to run sherlock. Please make sure it's installed correctly.")
            print_info("You can install it with: pip install sherlock-project")

    except Exception as e:
        print_error(f"Error in spy_on_username: {str(e)}")
