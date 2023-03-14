from dataclasses import dataclass
import os
import re


@dataclass
class FastaRecord:
    seq: str
    id_: str
    description: str


class OpenFasta:
    def __init__(self, file_name):
        self._fasta_record = FastaRecord(seq='', id_='', description='')
        self.file_obj = open(file_name)
        self.__seq_l = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.file_obj.close()

    def __iter__(self):
        yield self.file_obj

    def read_record(self):
        counter_name_seq = 0
        self.__seq_l.clear()
        while counter_name_seq <= 2:
            line = next(self.file_obj)
            line = line.strip('\n')
            if line.startswith('#'):
                continue
            
            elif line.startswith('>'):
                if self._fasta_record.id_ == '':  # need for first line: >gene spesies
                    self._fasta_record.id_, self._fasta_record.description = re.findall(r'(.+?) (.+)', line)[0]
                else:
                    self._fasta_record.seq = ''.join(self.__seq_l)
                    # make object with current values
                    current_fasta_record = self._fasta_record
                    # clear current info
                    self._fasta_record = FastaRecord(seq='', id_='', description='')
                    # remember for next iteration
                    self._fasta_record.id_, self._fasta_record.description = re.findall(r'(.+?) (.+)', line)[0]
                    return current_fasta_record
                
            else:
                self.__seq_l.append(line)

    def read_records(self):
        result_all_fasta = []
        while True:
            try:
                result_all_fasta.append(self.read_record())
            except StopIteration:
                # write last sequences
                self._fasta_record.seq = ''.join(self.__seq_l)
                result_all_fasta.append(self._fasta_record)
                return result_all_fasta
