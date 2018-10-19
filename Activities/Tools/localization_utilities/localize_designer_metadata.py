import os
from pathlib import Path
from resx_utils import ResourceFileUtil
from abc import ABC, abstractmethod
import re

current_dir = Path.cwd()
designer_path = current_dir.parent.parent.parent.parent.parent.joinpath("UiPath.Core.Activities.Design")
metedata_path = designer_path.joinpath("DesignerMetadata.cs")
documnetation_path = designer_path.joinpath("Documentation.cs")
resx_path = designer_path.joinpath("Properties").joinpath("UiPath.Core.Activities.Design.resx")
rf_util = ResourceFileUtil(resx_path)

class MetadataClassFileLocalization:

    def __init__(self, path):
        self.program_path = path
        with open(path, 'r') as f:
            self.program = f.readlines()
    
    def localize(self, attribute_localization_strategy):
        result = []
        for line in self.program:
            result.append(attribute_localization_strategy.localize(line))
        self.program = result
    
    def save(self):
        with open(self.program_path, "w") as f:
            f.writelines(self.program)
    

class IAttributeStrategy(ABC):

    resource_util = None
    
    @abstractmethod
    def localize(self, line):
        raise NotImplementedError
    
    @staticmethod
    def replace_attribute(line, key, attribute):
        return re.sub("{0}\(.?\".+\"\)".format(attribute),("{0}(Resources.".format(attribute)) + key + ")" , line)


class DisplayNameStrategy(IAttributeStrategy):

    def localize(self, line):
        if ("DisplayNameAttribute" in line and "Resources." not in line):
            m = None
            if (line.count(',') == 1):
                # Activity Display Name
                m = re.search(".*typeof\((.+)\).*,.*DisplayNameAttribute\(.?\"(.+)\"\).*", line)
            elif (line.count(',') == 2):
                # Property Display Name
                m = re.search(".*\"(.+)\".*,.*DisplayNameAttribute\(.?\"(.+)\"\).*", line)
            if (m):
                display_key = m.group(2) + "DispalyName"
                display_value = m.group(2)
                IAttributeStrategy.resource_util.add_resource(display_key, display_value)
                line = self.replace_attribute(line, display_key, "DisplayNameAttribute")
        
        return line

class CategoryAttributeStrategy(IAttributeStrategy):
    
    def localize(self, line):
        if ("CategoryAttribute" in line and "Resources." not in line):
            if (line.count(',') >= 1):
                # Category Display Name
                m = None
                m = re.search(".*CategoryAttribute.*\"(.*)\".*", line)
                if (m):
                    key = m.group(1)
                    key = key.replace('<', '')
                    key = key.replace('>', '')
                    key = key.replace('.', '')
                    key = re.sub('\s+', '', key)
                    category_key = key + "CategoryName"
                    category_value = m.group(1)
                    IAttributeStrategy.resource_util.add_resource(category_key, category_value)
                    line = self.replace_attribute(line, category_key, "CategoryAttribute")
        
        return line

class DescriptionAttributeStrategy(IAttributeStrategy):

    def localize(self, line):
        if ("DescriptionAttribute" in line and "Resources." not in line):
            if (line.count(',') >= 1):
                #Number of commas before DescriptionAttribute
                m_commas = re.search("(.*)DescriptionAttribute.*", line)
                if(m_commas):
                    commas = m_commas.group(1).count(',')
                    activity = ""
                    description = ""
                    argument = ""
                    if(commas == 1):
                        # ActivityDescritpion
                        m = re.search(".*\.([^\.]*)\).*DescriptionAttribute.*\"(.*)\".*", line)
                        if (m):
                            activity = m.group(1)
                            description = m.group(2)
                    elif (commas == 2):
                        # Activity argument despription
                        m = re.search(".*(\.|\()([^\.]*)\).*\"(.*)\".*DescriptionAttribute.*\"(.*)\".*", line)
                        if (m):
                            activity = m.group(2)
                            argument = m.group(3)
                            description = m.group(4)
                    activity = re.sub("(<|>)", "", activity)
                    description_key = activity + argument + "Description"
                    description_value = description
                    IAttributeStrategy.resource_util.add_resource(description_key, description_value)
                    line = self.replace_attribute(line, description_key, "DescriptionAttribute")

        return line

class ArgumentNameOfStrategy(IAttributeStrategy):
    def localize(self, line):
        if ("nameof" not in line):
            if (line.count(',') >= 1):
                    #The line is Activity Argument Description
                    m = re.search(".*(\.|\()([^\.]*)\).*,.*\"(.*)\",.*", line)
                    if (m):
                        activity = m.group(2)
                        argument = m.group(3)
                        activity = activity.replace("<>", "<object>")
                        nameof = "nameof({0}.{1})".format(activity, argument)
                        line = re.sub("\"{0}\"".format(argument), nameof, line)
        return line


IAttributeStrategy.resource_util = rf_util

designer_metadata = MetadataClassFileLocalization(metedata_path)

designer_metadata.localize(DisplayNameStrategy())
designer_metadata.localize(CategoryAttributeStrategy())
designer_metadata.localize(ArgumentNameOfStrategy())
designer_metadata.save()

documentation = MetadataClassFileLocalization(documnetation_path)
documentation.localize(DescriptionAttributeStrategy())
documentation.localize(ArgumentNameOfStrategy())
documentation.save()

rf_util.update_resource()