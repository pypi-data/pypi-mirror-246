import itertools
import os

def read_fasta(file):
    """
    Reads a FASTA file and returns the first sequence found in the file.
    """
    with open(file, 'r') as fasta_file:
        for line in fasta_file:
            if line.startswith('>'):
                continue
            return line.strip()

def get_complementary_sequence(sequence):
    """
    Generates the complementary DNA sequence for a given DNA sequence.
    """
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement[base] for base in sequence)

def design_primers(sequence, primer_len=20):
    """
    Designs primers from a given sequence, avoiding high GC content and complementary sequences.

    Parameters:
    sequence (str): The DNA sequence for which primers are to be designed.
    primer_len (int, optional): The length of the primers to be designed. Defaults to 20.

    Returns:
    list: A list of primer sequences designed from the input sequence.
    """
    primers = []
    max_gc_content = 0.60
    min_gc_content = 0.40

    def is_complementary(seq1, seq2):
        """
        Checks if two sequences are complementary to each other.

        Parameters:
        seq1 (str): The first sequence.
        seq2 (str): The second sequence.

        Returns:
        bool: True if the sequences are complementary, False otherwise.
        """
        comp_dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        return all(comp_dict[base1] == base2 for base1, base2 in zip(seq1, seq2[::-1]))

    def gc_content(primer):
        """
        Calculates the GC content of a primer.

        Parameters:
        primer (str): The primer sequence.

        Returns:
        float: The GC content of the primer as a proportion of the total length.
        """
        return (primer.count('G') + primer.count('C')) / len(primer)

    for i in range(len(sequence) - primer_len + 1):
        primer = sequence[i:i + primer_len]
        if min_gc_content <= gc_content(primer) <= max_gc_content:
            if not any(is_complementary(primer, other_primer) for other_primer in primers):
                primers.append(primer)

    return primers
def check_dimerization(primer1:str, primer2:str, threshold=4):
    """
    Checks for potential dimerization between two primers.

    Parameters:
    primer1 (str): The first primer sequence.
    primer2 (str): The second primer sequence.
    threshold (int, optional): The length of the complementary sequence that would indicate dimerization. Defaults to 4.

    Returns:
    bool: True if dimerization is possible, False otherwise.
    """
    for i in range(len(primer1)):
        for j in range(len(primer2)):
            if primer1[i:i+threshold] == primer2[j:j+threshold]:
                return True
    return False

def print_sequence_with_primer(sequence:str, primers:str, specific_primer=None):
    """
    Prints the entire sequence with the primer.
    If no specific primer is provided, the first primer in the list is used.

    Parameters:
    sequence (str): The DNA sequence from which the primers were designed.
    primers (list): A list of designed primer sequences.
    specific_primer (str, optional): A specific primer sequence in the sequence. Defaults to None.

    Returns:
    the entire sequence with the primer
    """
    primer_to_use = specific_primer if specific_primer else primers[0]
    primer_index = sequence.find(primer_to_use)

    if primer_index != -1:
        primer_sequence = (sequence[:primer_index]  + primer_to_use  +
                                sequence[primer_index + len(primer_to_use):])
        print(f"Primer: {primer_to_use}\nSequence with Primer : {primer_sequence}")

    else:
        print("Specified primer not found in the sequence.")


def write_to_fasta(filename, sequence, input_file_path):
    """
    Writes the sequence to a FASTA file.
    """
    directory = os.path.dirname(input_file_path)
    file_path = os.path.join(directory, filename)

    with open(file_path, 'w') as file:
        file.write(">Highlighted_Sequence\n")
        file.write(sequence + '\n')


def main(data_path):
    """
    Main function to design primers from a sequence.
    """

    reference_data = data_path
    sequence1 = read_fasta(reference_data)
    sequence2 = get_complementary_sequence(sequence1)

    primers1 = design_primers(sequence1, primer_len=20)
    primers2 = design_primers(sequence2, primer_len=20)

    non_dimerizing_primers1 = []
    for primer1, primer2 in itertools.combinations(primers1, 2):
        if not check_dimerization(primer1, primer2):
            non_dimerizing_primers1.append(primer1)

    non_dimerizing_primers2 = []
    for primer1, primer2 in itertools.combinations(primers2, 2):
        if not check_dimerization(primer1, primer2):
            non_dimerizing_primers2.append(primer1)

    print_sequence_with_primer(sequence1, non_dimerizing_primers1)
    print_sequence_with_primer(sequence2, non_dimerizing_primers2)

    write_to_fasta("highlighted_sequence1.fasta", sequence1, reference_data)
    write_to_fasta("highlighted_sequence2.fasta", sequence2, reference_data)


if __name__ == "__main__":
    main()
