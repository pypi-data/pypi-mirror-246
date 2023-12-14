import sys
import os
sys.path.append("../../pbx")
from kl_pbx import PBXProjectHelper
def Test():
    cur_path=os.path.abspath(os.curdir)
    main_target="UnityFramework"
    projectpath = os.path.join(cur_path, "project.pbxproj")
    pbx_helpr = PBXProjectHelper(projectpath)
    pbx_helpr.remo

if __name__ == "__main__":
    Test()