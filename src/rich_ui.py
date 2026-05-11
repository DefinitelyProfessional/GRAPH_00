from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

class UI_MANAGER:
    def __init__(self):
        self.CONSOLE = Console()
        self.MAINMENU = Table(title="Main Menu", box=box.ROUNDED, show_header=True)

    def show_title(self):
        banner = [
            "  ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗         ██████╗  ██████╗ ",
            " ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║        ██╔═████╗██╔═████╗",
            " ██║  ███╗██████╔╝███████║██████╔╝███████║        ██║██╔██║██║██╔██║",
            " ██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║        ████╔╝██║████╔╝██║",
            " ╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║███████╗╚██████╔╝╚██████╔╝",
            "  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ",
        ]
        colors = ["cyan", "bright_cyan", "blue", "magenta", "bright_magenta"]

        self.CONSOLE.print()
        for line in banner:
            gradient_line = Text()
            for index, char in enumerate(line):
                color = colors[index % len(colors)]
                gradient_line.append(char, style=f"bold {color}")
            self.CONSOLE.print(gradient_line)

        self.CONSOLE.print(
            "[bold white]Presented By UAS[3]:[/bold white] [cyan]Stephen[/cyan], ",
            "[bright_cyan]Neil[/bright_cyan], [blue]Joshua[/blue], ",
            "[magenta]Nehemy[/magenta]"
        )
        self.CONSOLE.print()


    def choose_input_file(self):
        # TODO dont make static files like this, must display whole of data directory,
        # make use of the Path object from pathlib
        self.CONSOLE.print("[bold]Choose CSV file to process:[/bold]")
        self.CONSOLE.print("1) relations.csv")
        self.CONSOLE.print("2) directed_relations.csv")
        self.CONSOLE.print("3) undirected_relations.csv")

        choice = Prompt.ask("Enter number", choices=["1", "2", "3"], default="1")

        if choice == "1":
            return "relations.csv"
        if choice == "2":
            return "directed_relations.csv"
        return "undirected_relations.csv"


    def show_main_menu(self):
        self.CONSOLE.print()

        # TODO add column on each function call causes accumulating duplicates
        self.MAINMENU.add_column("No", justify="center", style="cyan", width=4)
        self.MAINMENU.add_column("Feature", style="white")
        self.MAINMENU.add_column("Description", style="dim")

        self.MAINMENU.add_row("1", "Display Main Menu", "In case you forgot your choices")
        self.MAINMENU.add_row("2", "Display all nodes", "This will may be dubiously long")
        self.MAINMENU.add_row("3", "Find shortest path", "With the Legendary Dijkstra's")
        self.MAINMENU.add_row("4", "Generate MST", "Prim Algorithm and save to file")
        self.MAINMENU.add_row("5", "Change input file", "Choose a different input CSV")
        self.MAINMENU.add_row("0", "Exit", "Close program")

    def get_choice(self):
        self.CONSOLE.print(self.MAINMENU)
        return Prompt.ask("Your choice", choices=["0", "1", "2", "3", "4", "5"], default="1")


    def show_section(self, title, color="cyan"):
        self.CONSOLE.print()
        self.CONSOLE.print(Panel(f"[bold]{title}[/bold]", border_style=color))


    def ask_shortest_path_nodes(self):
        start = Prompt.ask("Start node : ")
        end   = Prompt.ask("End node   : ")
        return start, end


    def ask_mst_output_file(self):
        return Prompt.ask("MST output file name", default="MST_relations.csv")


    def show_mst_preview(self, mst_edges, limit: int = 20):
        if not mst_edges:
            self.show_error("Graph is empty or MST not found.")
            return
        MST_table = Table(title=f"Preview MST {limit} edges", box=box.SIMPLE)
        MST_table.add_column("src", style="cyan")
        MST_table.add_column("dst", style="cyan")
        MST_table.add_column("wgh", justify="right", style="magenta")

        for index, edge in enumerate(sorted(mst_edges)):
            if index >= limit:
                break
            src, dst, weight = edge
            MST_table.add_row(src, dst, f"{weight:.2f}")

        self.CONSOLE.print(MST_table)


    def show_success(self, message):
        self.CONSOLE.print(f"[green]{message}[/green]")


    def show_error(self, message):
        self.CONSOLE.print(f"[red]{message}[/red]")


    def show_goodbye(self):
        self.CONSOLE.print("[bold cyan]Thank you, goodbye![/bold cyan]")