import attr
from pathlib import Path

from pylexibank import Concept, Language,FormSpec
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar

import lingpy
from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Spanish = attr.ib(default=None)
    Number = attr.ib(default=None)
#
#
#@attr.s
#class CustomLanguage(Language):
#    Latitude = attr.ib(default=None)
#    Longitude = attr.ib(default=None)
#    ChineseName = attr.ib(default=None)
#    SubGroup = attr.ib(default="Bai")
#    Family = attr.ib(default="Sino-Tibetan")
#    DialectGroup = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "pharaocoracholaztecan"
    concept_class = CustomConcept
    #language_class = CustomLanguage
    form_spec = FormSpec(
            separators="/",
            first_form_only=True,
            replacements=[("*", "")]
            )

    def cmd_makecldf(self, args):

        # parse the data from the word document
        table = [['']] # we except 9 columns
        with open(self.raw_dir.joinpath('data.txt').as_posix()) as f:
            previous = []
            for i, line in enumerate(f):
                rows = [c.strip() for c in line.split('\t')]
                if rows[0].replace('.', '').isdigit():
                    table += [rows]
                else:
                    table[-1][-1] += '/'+rows[0]
                    table[-1] += rows[1:]
        # load cognates
        cognates = self.raw_dir.read_csv('cognates.tsv', delimiter='\t')[1:]
        concepts = {}
        for concept in self.concepts:
            idx = '{0}-{1}'.format(
                        concept['NUMBER'],
                        slug(concept['SPANISH']))
            args.writer.add_concept(
                    ID=idx,
                    Name=concept['SPANISH'],
                    Concepticon_ID=concept['CONCEPTICON_ID'],
                    Concepticon_Gloss=concept['CONCEPTICON_GLOSS'])
            concepts[concept['SPANISH']] = idx
            concepts[concept['SPANISH'].lower()] = idx
        concepts['Frio/(hace frio)'] = concepts['Frio (hace frio)']
        args.log.info('added concepts')

        args.writer.add_sources()
        cognacy, counter = {}, 1
        cogsets = {
          "A(B)": ["A"],
          "A/(B)": ["A"],
          "A/B": ["A", "B"],
          "A/B/C": ["A", "B", "C"],
          "A/B/D": ["A", "B", "D"],
          "A/B?": ["A"],
          "A/C": ["A", "C"],
          "B/(A)": ["A"],
          "B/(a)": ["B"],
          "B/C": ["B", "C"],                    
          "C D": ["C", "D"],
          "C/(B)": ["C"],
          "C/B": ["C", "B"],
          "C/E": ["C", "E"],
          "D/B": ["D", "B"],
          "a/(B)": ["A"],
          "a/A": ["A", "A"],
          "a/B": ["A", "B"],
          "ab": ["A", "B"],
        }        
        languages = args.writer.add_languages(lookup_factory='Name')
        for i, line in progressbar(enumerate(table[1:])):
            for j, (language, cell) in enumerate(zip(table[0][2:], line[2:])):
                if cell.strip():
                    cognatesets = cogsets.get(
                            cognates[i][j+1].strip(),
                            [cognates[i][j+1].strip()])
                    for cognate in cognatesets:
                        if cognate in ['?', '-']:
                            cid = counter
                            counter += 1
                        else:
                            cid = '{0}-{1}'.format(i, cognate)
                            if cid in cognacy:
                                cid = cognacy[cid]
                            else:
                                cognacy[cid] = counter
                                cid = cognacy[cid]
                                counter += 1
                        for lexeme in args.writer.add_forms_from_value(
                                Value=cell.strip(),
                                Language_ID=languages[language],
                                Parameter_ID=concepts[line[1]],
                                Source=['Pharao2020']
                                ):
                            args.writer.add_cognate(
                                    lexeme,
                                    Cognateset_ID=cid,
                                    Source=['Pharao2020'])




