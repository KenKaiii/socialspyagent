"""
Terminal UI Module for SocialSpyAgent.

This module provides enhanced terminal UI components using Rich and Pyfiglet
for a more visually appealing command-line experience.
"""

import re
import time
import unicodedata
from typing import List, Dict, Any, Optional, Callable

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text
from rich import box
from rich.style import Style

# Initialize Rich console
console = Console()

def clean_text_for_display(text: str) -> str:
    """
    Clean text for better terminal display by:
    1. Removing or replacing problematic characters
    2. Normalizing unicode characters
    3. Ensuring consistent spacing
    4. Handling commas and other punctuation that may cause rendering issues

    Args:
        text: The text to clean

    Returns:
        Cleaned text suitable for terminal display
    """
    # Handle None or empty text
    if text is None or text == "":
        return "(No text)"

    # Ensure text is a string
    if not isinstance(text, str):
        try:
            text = str(text)
        except:
            return "(Invalid text)"

    try:
        # Normalize unicode
        text = unicodedata.normalize('NFC', text)

        # Replace emojis with placeholders to avoid rendering issues
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        text = emoji_pattern.sub(' ', text)  # Replace emojis with spaces for cleaner display

        # Remove control characters
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

        # Replace commas with a middle dot to prevent rendering issues
        text = text.replace(',', ' ·')

        # Replace other problematic characters that might cause rendering issues
        text = text.replace('"', "'")  # Replace double quotes with single quotes
        text = text.replace('…', '...')  # Replace ellipsis with three dots
        text = text.replace('—', '-')   # Replace em dash with hyphen
        text = text.replace('–', '-')   # Replace en dash with hyphen

        # Normalize whitespace
        text = ' '.join(text.split())

        return text.strip()
    except Exception:
        # If any error occurs during processing, return a safe value
        return "(Text processing error)"

# Define color styles
TITLE_STYLE = "bold cyan"
SUBTITLE_STYLE = "bold magenta"
HIGHLIGHT_STYLE = "bold yellow"
SUCCESS_STYLE = "bold green"
ERROR_STYLE = "bold red"
INFO_STYLE = "bold blue"
WARNING_STYLE = "bold orange3"
PANEL_STYLE = "bold white on blue"
PANEL_TITLE_STYLE = "bold yellow"

# Neon colors for enhanced UI
NEON_PINK = "bold #FF00FF"
NEON_BLUE = "bold #00FFFF"
NEON_GREEN = "bold #00FF00"
NEON_YELLOW = "bold #FFFF00"
NEON_ORANGE = "bold #FF8800"
NEON_PURPLE = "bold #9900FF"

# Table styles for dark background
YOUTUBE_BORDER_STYLE = "bright_blue"
YOUTUBE_TITLE_STYLE = "bold bright_blue"
YOUTUBE_HEADER_STYLE = "bold bright_cyan"
YOUTUBE_TEXT_STYLE = "bright_white"
YOUTUBE_BANNER_STYLE = "bold white on bright_blue"

INSTAGRAM_BORDER_STYLE = "bright_magenta"
INSTAGRAM_TITLE_STYLE = "bold bright_magenta"
INSTAGRAM_HEADER_STYLE = "bold bright_cyan"
INSTAGRAM_TEXT_STYLE = "bright_white"
INSTAGRAM_BANNER_STYLE = "bold white on bright_magenta"

TIKTOK_BORDER_STYLE = "bright_cyan"
TIKTOK_TITLE_STYLE = "bold bright_cyan"
TIKTOK_HEADER_STYLE = "bold bright_green"
TIKTOK_TEXT_STYLE = "bright_white"
TIKTOK_BANNER_STYLE = "bold white on bright_cyan"

def print_ascii_banner(text: str, font: str = "slant", style: str = TITLE_STYLE) -> None:
    """
    Print ASCII art banner using pyfiglet.

    Args:
        text: The text to convert to ASCII art.
        font: The font to use for the ASCII art.
        style: The style to apply to the ASCII art.
    """
    ascii_art = pyfiglet.figlet_format(text, font=font)
    console.print(ascii_art, style=style)

def print_title(text: str) -> None:
    """
    Print a title with styling.

    Args:
        text: The title text to print.
    """
    console.print(f"\n{text}", style=TITLE_STYLE)

def print_subtitle(text: str) -> None:
    """
    Print a subtitle with styling.

    Args:
        text: The subtitle text to print.
    """
    console.print(f"\n{text}", style=SUBTITLE_STYLE)

