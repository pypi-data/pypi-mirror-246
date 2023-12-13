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

import jinja2 as j
import os

from conflspserver.symboltable.symbol_table import SymbolTable

__author__ = 'stu222808'

#Relative imports
from ..symboltable.symbol_table import SymbolTable, GroupSymbol, VariableSymbol, FeatureSymbol, EnumSymbol

class StandartCodeGenerator():
    """
    a simple code generator representing a simple structrue and helpful functions
    """
    def __init__(self, symbolTable : SymbolTable, outputPath : str, templatePath = "") -> None:
        self._symbolTable : SymbolTable = symbolTable
        self.outputPath = outputPath
        if not templatePath == "":
            self.templateLoader = j.PackageLoader(str(self.__module__), templatePath)
            self.templateEnv = j.Environment(loader=self.templateLoader)
        
    def writeFile(self, content : str, filename : str):
        """method to write content to a file inside the output folder

        Args:
            content (str): string to write into the file
            filename (str): filename specified
        """
        path = os.path.join(self.outputPath, filename)
        f = open(path, "w")
        f.write(content)
        f.close()
    
    def generate(self) -> None:
        """generate method that uses jinja templates to write files into output path
        """
        print("GIVE THE GENERATOR A TEMPLATE AND DATA TO WORK WITH")

class UvicCodeGenerator(StandartCodeGenerator):
    """code generator for uvic

    Args:
        StandartCodeGenerator (_type_): _description_
    """
    def __init__(self, symbolTable : SymbolTable, outputPath : str) -> None:
        super().__init__(symbolTable, outputPath)
        self.templateLoader = j.PackageLoader(str(self.__module__), "jinja-templates/uvic")
        self.templateEnv = j.Environment(loader=self.templateLoader)

    def generate(self) -> None:
        """generates uvic files
        """
        #control in template
        templatecontr = self.templateEnv.get_template("control.in.template")
        controlPath = os.path.join(self.outputPath, "control.in")
        control = open(controlPath, "w")
        control.write(templatecontr.render(symbols = self._symbolTable.children(), groupSymbol=GroupSymbol, paramSymbol=VariableSymbol, featureSymbol = FeatureSymbol, isinstance=isinstance, enumSymbol = EnumSymbol, enumerate = enumerate, bool = bool))
        control.close()
        #mk in template
        templatemk = self.templateEnv.get_template("mk.in.template")
        #get source and general group
        generalObj = {}
        sourceObj = {}
        for elem in self._symbolTable.children():
            if elem.name == "general":
                for i in elem.children():
                    if i.is_array:
                        generalObj[i.name] = i.toNormalizedArray()
                    else:
                        # could be an enum so we need the string here
                        generalObj[i.name] = i.value[0] if isinstance(i.value, tuple) else i.value
            if elem.name == "source":
                for i in elem.children():
                    if i.is_array:
                        sourceObj[i.name] = i.toNormalizedArray()
                    else:
                        generalObj[i.name] = i.value[0] if isinstance(i.value, tuple) else i.value
        mkPath = os.path.join(self.outputPath, "mk.in")
        mk = open(mkPath, "w")
        mk.write(templatemk.render(general = generalObj, source = sourceObj, features = self._symbolTable.getNestedSymbolsOfTypeSync(FeatureSymbol), isinstance = isinstance, tuple = tuple))
        mk.close()
    
