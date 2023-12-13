#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re

literalNames = [ "<INVALID>", "'model'", "'types'", "'group'", "':'", 
                 "'{'", "'}'", "'def'", "','", "'='", "'required'", 
                 "'feature'", "'requires'", "'excludes'", "'sub'", "'alternative'", 
                 "'multiple'", "'('", "')'", "'['", "']'", "'range'", 
                 "'enum'", "'*'", "'/'", "'**'", "'noP'", "'yotta'", 
                 "'zetta'", "'exa'", "'peta'", "'tera'", "'giga'", "'mega'", 
                 "'kilo'", "'hecto'", "'deca'", "'deci'", "'centi'", 
                 "'mili'", "'micro'", "'nano'", "'pico'", "'femto'", 
                 "'atto'", "'zepto'", "'yocto'", "'meter'", "'gram'", 
                 "'ton'", "'second'", "'ampere'", "'kelvin'", "'mole'", 
                 "'candela'", "'pascal'", "'Joul'", "'+'", "'-'", "'%'", 
                 "'.'" ]

symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                  "<INVALID>", "ELONG", "EDOUBLE", "EBoolean", "ID", 
                  "INT", "STRING", "WS", "ML_COMMENT", "SL_COMMENT", 
                  "ANY_OTHER" ]


def get_position_and_item_val(inp : str):
    from itertools import groupby

    ret_val = []

    for k, g in groupby(enumerate(inp), lambda x: not x[1].isspace()):
        if k:
            pos, first_item = next(g)
            item = first_item + ''.join([x for _, x in g])
            ret_val.append([pos, pos + len(item) - 1, item])
    return ret_val

string = "lelelelelelel def oder not def of model"

print(get_position_and_item_val(string))