def print_info(text: str) -> None:
    """
    Print an info message with styling.

    Args:
        text: The info text to print.
    """
    console.print(f"ℹ️ {text}", style=INFO_STYLE)

def print_success(text: str) -> None:
    """
    Print a success message with styling.

    Args:
        text: The success text to print.
    """
    console.print(f"✅ {text}", style=SUCCESS_STYLE)

def print_error(text: str) -> None:
    """
    Print an error message with styling.

    Args:
        text: The error text to print.
    """
    console.print(f"❌ {text}", style=ERROR_STYLE)

def print_warning(text: str) -> None:
    """
    Print a warning message with styling.

    Args:
        text: The warning text to print.
    """
    console.print(f"⚠️ {text}", style=WARNING_STYLE)

def create_gradient_text(text: str, start_color: str, end_color: str) -> Text:
    """
    Create text with a color gradient from start_color to end_color.

    Args:
        text: The text to apply the gradient to.
        start_color: The starting color in hex format (e.g., "#FF00FF").
        end_color: The ending color in hex format (e.g., "#00FFFF").

    Returns:
        A Rich Text object with gradient coloring.
    """
    gradient_text = Text()

    # Parse hex colors
    start_r, start_g, start_b = int(start_color[1:3], 16), int(start_color[3:5], 16), int(start_color[5:7], 16)
    end_r, end_g, end_b = int(end_color[1:3], 16), int(end_color[3:5], 16), int(end_color[5:7], 16)

    # Calculate step size
    steps = max(1, len(text) - 1)
    r_step = (end_r - start_r) / steps
    g_step = (end_g - start_g) / steps
    b_step = (end_b - start_b) / steps

    for i, char in enumerate(text):
        # Calculate color for this position
        r = int(start_r + r_step * i)
        g = int(start_g + g_step * i)
        b = int(start_b + b_step * i)

        # Ensure values are in valid range
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        # Convert to hex
        color = f"#{r:02x}{g:02x}{b:02x}"
        gradient_text.append(char, Style(color=color, bold=True))

    return gradient_text

def print_panel(text: str, title: Optional[str] = None) -> None:
    """
    Print text in a panel with styling.

    Args:
        text: The text to print in the panel.
        title: Optional title for the panel.
    """
    panel = Panel(
        Text(text, style="white"),
        title=title,
        title_align="left",
        border_style=PANEL_STYLE,
        padding=(1, 2)
    )
    console.print(panel)

def print_table_title(text: str, platform: str) -> None:
    """
    Print a prominent title for tables with platform-specific styling.

    Args:
        text: The title text to print.
        platform: The platform name ('youtube', 'instagram', or 'tiktok').
    """
    # Select style based on platform
    if platform.lower() == 'youtube':
        style = YOUTUBE_BANNER_STYLE
        symbol = "▶"  # YouTube play button symbol (using a simpler character to avoid rendering issues)
    elif platform.lower() == 'instagram':
        style = INSTAGRAM_BANNER_STYLE
        symbol = "📸"  # Instagram camera symbol
    elif platform.lower() == 'tiktok':
        style = TIKTOK_BANNER_STYLE
        symbol = "🎵"  # TikTok music symbol
    else:
        style = TITLE_STYLE
        symbol = "📊"  # Default chart symbol

    # Create a full-width panel with the title
    width = console.width

    # Create centered text with symbols on both sides
    padded_text = f" {symbol} {text} {symbol} "

    # For YouTube, ensure we don't have any extra spaces or line breaks
    if platform.lower() == 'youtube':
        panel = Panel(
            Text(padded_text.strip(), justify="center"),
            box=box.DOUBLE,
            style=style,
            width=width,
            padding=(0, 0)
        )
    else:
        panel = Panel(
            Text(padded_text, justify="center"),
            box=box.DOUBLE,
            style=style,
            width=width,
            padding=(0, 0)
        )

    # Add some space before the panel
    console.print("")
    console.print(panel)
    console.print("")

