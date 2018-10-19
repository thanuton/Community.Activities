from resx_utils import ResourceFileUtil
from cs_file_utils import CSFileLocalization
import os
from pathlib import Path
from os import walk

current_dir = Path.cwd()
resx_path = current_dir.parent.parent.joinpath("Properties").joinpath("UiPath.Core.Activities.resx")
sources_path = current_dir.parent
rf_util = ResourceFileUtil(resx_path)
CSFileLocalization.resource_util = rf_util

for (dirpath, dirnames, filenames) in walk(sources_path):
    for filename in filenames:
        print (os.path.join(dirpath, filename))
        (name, ext) = os.path.splitext(filename)
        if (ext == ".cs"):
            file_localization = CSFileLocalization(os.path.join(dirpath, filename))
            file_localization.localize()
            file_localization.save()
rf_util.update_resource()