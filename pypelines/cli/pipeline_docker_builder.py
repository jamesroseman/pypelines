import os
import pkg_resources
import subprocess


def build_docker_image(dockerfile_path: str, name: str, build_context: str):
    # Set the Docker environment to Minikube's Docker daemon
    minikube_docker_env_command = ["minikube", "docker-env"]
    result = subprocess.run(minikube_docker_env_command, capture_output=True, text=True, check=True)

    # Extract and set the environment variables accordingly
    for line in result.stdout.splitlines():
        if line.startswith('export'):
            key, value = line.replace('export ', '').split('=', 1)
            os.environ[key] = value.strip('"')

    # Build the Docker image
    command = [
        "docker", "build", "--tag", name, "--file", dockerfile_path, build_context
    ]
    print(command)
    subprocess.run(command, check=True)


def build_pipeline_docker_images(build_context: str):
    """Builds Docker images for each pipeline."""
    # Build the Beam base image.
    beam_dockerfile_path = pkg_resources.resource_filename(__name__, "../deployment/docker/Dockerfile.beam")
    build_docker_image(beam_dockerfile_path, "pypelines-beam:1.16", build_context)
    # Build the Beam harness base image.
    beam_harness_base_dockerfile_path = pkg_resources.resource_filename(
        __name__, "../deployment/docker/Dockerfile.beam-harness-base",
    )
    build_docker_image(
        beam_harness_base_dockerfile_path,
        "pypelines-beam-harness-base:2.56",
        pkg_resources.resource_filename(__name__, "..")
    )
    # Build the Beam harness image (which is dependent on the harness base image).
    beam_harness_dockerfile_path = pkg_resources.resource_filename(
        __name__,
        "../deployment/docker/Dockerfile.beam-harness",
    )
    build_docker_image(
        beam_harness_dockerfile_path,
        "pypelines-beam-harness:2.56",
        build_context,
    )
