# coding: utf-8
from __future__ import unicode_literals
from yargy import (rule, fact, not_, and_, or_, attribute,)
from yargy.predicates import (gram, caseless, normalized, is_title, dictionary, custom, eq, )
from yargy.relations import (gnc_relation, case_relation,)

### NATASHA EXTRACTOR DEF
from natasha.extractors import Extractor
class eduorganisationExtractor(Extractor):
    def __init__(self):
        super(eduorganisationExtractor, self).__init__(EDUORGANISATION)  
###

## 1 - FACT INIT
eduorganisation = fact('eduorganisation', ['name', 'tmp', 'tmp2'])
from .dictionary import EDUORGANISATION_DICT, EDUORGANISATION_DICT_REGEXP
###

### 2 - INIT GRAMS & GRAM RULES (pymorphy2)
ADJF = gram('ADJF')
NOUN = gram('NOUN')
INT = gram('INT')
TITLE = is_title()

PRE_WORDS = rule(
  or_(
    or_(
      gram('PREP'),
      gram('Vpre'),
      gram('CONJ'),
      gram('PRCL'),
      gram('INTJ'),
    ),
    gram('POST'),    
  ).optional()
)
    
case = case_relation()
GENT_GROUP = rule(
    gram('gent').match(case)
).repeatable().optional()

#ADJF
ADJF_PREFIX_COUNTABLE = rule(
    or_(caseless('и'), eq(',')).optional(),
).repeatable()


ADJF_PREFIX_ADJF = and_(
    ADJF,
    TITLE
).repeatable()


ADJF_NORM = rule(
            and_(
            ADJF,
            custom(lambda s: EDUORGANISATION_DICT_REGEXP.search(s), types=(str))
            )
).repeatable()


ADJF_PREFIX = rule(
    ADJF_PREFIX_ADJF,
    ADJF.optional(), #Киевском государственном университете
    ADJF_PREFIX_COUNTABLE
).repeatable()
#
###


### 1-ST RING RULES
R1_SIMPLE = rule(
   EDUORGANISATION_DICT,
).repeatable()


R1_ADJF = rule(
   ADJF_NORM,
).repeatable()
###


### 2-ST RING RULES

#Кембриджском университете
#Казанский и Московский университеты
R2_SIMPLE_W_ADJF = rule(
    ADJF_PREFIX,
    R1_SIMPLE,
).repeatable()


R2_QUOTED = or_(rule(
    EDUORGANISATION_DICT,
    gram('QUOTE'),
    not_(
        or_(
            gram('QUOTE'),
            gram('END-OF-LINE'),
        )).repeatable(),
    gram('QUOTE')),
    
    rule(
      gram('QUOTE'),
      ADJF.optional(),      
      EDUORGANISATION_DICT,      
      not_(
          or_(
              gram('QUOTE'),
              gram('END-OF-LINE'),
          )).repeatable(),
      gram('QUOTE'),        
))


R2_KNOWN = rule(
    gram('Orgn'),
    GENT_GROUP,
)
###
    
### INTERPRETATION RULE
INTERPRET_NAME = rule(or_(
  R2_QUOTED,
  R2_SIMPLE_W_ADJF,
  R2_KNOWN,
  R1_SIMPLE,  
  )
).interpretation(eduorganisation.name.normalized())


INTERPRET_TMP = rule(or_(
  R1_ADJF
  )
).interpretation(eduorganisation.tmp.normalized())
###

### SUMMARY RULE
EDUORGANISATION_ = or_(
  INTERPRET_NAME,
  INTERPRET_TMP,  
)
###

### EXPORT RULE
EDUORGANISATION = EDUORGANISATION_.interpretation(eduorganisation)
###
