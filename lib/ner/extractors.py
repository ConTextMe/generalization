# -*- coding: utf-8 -*-
########    #######    ########    #######    ########    ########
##     / / / /    License    \ \ \ \ 
##    Copyleft culture, Copyright (C) is prohibited here
##    This work is licensed under a CC BY-SA 4.0
##    Creative Commons Attribution-ShareAlike 4.0 License
##    Refer to the http://creativecommons.org/licenses/by-sa/4.0/
########    #######    ########    #######    ########    ########
##    / / / /    Code Climate    \ \ \ \ 
##    Language = python3
##    Indent = space;    2 chars;
########    #######    ########    #######    ########    ########


#@profile
def init(args, session):
  import importlib
  extractor = {}
  
  for ex in session['cognitions']:
    extractor[ex] = {}
    facts = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    grammar = importlib.import_module('cognitions.' + ex.lower() + '.grammar')  
    extractor[ex]['ExtractorHandler'] = eval('grammar.' + ex + 'Extractor')()
  return extractor
