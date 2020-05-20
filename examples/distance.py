"""
Calculate distances in order to create a Neighbor-Net from the data.
"""

from lingpy import *
from lexibank_pharaocoracholaztecan import Dataset
from lingpy.convert.strings import write_nexus
from tabulate import tabulate
from itertools import combinations

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

taxa = [t for t in wl.cols if not t.startswith('Proto')] + ['ProtoNahua']
table = []
for t1, t2 in combinations(taxa, r=2):
    cog1 = wl.get_list(col=t1, entry='cogid', flat=True)
    cog2 = wl.get_list(col=t2, entry='cogid', flat=True)
    table += [[t1, t2, len([c for c in cog1 if c in cog2])]]
print(tabulate(table, tablefmt='pipe'))

#alms = Alignments(wl, transcription='form', ref='cogid')
#alms.align()
#
#alms.output('tsv', filename='wordlist', ignore='all', prettify=False)
