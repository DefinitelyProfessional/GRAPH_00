from rich import box
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.columns import Columns
from rich.text import Text

# To ensure reliable and safe clear terminal
from os import name as os_name
from subprocess import run as sub_run

class UI_MANAGER:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        
        # Define the structural grid once
        self.layout.split_column(
            Layout(name="header", size=9),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        self.layout["body"].split_row(
            Layout(name="sidebar", ratio=1, minimum_size=25),
            Layout(name="content", ratio=4)
        )

        # Pre-build static elements
        self.menu_table = self._build_menu_table()
        self.layout["header"].update(self._build_banner())
        self.layout["sidebar"].update(Panel(self.menu_table, title="[bold cyan]Action Menu", border_style="cyan"))
        
        # Initial states
        self.set_content("Welcome", Text("Select an option from the menu to begin.", style="dim"))
        self.set_status("System ready.", "green")



    def select_file_from_directory(self, directory_path) -> str:
        """
        Scans the directory for .csv files, displays them in the 'content' area, and prompts the user for a selection.
        """
        # Gather list of .csv files
        files = sorted([f.name for f in directory_path.iterdir() if f.is_file() and f.suffix == '.csv'])
        
        if not files:
            self.set_content("Error", "[bold red]No .csv files found in the data directory![/]", color="red")
            self.set_status("Missing data files.", "red")
            self.prompt("Press Enter to Cancel and Return")
            return None

        # Build a display table for the 'content' window
        file_table = Table(box=box.SIMPLE, show_header=True, expand=True)
        file_table.add_column("No", justify="center", style="cyan", width=3)
        file_table.add_column("Available Data Files", style="white")
        
        valid_choices = []
        for i, filename in enumerate(files, 1):
            valid_choices.append(str(i))
            file_table.add_row(str(i), filename)

        # Update UI state
        self.set_content("File Selection", file_table, color="yellow")
        self.set_status("Awaiting file selection...", "yellow")
        
        # Get user selected file        
        return files[int(self.prompt("Enter file number", choices=valid_choices, default="1")) - 1]

    def clear_terminal(self):
        """Clear terminal buffer, Ensure predictable rich UI display"""
        if os_name == "nt": sub_run(["cmd", "/c", "cls"])
        else: sub_run(["clear"])

    def _build_banner(self):
        """Generates the static banner"""
        banner_text = (
            " ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗         ██████╗  ██████╗ \n"
            "██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║        ██╔═████╗██╔═████╗\n"
            "██║  ███╗██████╔╝███████║██████╔╝███████║        ██║██╔██║██║██╔██║\n"
            "██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║        ████╔╝██║████╔╝██║\n"
            "╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║███████╗╚██████╔╝╚██████╔╝\n"
            " ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ "
        )
        colors = ["cyan", "bright_cyan", "blue", "magenta", "bright_magenta"]
        gradient_text = Text()
        
        for index, char in enumerate(banner_text):
            color = colors[index % len(colors)] if char not in ('\n', ' ') else "white"
            gradient_text.append(char, style=f"bold {color}")

        subtitle = Text.from_markup("\n[bold white]Presented By UAS[3]:[/] [cyan]Stephen[/], [bright_cyan]Neil[/], [blue]Joshua[/], [magenta]Nehemy[/]")
        gradient_text.append(subtitle)
        
        return Panel(gradient_text, box=box.SIMPLE)

    def _build_menu_table(self):
        """Builds the menu table once"""
        table = Table(box=box.SIMPLE, show_header=True, expand=True)
        table.add_column("No", justify="center", style="cyan", width=2)
        table.add_column("Feature", style="white")
        
        table.add_row("1", "Reset Window Display")
        table.add_row("2", "Show ALL nodes")
        table.add_row("3", "Find shortest path")
        table.add_row("4", "Generate MST")
        table.add_row("5", "Change input file")
        table.add_row("0", "Exit")
        return table

    def set_content(self, title: str, renderable, color="blue"):
        """Swaps out the main viewing area content"""
        self.layout["content"].update(Panel(renderable, title=f"[bold]{title}", border_style=color))

    def set_status(self, message: str, color="cyan"):
        """Updates the footer status bar"""
        self.layout["footer"].update(Panel(f"[{color}]{message}[/{color}]", title="Status", border_style="dim"))

    def generate_mst_table(self, mst_edges, limit: int = 20) -> Table:
        """Returns a Table object for the MST rather than printing it"""
        table = Table(box=box.ROUNDED, expand=True)
        table.add_column("Source", style="cyan")
        table.add_column("Destination", style="cyan")
        table.add_column("Weight", justify="right", style="magenta")

        if not mst_edges:
            table.add_row("No edges found", "", "")
            return table

        for index, edge in enumerate(sorted(mst_edges)):
            if index >= limit:
                table.add_row("...", "...", "...")
                break
            src, dst, weight = edge
            table.add_row(str(src), str(dst), f"{weight:.2f}")
        return table

    def prompt(self, prompt_text: str, choices: list = None, default: str = None):
        """Clears screen, renders the full UI, and captures input safely."""
        # Use OS clear for a true full-screen reset, avoiding scrollback clutter
        self.clear_terminal()
        
        # Calculate height to be 2-3 lines shorter than the actual terminal height
        reserved_height = self.console.height - 3
        
        # Wrap the layout in a fixed-height container for this render
        self.console.print(self.layout, height=reserved_height)
        
        if choices: return Prompt.ask(f"\n[bold yellow]{prompt_text}[/]", choices=choices, default=default)
        return Prompt.ask(f"\n[bold yellow]{prompt_text}[/]")

    # ========================================================================================================
    def display_nodes(self, nodenames: list):
        """Janky way to display ALL nodes but must resize to fit ..."""
        # Style the names to make them pop
        node_renderables = [Text(f"{name}", style="bright_blue") for name in nodenames]
        # Columns will wrap automatically based on terminal width
        grid = Columns(node_renderables, padding=(0, 2), equal=True, expand=True)
        self.set_content("List of ALL Nodes (if it fits the screen)", grid, color="cyan")
    
    # ========================================================================================================
    def display_traversal(self, traversal_paths:list, total_wgh_sum:int):
        """Display the traversal Paths"""
        table = Table(box=box.SIMPLE, show_header=True, expand=True)
        table.add_column("Traversal Path", justify="center", style="cyan", width=2)
        for path in traversal_paths: table.add_row(path)
        table.add_row(f"TOTAL WEIGHT = {total_wgh_sum}")
        self.set_content("Shortest Path (Dijkstra)", table, color="green")