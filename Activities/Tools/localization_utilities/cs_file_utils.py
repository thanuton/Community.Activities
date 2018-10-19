'''
 Localizes windows workflow properties activities, using multiple heuristics.
 For example a property that needs to be localized is found if
 the property is public, has getter and setters in line with its signature.
 N.B.: USE WITH CAUTION
'''
import re

class CSFileLocalization:
    resource_util = None
    
    def __init__(self, path):
        self.program_path = path
        with open(path, mode='r') as f:
            self.program = f.readlines()
    
    def is_activity(self):
        has_activities_namespace = False
        for line in self.program:
            if ("System.Activities" in line):
                has_activities_namespace = True
                break
        is_class_extended = False
        for line in self.program:
            if ("class" in line and ":" in line):
                is_class_extended = True
                break
        return has_activities_namespace and is_class_extended
        
    def localize(self):
        if (not self.is_activity()):
            return
        result = []
        for i in range(0, len(self.program)):
            if (self.line_contains_property(self.program[i])):
                attributes = self.get_attributes(i)
                if (not self.is_property_browsable(attributes)):
                    result.append(self.program[i])
                    continue
                m = re.search(".*\s+(.*)\s+{.*", self.program[i])
                if (m):
                    #The property name was found
                    display_prop = m.group(1)
                    spaces = self.program[i][:(len(self.program[i]) - len(self.program[i].lstrip()))]
                    attributes = self.localize_attribute("Category", attributes, spaces)
                    attributes = self.localize_attribute("DisplayName", attributes, spaces)
                    
                    for j in range(0, len(attributes)):
                        #remove old attribute lines
                        result.pop()
                    
                    if (not self.is_attribute_localized("DisplayName", attributes)):
                        attributes.append(spaces + "[LocalizedDisplayName(nameof(Resources.{0}))]\n".format(display_prop))
                        CSFileLocalization.resource_util.add_resource(display_prop, display_prop)
                
                result.extend(attributes)
            result.append(self.program[i])
        isProgramUpdated = len(result) > len(self.program)
        self.program = result
        if (isProgramUpdated):
            self.add_properties_namespace()
    
    def save(self):
        with open(self.program_path, "w") as f:
            f.writelines(self.program)
    
    @staticmethod
    def localize_attribute(attribute_type, attributes, spaces):
        res = []
        if (not CSFileLocalization.is_attribute_localized(attribute_type, attributes)):
            for attr in attributes:
                if (attribute_type in attr):
                    val = CSFileLocalization.get_attribute_value(attr)
                    key = re.sub('\s+', '', val)
                    res.append(spaces + "[Localized{0}(nameof(Resources.{1}))]\n".format(attribute_type, key))
                    CSFileLocalization.resource_util.add_resource(key, val)
                else:
                    res.append(attr)
        else:
            res = attributes
        return res
    
    @staticmethod
    def get_attribute_value(attribute):
        m = re.search(".*\"(.*)\".*", attribute)
        if (m):
            return m.group(1)
        return None
    
    @staticmethod
    def line_contains_property(line):
        return "public" in line and "{" in line and "}" in line and "get" in line and "set" in line
    
    @staticmethod
    def is_property_browsable(lines):
        for line in lines:
            if ("Browsable" in line):
                m = re.search(".*\((.*)\).*", line)
                if (m):
                    return m.group(1).strip() != 'false'
        return True
    
    @staticmethod
    def is_attribute_localized(attribute_type, attributes):
        for attr in attributes:
            if ("Localized{0}".format(attribute_type) in attr):
                return True
        return False
        
    def get_attributes(self, index):
        res = []
        sw = True
        i = index - 1
        while (sw and i >= 0):
            if ("[" in self.program[i] and "]" in self.program[i] or self.program[i].isspace()):
                res.append(self.program[i])
            else:
                sw = False
            i = i - 1
        res.reverse()
        return res
    
    def add_properties_namespace(self):
        namespaces = self.get_namespaces()
        hasPropertiesNamespace = False
        for namespace in namespaces:
            if ("using UiPath.Core.Activities.Properties;" in namespace):
                hasPropertiesNamespace = True
                break
        after_namespaces_index = len(namespaces)
        
        if (not hasPropertiesNamespace):
            namespaces.append("using UiPath.Core.Activities.Properties;\n")
        
        res = []
        
        for namespace in namespaces:
            res.append(namespace)
        
        for i in range(after_namespaces_index, len(self.program)):
            res.append(self.program[i])
        self.program = res
  
    def get_namespaces(self):
        sw = True
        i = 0
        res = []
        while(sw and i < len(self.program)):
            if ("using" in self.program[i] and ";" in self.program[i] or self.program[i].isspace()):
                res.append(self.program[i])
            else:
                sw = False
            i = i + 1
        
        while(len(res) > 0 and res[-1].isspace()):
            res.pop()
        return res