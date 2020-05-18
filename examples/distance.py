"""
Calculate distances in order to create a Neighbor-Net from the data.
"""

from lingpy import *
from lexibank_pharaocoracholaztecan import Dataset
from lingpy.convert.strings import write_nexus


wl = Wordlist.from_cldf(
        Dataset().cldf_dir.joinpath('cldf-metadata.json'), 
        columns=['language_id', 'concept_name', 'value', 'form',
            'cogid_cognateset_id'],
        namespace=(
            ('language_id', 'doculect'),
            ('concept_name', 'concept'),
            ('cogid_cognateset_id', 'cogid'),
            ))
wl.calculate('distances', ref='cogid')
wl.output('dst', filename='distances')
wl.calculate('tre', tree_calc='neighbor')
wl.output('tre', filename='tree.nwk')
wl.add_entries('tokens', 'form', ipa2tokens)
wl.output('tsv', filename='wordlist', ignore='all', prettify=False)

write_nexus(wl, mode='splitstree', filename='coracholaztecan.nex')

#alms = Alignments(wl, transcription='form', ref='cogid')
#alms.align()
#
#alms.output('tsv', filename='wordlist', ignore='all', prettify=False)
