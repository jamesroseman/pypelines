import logging
import os
import pkg_resources
from typing import Any, List

import jinja2


def load_template(template_file: str) -> jinja2.Template:
    """Loads template YAML file."""
    template_dir = pkg_resources.resource_filename(__name__, "../deployment/docker")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    return template


def render_template(template: jinja2.Template, context: dict[str, Any]) -> str:
    """Renders the template by interpolating variables in the context."""
    return template.render(context)


def save_dockerfile(content, output_path: str):
    """Saves the new generated Dockerfile"""
    with open(output_path, "w") as file:
        file.write(content)


def generate_pipeline_docker_files(pipelines_file_paths: List[str]) -> None:
    """Generates base and harness Dockerfiles for every pipeline.

    Args:
        pipelines_file_paths: List of file paths to pipelines.
        source_dir: The root directory for the pipelines, which have to be mounted into the
            harness Dockerfile.
    """
    base_template = load_template("Dockerfile.beam")
    harness_template = load_template("Dockerfile.beam-harness")
    for pipeline_file_path in pipelines_file_paths:
        pipeline_name = os.path.splitext(os.path.basename(pipeline_file_path))[0]
        output_dir = pkg_resources.resource_filename(__name__, f"../deployment/dist/{pipeline_name}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        context = {
            'SOURCE_DIR': source_dir,
        }
        # Render and save base Dockerfile.
        base_content = render_template(base_template, context)
        base_file_path = os.path.join(output_dir, f"Dockerfile.{pipeline_name.replace('_', '-')}-beam")
        save_dockerfile(base_content, base_file_path)
        # Render and save harness Dockerfile.
        harness_content = render_template(harness_template, context)
        harness_file_path = os.path.join(output_dir, f"Dockerfile.{pipeline_name.replace('_', '-')}-beam-harness")
        save_dockerfile(harness_content, harness_file_path)


def build_pipeline_docker_images()