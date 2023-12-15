import subprocess
def setup_environment():
    """
    Sets up the environment by installing Java, Docker, and Nextflow.
    """
    def install_software(name, check_command, install_commands):
        """
        Helper function to install software if not already installed.
        """
        try:
            subprocess.run(check_command, stderr=subprocess.STDOUT, check=True)
            print(f"{name} is already installed.")
        except subprocess.CalledProcessError:
            print(f"you should install {name}...")
            for command in install_commands:
                subprocess.run(command, check=True)

    install_software(
        "Java", ["java", "-version"],
        [["apt-get", "update"], ["apt-get", "install", "-y", "default-jdk"]]
    )

    install_software(
        "Docker", ["docker", "--version"],
        [["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"], ["sh", "get-docker.sh"]]
    )

    install_software(
        "Nextflow", ["nextflow", "-version"],
        [["curl", "-s", "https://get.nextflow.io", "|", "bash"]]
    )

def run_wf_tb_amr(fastq_data_path):
    """
    Runs the wf-tb-amr workflow using Nextflow with the specified FASTQ data path.
    """
    sample_sheet_path = fastq_data_path + '/sample_sheet.csv'
    command = [
        "nextflow",
        "run",
        "epi2me-labs/wf-tb-amr",
        "--fastq", fastq_data_path,
        "--sample_sheet", sample_sheet_path,
    ]
    subprocess.run(command, check=True)

def main(fastq_data_path : str):
    """
    Main function to execute the script.
    """
    run_wf_tb_amr(fastq_data_path)