class mitGcmCodeGenerator(StandartCodeGenerator):
    """a generator for mitgcm

    Args:
        StandartCodeGenerator (_type_): _description_
    """
    def __init__(self, symbolTable: SymbolTable, outputPath: str) -> None:
        super().__init__(symbolTable, outputPath)
        self.templateLoader = j.PackageLoader(str(self.__module__), "jinja-templates/mitgcm")
        self.templateEnv = j.Environment(loader=self.templateLoader)

    def isConfigurated(self, elem : FeatureSymbol) -> bool:
        """function to lookup if any parameter in elem was configurated

        Args:
            elem (FeatureSymbol): _description_

        Returns:
            bool: if one parameter was configurated
        """
        groupSymbol = elem.getNestedSymbolsOfTypeSync(GroupSymbol)
        for param in groupSymbol:
            if len(param.configuration) > 0:
                return True
        return False
    
    def firstNotNoneElem(self, elem, type) -> int:
        """function for jinja template to avoid ',' behind last element

        Args:
            elem (_type_): the element to search inside for
            type (_type_): the type to search for

        Returns:
            int: returns the index of last element
        """
        index = 0
        for param in elem.getNestedSymbolsOfTypeSync(type):
            if param.value == None:
                index+=1
            else:
                return index

    def generate(self) -> None:
        """generates files for mitgcm
        """
        #need groups, feature list
        groupList = {}
        featureList = {}
        activatedList = []
        layer_size = False
        alreadyDone = {"EEPARMS" : [False, "eedata"], "MNC" : [False, "data.mnc"], "GMRedi" : [False, "data.gmredi"], "RBCS" : [False, "data.rbcs"], "Layers" : [False, "data.layers"], "PTRACERS" : [False, "data.ptracers"], "Shap" : [False, "data.shap"], "obcs" : [False, "data.obcs"], "GCHEM" : [False, "data.gchem"], "offline" : [False, "data.offline"]}
        featureTemplate = self.templateEnv.get_template("data.feature.template")

        def checkFeature(elem):
            """a function to check if the givben feature is activated -> write the mitgcm file

            Args:
                elem (GroupSymbol, FeatureSymbol): a feature from mitgcm
            """
            try:
                if elem.is_activated:
                    if elem.name == "diagnostics":
                        activatedList.append("Diagnostics")
                    else:
                        activatedList.append(elem.name)
                dataList = alreadyDone[elem.name]
                if dataList[0]:
                    return
                if elem.name == "EEPARMS":
                    eeparmsTemplate = self.templateEnv.get_template("eedata.template")
                    self.writeFile(eeparmsTemplate.render(group = elem, isinstance = isinstance, variableSymbol = VariableSymbol, float = float, int = int, bool = bool, groupSymbol = GroupSymbol, none = None, str = str, enumerate = enumerate, firstNotNoneElem = self.firstNotNoneElem), "eedata")
                    return
                if not elem.is_activated:
                    return
                fileName = dataList[1]
                alreadyDone[elem.name] = [True, fileName]
                self.writeFile(featureTemplate.render(feature = elem, isinstance = isinstance, variableSymbol = VariableSymbol, float = float, int = int, bool = bool, groupSymbol = GroupSymbol, none = None, str = str, enumerate = enumerate, firstNotNoneElem = self.firstNotNoneElem), fileName)
            except:
                pass

        for elem in self._symbolTable.getAllNestedSymbolsSync():
            if isinstance(elem, GroupSymbol):
                groupList[elem.name] = elem
            if isinstance(elem, FeatureSymbol):
                featureList[elem.name] = elem
            #check and use template for group(EEPARMS), feature(MNC, GMRedi, RBCS, Layers, PTRACERS, Shap, obcs, GCHEM, offline)
            checkFeature(elem)
            if elem.name == "layers_size":
                layer_size = True

        #give group for eedata, feature for data.mnc, data.gmredi, data.rbcs, data.layers, data.ptracers, data.shap, data.obcs, data.gchem, data.off all same template
        #for every feature give to data.pkg + check for feature diagnostic
        dataPkgTemplate = self.templateEnv.get_template("data.pkg.template")
        self.writeFile(dataPkgTemplate.render(actData = activatedList, enumerate = enumerate), "data.pkg")
        
        #layer_size template only if group layer_size exists (LAYERS_SIZE.h)
        if layer_size:
            #TODO: still buggy
            layerSizeTemplate = self.templateEnv.get_template("layer_size.template")
            self.writeFile(layerSizeTemplate.render(groups = groupList, variableSymbol = VariableSymbol, groupSymbol = GroupSymbol, none = None, str = str, enumerate = enumerate, firstNotNoneElem = self.firstNotNoneElem), "LAYERS_SIZE.h")
        
        #packages.conf check for feature diagnostics
        packagesTemplate = self.templateEnv.get_template("packages.conf.template")
        try:
            activatedList.remove("EEPARMS")
        except:
            pass
        self.writeFile(packagesTemplate.render(features = activatedList), "packages.conf")

        dataTemplate = self.templateEnv.get_template("data.template")
        self.writeFile(dataTemplate.render(groups = groupList, isinstance = isinstance, variableSymbol = VariableSymbol, float = float, int = int, bool = bool, groupSymbol = GroupSymbol, none = None, str = str, enumerate = enumerate, firstNotNoneElem = self.firstNotNoneElem), "data")

        sizeTemplate = self.templateEnv.get_template("size.template")
        self.writeFile(sizeTemplate.render(groups = groupList, variableSymbol = VariableSymbol, groupSymbol = GroupSymbol, none = None, str = str, enumerate = enumerate, firstNotNoneElem = self.firstNotNoneElem), "SIZE.h")

        for elem in self._symbolTable.getAllNestedSymbolsSync("tRef"):
            print(elem.name, elem.value, type(elem))