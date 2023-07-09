import os
import shutil
from pathlib import Path
import re
import time

class Filer:

    home_dir_pattern = r'^.*~/'
    flag_pattern = r'^.*?__'
    flag_dir_map = {}

    source_input = ""
    source_dir = ""

    def __init__(self, conf_file):

        with open(conf_file, 'r') as fin:
            self.source_input = fin.readline().strip()
            self.source_dir = Path(os.path.join(os.path.expanduser("~"), re.sub(self.home_dir_pattern,'', self.source_input)))

            next(fin)
            for line in fin.readlines():
                flag, conf_path = line.split(' ')
                self.flag_dir_map[flag] = Path(os.path.join(os.path.expanduser("~"), re.sub(self.home_dir_pattern,'', conf_path.strip())))
        

    def run(self):
        while True:
            files = os.listdir(self.source_dir)     # list the files in source_dir
            for filename in files:
                new_flag_key = ""
                dest_dir = ""   # destination dir; where the file is to be sent
                reduced_name = filename 
                match = re.search(self.flag_pattern, filename)
                while match:   # while flag pattern is contained in the filename...

                    if match.group(0) in flag_dir_map:  # if the matching flag is already in our map
                        reduced_name = (re.sub(flag_pattern, '', filename)).strip()
                        dest_dir.join("/", flag_dir_map[match_str])
                        filename = filename[]
                    else:
                        new_flag_key += str(match)

                        if len(dest_dir) > 0:   # initialize destination with home dir if empty
                            dest_dir = Path(os.path.expanduser("~"))


                flag_dir_map["new_flag_key"] = dest_dir     # add our new path to our known paths 
                new_file = dest_dir / reduced_name
                shutil.move(str(start_file), str(new_file))

                time.sleep(.01)


