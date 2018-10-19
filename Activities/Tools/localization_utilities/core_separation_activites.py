from resx_utils import ResourceFileUtil
import os
from pathlib import Path
from os import walk
import re

def get_res_object(program):
    for line in program:
        if ("=", "using", "UiPath.Core.Activities.Design.Properties.Resources" in line):
            m = re.search("using\s+(\w+)\s+", line)
            if (m):
                return m.group(1)
    return None

def get_resources_from_file(program_path): 
    with open(program_path, mode='r') as f:
        program = f.readlines()
    res = set()
    res_object = get_res_object(program)
    for line in program:
        if ("Resources." in line):
            for m in re.finditer("Resources\.(\w+)", line):
                if (m):
                    key = m.group(1)
                    res.add(key.lower())
        if (res_object is not None and "{0}.".format(res_object) in line):
            for m in re.finditer("{0}\.(\w+)".format(res_object), line):
                if (m):
                    key = m.group(1)
                    res.add(key.lower())
    return res

def get_keys_from_folder(dir_path):
    keys = set()
    for (dirpath, dirnames, filenames) in walk(dir_path):
        if (os.path.dirname(dirpath) == "Properties"):
            continue
        for filename in filenames:
            print(os.path.join(dirpath, filename))
            (name, ext) = os.path.splitext(filename)
            if (ext == ".cs"):
                res = get_resources_from_file(os.path.join(dirpath, filename))
                keys = keys.union(res)
            elif (ext == ".xaml"):
                res = get_resources_from_file(os.path.join(dirpath, filename))
                keys = keys.union(res)
    return keys
        
current_dir = Path.cwd()
root_path = current_dir.parent.parent.parent
shared_path = root_path.joinpath("UiPath.Activities.Shared")

def split_activities_resx(project_path, shared_path, resx_path, new_resx_path):
    resx_util = ResourceFileUtil(resx_path, new_resx_path)
    keys = get_keys_from_folder(project_path)
    keys = keys.union(get_keys_from_folder(shared_path))
    resx_util.remove_resources(keys)
    resx_util.save()

ui_automation_path = root_path.joinpath("UiPath.UiAutomation.Activities")
ui_core_resx = ui_automation_path.joinpath("Properties").joinpath("UiPath.Core.Activities.resx")

ui_automation_resx = ui_automation_path.joinpath("Properties").joinpath("UiPath.UiAutomation.Activities.resx")
split_activities_resx(ui_automation_path, shared_path, ui_core_resx, ui_automation_resx)


ui_base_path = root_path.joinpath("UiPath.Base.Activities")
ui_base_resx = ui_base_path.joinpath("Properties").joinpath("UiPath.Base.Activities.resx")
split_activities_resx(ui_base_path, shared_path, ui_core_resx, ui_base_resx)


ui_automation_design_path = root_path.joinpath("UiPath.UiAutomation.Activities.Design")
ui_core_design_resx = ui_automation_design_path.joinpath("Properties").joinpath("UiPath.Core.Activities.Design.resx")
shared_designer_path = root_path.joinpath("UiPath.Activities.Design.Shared")
ui_automation_design_resx = ui_automation_design_path.joinpath("Properties").joinpath("UiPath.UiAutomation.Activities.Design.resx")
split_activities_resx(ui_automation_design_path, shared_designer_path, ui_core_design_resx, ui_automation_design_resx)

ui_base_desing_path = root_path.joinpath("UiPath.Base.Activities.Design")
ui_base_design_resx = ui_base_desing_path.joinpath("Properties").joinpath("UiPath.Base.Activities.Design.resx")
split_activities_resx(ui_base_desing_path, shared_path, ui_core_design_resx, ui_base_design_resx)
