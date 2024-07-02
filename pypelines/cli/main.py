import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import load_config, get_pipeline_file_paths
from .deploy import deploy_pipelines
from .pipeline_yaml_generator import generate_pipeline_yaml_files
from .pipeline_docker_builder import build_pipeline_docker_images


console = Console()


@click.group()
def cli():
    pass


def print_banner():
    """Displays a banner."""
    banner = """
            ██████╗ ██╗   ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗███████╗
            ██╔══██╗██║   ██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝██╔════╝
            ██████╔╝██║   ██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗  ███████╗
            ██╔═══╝ ██║   ██║██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  ╚════██║
            ██║     ╚██████╔╝██║     ███████╗███████╗██║██║ ╚████║███████╗███████║
            ╚═╝      ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
            """
    console.print(Panel(Text(banner, style="bold cyan"), box=box.ASCII_DOUBLE_HEAD, expand=False))


@click.command()
@click.option('--config', default='pypelines.toml', help='Path to the pypelines.toml configuration file')
def deploy(config):
    print_banner()

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

    # Generate distribution files for each pipeline.
    if click.confirm(
        "Continue generating distribution files for these pipelines?",
        default=False,
    ):
        # Building the Docker images.
        build_pipeline_docker_images(".")  # Build context could be changed to be configurable later.
        console.print(f"{len(pipeline_files)} Docker images built...", style="green")
        # Generate the YAML files.
        generate_pipeline_yaml_files(pipeline_files)
        console.print(f"{len(pipeline_files) * 2} YAML distribution files generated...", style="green")
    else:
        console.print("YAML generation aborted.", style="bold red")

    # Deploy all pipelines.
    if click.confirm(
        "Deploy all pipelines?",
        default=False,
    ):
        deploy_pipelines(pipeline_files, console)
        console.print(f"{len(pipeline_files)} pipelines deployed...", style="green")


def main():
    cli.add_command(deploy)
    cli()


if __name__ == "__main__":
    main()