def create_spinner(description: str, platform: str = None) -> Progress:
    """
    Create a visually pleasing spinner animation for social media processing tasks.
    Uses a combination of 'smiley' and 'aesthetic' spinners with platform-specific styling.

    Args:
        description: The text to display with the spinner.
        platform: Optional platform name ('youtube', 'instagram', or 'tiktok') for styling.

    Returns:
        A Progress object that can be used in a context manager.
    """
    # Select style based on platform
    if platform and platform.lower() == 'youtube':
        style = YOUTUBE_TITLE_STYLE
        emoji = "▶ "  # YouTube play button
    elif platform and platform.lower() == 'instagram':
        style = INSTAGRAM_TITLE_STYLE
        emoji = "📸 "  # Instagram camera
    elif platform and platform.lower() == 'tiktok':
        style = TIKTOK_TITLE_STYLE
        emoji = "🎵 "  # TikTok music note
    else:
        style = HIGHLIGHT_STYLE
        emoji = "🔍 "  # Default search icon

    # Create a progress bar with dual spinners for a more engaging visual
    return Progress(
        # Left spinner (smiley)
        SpinnerColumn("smiley", style=style, speed=1.0),

        # Platform-specific emoji and task description
        # The {task.description} will be set to the description parameter when the task is added
        TextColumn(f"[{style}]{emoji}{{task.description}}"),

        # Right spinner (aesthetic)
        SpinnerColumn("aesthetic", style=style, speed=1.0),

        # Ensure the spinner is displayed properly
        console=console,
        transient=True,  # Spinner disappears after completion
        refresh_per_second=15  # Smoother animation
    )

