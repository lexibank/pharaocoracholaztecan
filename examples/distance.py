"""
Calculate distances in order to create a Neighbor-Net from the data.
"""

from lingpy import *
from lexibank_pharaocoracholaztecan import Dataset
from lingpy.convert.strings import write_nexus
from tabulate import tabulate
from itertools import combinations

wl_ = Wordlist.from_cldf(
        Dataset().cldf_dir.joinpath('cldf-metadata.json'), 
        columns=['language_id', 'concept_name', 'value', 'form',
            'segments',
            'cogid_cognateset_id'],
        namespace=(
            ('language_id', 'doculect'),
            ('concept_name', 'concept'),
            ('segments', 'tokens'),
            ('cogid_cognateset_id', 'cogid'),
            ))

taxa = [t for t in wl_.cols if not t.startswith('Proto')] + ['ProtoNahua']
D = {0: wl_.columns}
for idx in wl_:
    if wl_[idx, 'doculect'] in taxa:
        D[idx] = wl_[idx]
wl = Wordlist(D)
table = []
for t1, t2 in combinations(taxa, r=2):
    cog1 = wl.get_list(col=t1, entry='cogid', flat=True)
    cog2 = wl.get_list(col=t2, entry='cogid', flat=True)
    table += [[t1, t2, len([c for c in cog1 if c in cog2])]]
print(tabulate(table, tablefmt='pipe'))

wl.calculate('distances', ref='cogid')
wl.output('dst', filename='distances')
wl.calculate('tre', tree_calc='neighbor')
wl.output('tre', filename='tree')
wl.output('tsv', filename='wordlist', ignore='all', prettify=False)

write_nexus(wl, mode='splitstree', filename='coracholaztecan.nex')


alms = Alignments(wl_, transcription='form', ref='cogid')
alms.align()

alms.output('tsv', filename='wordlist', ignore='all', prettify=False)
