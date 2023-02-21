from abc import ABC, abstractmethod


class BiologicalSequence(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def do_slice(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def check_alphabet(self):
        pass


class AcidSequence(BiologicalSequence):
    def __init__(self, sequence):
        self._sequence = sequence
        self._DICT_COMPLEMENT = None

    def __len__(self):
        return len(self._sequence)

    def do_slice(self, bounds):
        if isinstance(bounds, int):
            return self._sequence[bounds]
        elif isinstance(bounds, tuple):
            start, stop = bounds
            return self._sequence[start:stop]

    def __str__(self):
        return str(self._sequence)

    def check_alphabet(self):
        for nucl in self._sequence:
            if nucl.upper() not in self._DICT_COMPLEMENT:
                return False
        return True


class NucleicAcidSequence(AcidSequence):
    def __init__(self, sequence):
        super().__init__(sequence)

    def complement(self):
        complement_seq = []
        for nucl in self._sequence:
            complement_seq.append(self._DICT_COMPLEMENT[nucl])
        return ''.join(complement_seq[::-1])

    def gc_content(self):
        gc_compound = 0
        total_len = len(self._sequence)
        for nucl in self._sequence:
            if nucl.upper() == 'G' or nucl.upper() == 'C':
                gc_compound += 1
        return gc_compound / total_len * 100


class AminoAcidSequence(AcidSequence):
    def __init__(self, sequence):
        super().__init__(sequence)
        self._DICT_COMPLEMENT = {'A': 'Ala',
                                 'R': 'Arg',
                                 'N': 'Asn',
                                 'D': 'Asd',
                                 'C': 'Cys',
                                 'Q': 'Gln',
                                 'E': 'Glu',
                                 'G': 'Gly',
                                 'H': 'His',
                                 'I': 'Iso',
                                 'L': 'Leu',
                                 'K': 'Lys',
                                 'M': 'Met',
                                 'F': 'Phe',
                                 'P': 'Pro',
                                 'S': 'Serine',
                                 'T': 'Thr',
                                 'W': 'Trp',
                                 'Y': 'Tyr',
                                 'V': 'Val',
                                 'X': 'Glx',
                                 'Z': 'Gli',
                                 'J': 'Nle',
                                 'U': 'Cyc'}

    def translate(self):
        # converting a one-letter amino acid sequence to a three-letters sequence
        three_letter_translated = []
        for nucl in self._sequence:
            three_letter_translated.append(self._DICT_COMPLEMENT[nucl])
        return '-'.join(three_letter_translated)


class DNASequence(NucleicAcidSequence):
    def __init__(self, sequence):
        super().__init__(sequence)
        self._DICT_COMPLEMENT = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}


class RNASequence(NucleicAcidSequence):
    def __init__(self, sequence):
        super().__init__(sequence)
        self._DICT_COMPLEMENT = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}
        self._TRANSCRIBE_RNA_TO_DNA = {'A': 'T', 'U': 'A', 'C': 'G', 'G': 'C'}

    def transcribe(self):
        transcriped_seq = []
        for nucl in self._sequence:
            transcriped_seq.append(self._TRANSCRIBE_RNA_TO_DNA[nucl])
        return ''.join(transcriped_seq)
