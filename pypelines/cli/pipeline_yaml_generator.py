import logging
import os
import pkg_resources
from typing import Any, List

import jinja2
import yaml


def load_template(template_file: str) -> jinja2.Template:
    """Loads template YAML file."""
    template_dir = pkg_resources.resource_filename(__name__, "../deployment/beam")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    return template


def render_template(template: jinja2.Template, context: dict[str, Any]) -> str:
    """Renders the template by interpolating variables in the context."""
    return template.render(context)


def save_yaml(content, output_path: str):
    """Saves the new generated YAML file."""
    with open(output_path, "w") as file:
        yaml.dump(yaml.safe_load(content), file, default_flow_style=False)


def generate_pipeline_yaml_files(pipelines_file_paths: List[str]) -> None:
    """Generates cluster and job deployment YAMLs for every pipeline.

    Args:
        pipelines_file_paths: List of file paths to pipelines.
    """
    cluster_template = load_template("pipeline-cluster-template.yaml")
    job_template = load_template("pipeline-job-template.yaml")

    for pipeline_file_path in pipelines_file_paths:
        pipeline_name = os.path.splitext(os.path.basename(pipeline_file_path))[0]
        output_dir = pkg_resources.resource_filename(__name__, f"../deployment/dist/{pipeline_name}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        context = {
            'PIPELINE_NAME': pipeline_name.replace("_", "-"),
            'PIPELINE_FILE_PATH': pipeline_file_path,
        }
        # Render and save cluster YAML.
        cluster_yaml_content = render_template(cluster_template, context)
        cluster_file_path = os.path.join(output_dir, f"{pipeline_name}_cluster.yaml")
        save_yaml(cluster_yaml_content, cluster_file_path)
        logging.debug(f"Wrote {pipeline_name} cluster YAML to {cluster_file_path}")
        # Render and save job YAML
        job_yaml_content = render_template(job_template, context)
        job_file_path = os.path.join(output_dir, f"{pipeline_name}_job.yaml")
        save_yaml(job_yaml_content, job_file_path)
        logging.debug(f"Wrote {pipeline_name} job YAML to {job_file_path}")
