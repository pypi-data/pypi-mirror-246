
# nanopore_alignment

A Python package for nanopore sequence alignment and primer design. This package provides tools to set up an environment for nanopore sequence analysis and to design primers from DNA sequences.

## Introduction

The primer Design function is to optimize primer design from a given fasta file. Currently, it is working with a single sequence (a single fasta file)


The Sequence Alignment function is a subprocess of the "wf_tb_amr" workflow from Nanopore Sequencing. It is a workflow for determining the antibiotic resistance of Mycobacterium tuberculosis targeted sequencing samples and provides the alignment information to the reference genome.
## Prerequisites

Before installing `nanoSeq`, ensure that you have the following software installed on your system:


- **Java**: Java is used for running various bioinformatics tools. You can download it from the [official Java website](https://www.java.com/en/download/).

- **Docker**: Docker is used for running software in isolated containers, ensuring that they work consistently on any system. You can download it from the [official Docker website](https://www.docker.com/products/docker-desktop).

- **Nextflow**: Nextflow is a workflow management system that simplifies the deployment of complex computational pipelines. You can download it from the [official Nextflow website](https://www.nextflow.io/).

Please ensure these are installed on your system before using nanoSeq.
These are external dependencies that cannot be installed via pip and need to be set up separately.




## Installation

To install the `nanopore_alignment` package, follow these steps:

   pip install nanoseq

## Usage

### Sequence Alignment

Important: `fastq_data_path` should be the directory containing the `sample_sheet.csv` and the subfolders with the fastq files, not the folder directly containing the fastq files.
e.g. The test_nanopore folder contains the accurate structure and all the files to run the function. Your 'fastq_data_path' should be pointing to this folder instead of the individual fastq files.
```
+-- ./fastq_data_path/
|   +-- sample_sheet.csv
|   +-- /barcode00/
|       +-- barcode00_sample.fastq(.gz)
|   +-- /barcode01/
|       +-- barcode01_sample.fastq(.gz)
```

This workflow also requires a sample sheet which identifies test samples and controls. The sample sheet must have three columns: `barcode`, `alias`, and `type`:
- `barcode`: the barcode of the sample (e.g., barcode02).
- `alias`: a unique identifier for the sample.
- `type`: can be `test_sample`, `positive_control`, or `no_template_control`.

### Sequence Alignment Workflow Details

- Align reads to NC_000962.3 reference genome (minmap2)
- Use mpileup to determine base composition of pre-defined variants, “genotyping” (bcftools)
- Phase variants (whatshap)
- Report results

To run sequence alignment:

```python
from nanoporeAlignment import nanoAlign

# Path to the directory containing 'sample_sheet.csv' and subfolders with fastq files

fastq_data_path = 'path/to/your/folder_with_samplesheet_and_sub_folders'
nanoAlign.main(fastq_data_path)
```

** Note: If you want to compare the alignment result in Geneious Prime, you can use the bam file generated and the "NC_000962.3.fasta" file in the TB Data file for demo comparison.


### Primer Design

To design primers from a DNA sequence:

```python
from primer_design import primerdesign

# Path to your FASTA file - e.g. the path to the 'reference_primer' file in the 'test_primer' folder
fasta_file = 'path/to/your/fasta/file.fasta'

primerdesign.main(fasta_file)

# Process or print your primers as needed


```
## Unit Testing

Unit tests are included in the `test_` directory of this project. These tests cover the main functions of the `nanoAlign` and `primerdesign` modules.

To run the unit tests, navigate to the `test_` directory and run the following command:

```bash
python -m unittest Test_Unitest.py
```

This will run all the test methods in the `TestNanoSeq` test case class. Each test method tests a specific function in the `nanoAlign` or `primerdesign` module.

Here's a brief description of each test method:

- `test_nanoAlign_main`: This test checks if the `nanoAlign.main` function generates the expected output files.

- `test_primerdesign_read_fasta`: This test checks if the `primerdesign.read_fasta` function returns a string.

- `test_primerdesign_get_complementary_sequence`: This test checks if the `primerdesign.get_complementary_sequence` function returns a string.

- `test_primerdesign_design_primers`: This test checks if the `primerdesign.design_primers` function returns a list.

- `test_primerdesign_check_dimerization`: This test checks if the `primerdesign.check_dimerization` function returns a boolean.

- `test_primerdesign_main`: This test checks if the `primerdesign.main` function generates the expected output files.

If all the tests pass, this indicates that the functions in the `nanoAlign` and `primerdesign` modules are working as expected. If any test fails, this indicates a potential issue with the function being tested.


If you are testing the software locally, from the whl file, the following needs to be done in order to setup the veritual environment:

## Local Virtual Environment Setup (This is for testing the package locally without downloading from PyPI) 

To set up a local environment for package testing, follow these steps:

1. **Generate distribution archives**: Navigate to the directory containing the `setup.py` file and run the following command to create a source distribution archive (.tar.gz file) and a built distribution (.whl file):

    ```bash
    python setup.py sdist bdist_wheel
    ```

2. **Create a virtual environment**: Create a new virtual environment named `test_env`. A virtual environment is an isolated Python environment where you can install packages without affecting your global Python installation:

    ```bash
    python -m venv test_env
    ```

3. **Activate the virtual environment**: Activate the `test_env` virtual environment. After activation, any packages installed will be installed to this environment, and Python will use this environment's version and packages:

    ```bash
    source test_env/bin/activate
    ```

4. **Install the package**: Navigate to the directory containing the .whl file (the `<dist>` directory) and install the package in the current Python environment:

    ```bash
    pip install nanoSeq-0.1-py3-none-any.whl
    ```
    
5. **List installed packages**: You can list all the installed packages in the current Python environment with the following command:

    ```bash
    pip list
    ```


Now, your local environment is set up and ready for package testing.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/hgu1uw/UW_BIOEN537/blob/71fcb6fdbf6b4f99d18303e0e0bb32ac0ee0acbd/LICENSE) file for details.

## Contact

For any queries or further assistance, please reach out to Nello at hgu1@uw.edu.
