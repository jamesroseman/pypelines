import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from .config import load_config, get_pipeline_file_paths
from .yaml_generator import generate_pipeline_yaml_files

console = Console()


@click.command()
@click.option('--config', default='pypelines.toml', help='Path to the pypelines.toml configuration file')
def main(config):
    # Display a welcome banner.
    banner = """
        ██████╗ ██╗   ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗███████╗
        ██╔══██╗██║   ██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝██╔════╝
        ██████╔╝██║   ██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗  ███████╗
        ██╔═══╝ ██║   ██║██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  ╚════██║
        ██║     ╚██████╔╝██║     ███████╗███████╗██║██║ ╚████║███████╗███████║
        ╚═╝      ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
        """
    console.print(Panel(Text(banner, style="bold cyan"), box=box.ASCII_DOUBLE_HEAD, expand=False))

    # Load the configuration file.
    console.print(f"Loading configuration from {config}", style="bold green")
    config_data = load_config(config)

    # Get and display all pipelines found in the project.
    pipeline_files = get_pipeline_file_paths(config_data)
    table = Table(title="Pipeline Files")
    table.add_column("File Path", style="cyan", no_wrap=True)
    for file in pipeline_files:
        table.add_row(file)
    console.print(table)

    # Generate YAML distribution files for each pipeline.
    if click.confirm(
        "Continue generating YAML distribution files for these pipelines?",
        default=False,
    ):
        generate_pipeline_yaml_files(pipeline_files)
        console.print(f"{len(pipeline_files)} YAML distribution files generated...", style="green")
    else:
        console.print("YAML generation aborted.", style="bold red")


if __name__ == "__main__":
    main()