def create_progress_bar() -> Progress:
    """
    Create a progress bar.

    Returns:
        A Progress object that can be used in a context manager.
    """
    return Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40, style="cyan", complete_style="green"),
        TextColumn("[bold cyan]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    )

def get_user_choice(prompt: str, options: List[str]) -> int:
    """
    Display a menu and get user choice with rich styling.

    Args:
        prompt: The prompt to display.
        options: List of options to display.

    Returns:
        The user's choice as an integer.

    Raises:
        KeyboardInterrupt: If the user presses CTRL+C to cancel the operation.
    """
    print_subtitle(prompt)

    # Create a table for options
    table = Table(show_header=False, box=None)
    table.add_column("Number", style=HIGHLIGHT_STYLE)
    table.add_column("Option", style="white")

    for i, option in enumerate(options, 1):
        table.add_row(f"{i}.", option)

    console.print(table)

    # Get user input using a more direct approach that properly handles KeyboardInterrupt
    while True:
        console.print("\nEnter your choice: ", style=HIGHLIGHT_STYLE, end="")
        try:
            user_input = input()
            # If we get here, the user didn't press CTRL+C
            try:
                choice = int(user_input)
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print_error(f"Invalid choice. Please enter a number between 1 and {len(options)}.")
            except ValueError:
                print_error("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            # Re-raise KeyboardInterrupt to be caught by the outer try-except block
            print("\n")  # Add some space after the ^C
            raise

def get_user_input(prompt: str) -> str:
    """
    Get user input with rich styling.

    Args:
        prompt: The prompt to display.

    Returns:
        The user's input as a string.

    Raises:
        KeyboardInterrupt: If the user presses CTRL+C to cancel the operation.
    """
    console.print(prompt, style=HIGHLIGHT_STYLE, end=" ")
    try:
        return input()
    except KeyboardInterrupt:
        # Re-raise KeyboardInterrupt to be caught by the outer try-except block
        print("\n")  # Add some space after the ^C
        raise

def get_fancy_user_input(prompt: str, description: str = None, default: Optional[str] = None) -> str:
    """
    Get user input with a visually stunning prompt panel.

    Args:
        prompt: The prompt to display.
        description: Optional description or examples to show.
        default: Optional default value.

    Returns:
        The user input.

    Raises:
        KeyboardInterrupt: If the user presses CTRL+C to cancel the operation.
    """
    # Create a gradient title
    title = create_gradient_text(prompt, "#FF00FF", "#00FFFF")

    # Create content with description if provided
    content = ""
    if description:
        content = f"[bold white]{description}[/]"
        if default:
            content += f"\n[dim]Default: {default}[/]"

    # Create a panel with double borders
    panel = Panel(
        content,
        title=title,
        border_style="bright_magenta",
        box=box.DOUBLE,
        padding=(1, 2)
    )

    # Display the panel
    console.print(panel)

    # Create a colored prompt
    console.print(f"[{NEON_BLUE}]{prompt}: [/]", end="")

    # Get user input
    try:
        user_input = input()
        if default and not user_input:
            return default
        return user_input
    except KeyboardInterrupt:
        # Re-raise KeyboardInterrupt to be caught by the outer try-except block
        print("\n")  # Add some space after the ^C
        raise

def display_platform_data(data: List[Dict[str, Any]], title: str, platform: str, columns_config: List[Dict[str, Any]]) -> None:
    """
    Generic function to display platform data in a table.

    Args:
        data: List of dictionaries containing the data to display
        title: Title for the table
        platform: Platform name for styling ('youtube', 'instagram', or 'tiktok')
        columns_config: Configuration for table columns
    """
    if not data:
        print_warning(f"No {platform} data found.")
        return

    # Get platform-specific styling
    if platform.lower() == "youtube":
        border_style = YOUTUBE_BORDER_STYLE
        header_style = YOUTUBE_HEADER_STYLE
        text_style = YOUTUBE_TEXT_STYLE
    elif platform.lower() == "instagram":
        border_style = INSTAGRAM_BORDER_STYLE
        header_style = INSTAGRAM_HEADER_STYLE
        text_style = INSTAGRAM_TEXT_STYLE
    elif platform.lower() == "tiktok":
        border_style = TIKTOK_BORDER_STYLE
        header_style = TIKTOK_HEADER_STYLE
        text_style = TIKTOK_TEXT_STYLE
    else:
        border_style = "bright_blue"
        header_style = "bold bright_blue"
        text_style = "white"

    # Print a prominent title banner
    print_table_title(title, platform)

    # Get console width
    console_width = console.width

    # Create a table that expands to terminal width
    table = Table(
        border_style=border_style,
        expand=True,
        header_style=header_style,
        padding=(0, 2),
        collapse_padding=True,
        row_styles=["none", "none"],
        box=box.DOUBLE,
        safe_box=True
    )

    # Add columns based on configuration
    for col in columns_config:
        table.add_column(
            col["name"],
            style=col.get("style", text_style),
            width=col.get("width", int(console_width * col.get("width_pct", 0.1))),
            justify=col.get("justify", "left"),
            no_wrap=col.get("no_wrap", True),
            overflow=col.get("overflow", "ellipsis")
        )

    # Add rows
    for item in data:
        try:
            # Extract and format values based on columns configuration
            row_values = []
            for col in columns_config:
                field = col["field"]
                formatter = col.get("formatter")

                if formatter and callable(formatter):
                    # Use custom formatter function
                    value = formatter(item)
                else:
                    # Get value with default
                    value = item.get(field, col.get("default", ""))

                    # Apply basic formatting based on field type
                    if col.get("type") == "text" and isinstance(value, str):
                        value = clean_text_for_display(value)
                    elif col.get("type") == "number":
                        value = f"{value:,}"
                    elif col.get("type") == "percentage":
                        value = f"{value}%"

                row_values.append(value)

            table.add_row(*row_values)
        except Exception as e:
            # If there's an error processing a row, add a placeholder row
            error_row = ["(Error)"]
            error_row.append(f"Error processing data: {str(e)}")
            error_row.extend(["N/A"] * (len(columns_config) - 2))
            table.add_row(*error_row)

    console.print(table)

    # Print additional info if specified
    print_info(f"URLs for these {platform} items are available in the JSON output file.")


def display_youtube_videos(videos: List[Dict[str, Any]], title: str) -> None:
    """
    Display YouTube videos in a rich table.

    Args:
        videos: List of video dictionaries.
        title: Title for the table.
    """
    # Define column configuration
    columns_config = [
        {
            "name": "Username",
            "field": "channelTitle",
            "type": "text",
            "width_pct": 0.08,
            "style": YOUTUBE_TEXT_STYLE
        },
        {
            "name": "Title",
            "field": "title",
            "type": "text",
            "width_pct": 0.52,
            "style": YOUTUBE_TEXT_STYLE
        },
        {
            "name": "Views",
            "field": "viewCount",
            "type": "number",
            "width_pct": 0.08,
            "style": "bright_green",
            "justify": "right"
        },
        {
            "name": "Likes",
            "field": "likeCount",
            "type": "number",
            "width_pct": 0.08,
            "style": "bright_magenta",
            "justify": "right"
        },
        {
            "name": "Comments",
            "field": "commentCount",
            "type": "number",
            "width_pct": 0.08,
            "style": "bright_yellow",
            "justify": "right"
        },
        {
            "name": "Engagement",
            "field": "viewCount",  # Not directly used, but needed for formatter
            "formatter": lambda video: f"{calculate_youtube_engagement(video)}%",
            "width_pct": 0.08,
            "style": "bright_blue",
            "justify": "right"
        }
    ]

    display_platform_data(videos, title, "youtube", columns_config)


def calculate_youtube_engagement(video: Dict[str, Any]) -> float:
    """Calculate engagement rate for YouTube videos."""
    view_count = video.get('viewCount', 0)
    like_count = video.get('likeCount', 0)
    comment_count = video.get('commentCount', 0)

    engagement_rate = 0
    if view_count > 0:
        engagement = like_count + comment_count
        engagement_rate = round((engagement / view_count) * 100, 2)

    return engagement_rate

def display_instagram_reels(reels: List[Dict[str, Any]], title: str) -> None:
    """
    Display Instagram reels in a rich table.

    Args:
        reels: List of reel dictionaries.
        title: Title for the table.
    """
    # Define column configuration
    columns_config = [
        {
            "name": "Username",
            "field": "username",
            "type": "text",
            "width_pct": 0.08,
            "style": INSTAGRAM_TEXT_STYLE
        },
        {
            "name": "Caption",
            "field": "caption",
            "type": "text",
            "width_pct": 0.50,
            "style": INSTAGRAM_TEXT_STYLE
        },
        {
            "name": "Views",
            "field": "view_count",
            "type": "number",
            "width_pct": 0.07,
            "style": "bright_green",
            "justify": "right"
        },
        {
            "name": "Likes",
            "field": "like_count",
            "type": "number",
            "width_pct": 0.07,
            "style": "bright_red",
            "justify": "right"
        },
        {
            "name": "Comments",
            "field": "comment_count",
            "type": "number",
            "width_pct": 0.07,
            "style": "bright_yellow",
            "justify": "right"
        },
        {
            "name": "Engagement",
            "field": "engagement_rate",
            "type": "percentage",
            "width_pct": 0.07,
            "style": "bright_blue",
            "justify": "right"
        }
    ]

    display_platform_data(reels, title, "instagram", columns_config)

def display_tiktok_videos(videos: List[Dict[str, Any]], title: str) -> None:
    """
    Display TikTok videos in a rich table.

    Args:
        videos: List of video dictionaries.
        title: Title for the table.
    """
    # Define column configuration
    columns_config = [
        {
            "name": "Username",
            "field": "username",
            "type": "text",
            "width_pct": 0.08,
            "style": TIKTOK_TEXT_STYLE
        },
        {
            "name": "Caption",
            "field": "caption",
            "type": "text",
            "width_pct": 0.45,
            "style": TIKTOK_TEXT_STYLE
        },
        {
            "name": "Views",
            "field": "views",
            "type": "number",
            "width_pct": 0.07,
            "style": "bright_green",
            "justify": "right"
        },
        {
            "name": "Likes",
            "field": "likes",
            "type": "number",
            "width_pct": 0.07,
            "style": "bright_red",
            "justify": "right"
        },
        {
            "name": "Comments",
            "field": "comments",
            "type": "number",
            "width_pct": 0.07,
            "style": "bright_yellow",
            "justify": "right"
        },
        {
            "name": "Shares",
            "field": "shares",
            "type": "number",
            "width_pct": 0.05,
            "style": "bright_blue",
            "justify": "right"
        },
        {
            "name": "Engagement",
            "field": "engagement_rate",
            "type": "percentage",
            "width_pct": 0.07,
            "style": "bright_cyan",
            "justify": "right"
        }
    ]

    display_platform_data(videos, title, "tiktok", columns_config)

def run_with_spinner(func: Callable, description: str, platform: str = None, *args, **kwargs) -> Any:
    """
    Run a function with an engaging spinner animation suitable for social media automation.

    Args:
        func: The function to run.
        description: Description to show next to the spinner.
        platform: Optional platform name ('youtube', 'instagram', or 'tiktok') for styling.
        *args: Arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        The result of the function.
    """
    # Create a platform-specific spinner
    with create_spinner(description, platform) as progress:
        task_id = progress.add_task(description, total=None)
        try:
            # Execute the function
            result = func(*args, **kwargs)

            # Update the spinner to show completion
            progress.update(task_id, completed=True)

            # Return the result
            return result
        except Exception as e:
            # Update the spinner to show completion even on error
            progress.update(task_id, completed=True)

            # Re-raise the exception
            raise e



def welcome_screen() -> None:
    """Display a welcome screen for SocialSpyAgent."""
    console.clear()
    print_ascii_banner("SocialSpyAgent")
    print_panel(
        "Welcome to SocialSpyAgent - Your Social Media Intelligence Tool",
        title="About"
    )
    print_info("This tool helps you gather intelligence from various social media platforms.")
    print_info("Currently supporting: YouTube, Instagram, and TikTok")
    print()
    time.sleep(1)  # Pause for dramatic effect

def exit_screen() -> None:
    """Display a goodbye screen for SocialSpyAgent."""
    console.clear()
    print_ascii_banner("Keep spyin'!", font="big", style="bold green")
    print_panel(
        "SocialSpyAgent has completed all operations successfully.",
        title="Goodbye"
    )
    print_info("Your data has been saved to the output directory.")
    print_info("Feel free to run the tool again anytime!")
    print()
