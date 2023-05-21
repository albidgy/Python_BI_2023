from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests
import time



'''
There are a number of shortcomings here, for example, time.sleep without 
additional check between requests.get and requests.post. 
Unfortunately, I can’t improve the code yet, I was banned by NCBI :(
'''

@dataclass
class Alignment:
    '''
    This data class has some attributes
    subj_name - name of reference sequence
    subj_id - id of reference sequence
    subj_len - length of reference sequence
    subj_range - start, end of attachment of the protein sequence of the reference
    score - score of alignment
    e_value - E-value of alignment
    identity - percent match of two sequences
    query_seq - aligned parse sequence
    subj_seq - sequence on which query_seq aligned
    '''
    
    subj_name: str
    subj_id: str
    subj_len: int
    subj_range: tuple
    score: int
    e_value: float
    identity: int
    query_seq: str
    subj_seq: str


class TBlastn:
    URL = 'https://blast.ncbi.nlm.nih.gov/'
    
    def __init__(self, prot_seq, taxon):
        self._prot_seq = prot_seq
        self._taxon = taxon
        self._alignments_l = []
        
        self.data = {'QUERY': self._prot_seq,
                     'QUERYFILE': None,
                     'EQ_MENU': self._taxon,
                     'CMD': 'request',
                     'PROGRAM': 'tblastn',
                     'BLAST_PROGRAMS': 'tblastn',
                     'ORG_DBS': 'orgDbsOnly_wgs',
                     'EXPECT': '0.05',
                     'WORD_SIZE': '5',  # this is default value, but results diverge without it
                     'HSP_RANGE_MAX': 0,
                     'FILTER': 'L',
                    }
    
    def _parse_xml(self, response_get_xml):
        soup_for_parse_xml = BeautifulSoup(response_get_xml.content, 'xml')
        hit_num = soup_for_parse_xml.find_all('Hit_num')
        for jdx in range(len(hit_num)):
            subj_name = hit_num[jdx].next_sibling.parent.findNext('Hit_def').text.split(', whole')[0]  # work just with wgs
            subj_id = hit_num[jdx].next_sibling.parent.findNext('Hit_accession').text
            subj_len = int(hit_num[jdx].next_sibling.parent.findNext('Hit_len').text)
            n_matches_by_1sp = hit_num[jdx].next_sibling.parent.find_all('Hsp_num')
            for idx in range(len(n_matches_by_1sp)):
                number_of_match = n_matches_by_1sp[idx].parent
                subj_range = (int(number_of_match.findNext('Hsp_hit-from').text), 
                              int(number_of_match.findNext('Hsp_hit-to').text))
                score = round(float(number_of_match.findNext('Hsp_bit-score').text))
                e_value = float(number_of_match.findNext('Hsp_evalue').text)
                identity = int(int(number_of_match.findNext('Hsp_identity').text) / 
                               int(number_of_match.findNext('Hsp_align-len').text) * 100)

                query_seq = number_of_match.findNext('Hsp_qseq').text
                subj_seq = number_of_match.findNext('Hsp_hseq').text

                alignment = Alignment(subj_name=subj_name, 
                                      subj_id=subj_id, 
                                      subj_len=subj_len, 
                                      subj_range=subj_range, 
                                      score=score, 
                                      e_value=e_value,
                                      identity=identity,
                                      query_seq=query_seq,
                                      subj_seq=subj_seq,
                                     )
                self._alignments_l.append(alignment)
    
    def _get_xml_file(self, response_get_res):
        soup_get_res = BeautifulSoup(response_get_res.content, 'lxml')
        xml_link = soup_get_res.find_all('a', class_='xgl', string='XML')[0].attrs['href']
        response_get_xml = requests.get(self.URL + xml_link)
        return response_get_xml
    
    def run_tblastn_analysis(self, sleep_multiplier=2.0):
        response_send_seq = requests.post(f'{self.URL}Blast.cgi', data=self.data)
        soup = BeautifulSoup(response_send_seq.content, 'lxml')
        rsid = soup.find_all('td', string='Request ID')[0].next_sibling.text.strip(' ')
        rtoe = int(soup.find_all('input', attrs={'name': 'RTOE'})[0].attrs['value'])  # NCBI calculate estimated working time
        
        time.sleep(round(rtoe * sleep_multiplier))
        response_get_res = requests.get(f'{self.URL}Blast.cgi', params={'CMD': 'Get', 'RID': rsid})
        response_get_xml = self._get_xml_file(response_get_res)
        self._parse_xml(response_get_xml)
        
        return self._alignments_l
