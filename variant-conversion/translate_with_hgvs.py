import random
import logging

import hgvs.parser
import hgvs.dataproviders.uta
import hgvs.assemblymapper

logging.basicConfig(level=logging.INFO)

hdp = hgvs.dataproviders.uta.connect()
hgvsparser = hgvs.parser.Parser()
am_38 = hgvs.assemblymapper.AssemblyMapper(hdp, assembly_name='GRCh38')
am_37 = hgvs.assemblymapper.AssemblyMapper(hdp, assembly_name='GRCh37')

var_str = 'NC_000007.13:g.117180196C>G'
var_hg37 = hgvsparser.parse_hgvs_variant(var_str)

## Hacky way
transcripts = am_37.relevant_transcripts(var_g=var_hg37)

if len(transcripts) == 0:
    raise Exception('No valid transcripts found')

# choose a random transcript
chosen_transcript = random.choice(transcripts)

var_c = am_37.g_to_c(var_hg37, chosen_transcript)
var_hg38 = am_38.c_to_g(var_c)

logging.info(f"Converted {var_hg37} (HG37) to {var_hg38} (HG38) over {var_c}")