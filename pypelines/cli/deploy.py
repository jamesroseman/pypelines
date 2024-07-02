import os
import pkg_resources
import subprocess
from typing import List

from rich.console import Console


def deploy_pipeline(
    pipeline_name: str,
    cluster_yaml_path: str,
    job_yaml_path: str,
    console: Console,
) -> None:
    """Deploys a pipeline, assuming the file paths are valid."""
    console.print(f"Deleting existing {pipeline_name} cluster deployment, if it exists...")
    subprocess.run([
        'kubectl', 'delete', 'flinkdeployment.flink.apache.org', f'{pipeline_name}-cluster', '--ignore-not-found',
    ], check=True)
    console.print(f"Successfully deleted {pipeline_name} cluster deployment.", style="bold green")

    console.print(f"Starting {pipeline_name} cluster deployment...")
    subprocess.run([
        'kubectl', 'apply', '-f', cluster_yaml_path,
    ], check=True)
    console.print(f"Successfully deployed {pipeline_name} cluster deployment.", style="bold green")

    console.print(f"Deleting existing {pipeline_name} job deployment, if it exists...")
    subprocess.run([
        'kubectl', 'delete', 'jobs.batch', f'{pipeline_name}-job', '--ignore-not-found',
    ], check=True)
    console.print(f"Successfully deleted {pipeline_name} job deployment.", style="bold green")

    console.print(f"Starting {pipeline_name} job deployment...")
    subprocess.run([
        'kubectl', 'apply', '-f', job_yaml_path,
    ], check=True)
    console.print(f"Successfully deployed {pipeline_name} job deployment.", style="bold green")


def deploy_pipelines(pipelines_file_paths: List[str], console: Console) -> None:
    """Deploys pipelines, assuming that a _cluster.yaml and _job.yaml file exists for each."""
    for pipeline_file_path in pipelines_file_paths:
        pipeline_name = os.path.splitext(os.path.basename(pipeline_file_path))[0]
        deployment_path = pkg_resources.resource_filename(__name__, f"../deployment/dist/{pipeline_name.replace('-', '_')}")
        # Get the cluster.yaml file for the pipeline.
        cluster_yaml_name = f"{pipeline_name}_cluster.yaml"
        cluster_yaml_path = os.path.join(deployment_path, cluster_yaml_name)
        if not os.path.exists(cluster_yaml_path):
            raise FileNotFoundError(f"Could not find {cluster_yaml_path}")
        # Get the job.yaml file for the pipeline.
        job_yaml_name = f"{pipeline_name}_job.yaml"
        job_yaml_path = os.path.join(deployment_path, job_yaml_name)
        if not os.path.exists(job_yaml_path):
            raise FileNotFoundError(f"Could not find {job_yaml_path}")
        # Deploy the pipeline.
        console.print(f"Attempting to deploy {pipeline_name} pipeline...")
        deploy_pipeline(pipeline_name, cluster_yaml_path, job_yaml_path, console)
        console.print(f"{pipeline_name} pipeline deployed successfully!", style="bold green")
