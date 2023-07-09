import os
import shutil
from pathlib import Path
import re
import time
from pytrie import StringTrie

class Filer:
    flag_pattern = r'[^_]+__'   # matches flags in a string
    flag_dir_trie = StringTrie() # trie to store flag prefixes

    # reads config file and initializes variables
    def __init__(self, conf_file):
        self.__config = conf_file
        with open(self.__config, 'r') as fin:
            source_input = fin.readline().strip()  # source path stored in first line of config
            self.__source_dir = Path(source_input).expanduser()

            # read flags and their corresponding path from each line of config
            for line in fin.readlines():
                if line.startswith("#"):    # ignore comments
                    continue
                flag, conf_path = line.split(' ')
                self.flag_dir_trie[flag] = conf_path.strip()

    # writes a string to the config file
    def write_config(self, line):
        with open(self.__config, 'a') as fin:
            fin.write(line + '\n')


    def run(self):
        while True:
            # 'ls' in __source_dir to parse filenames
            files = os.listdir(self.__source_dir)
            for filename in files:
                flag_matches = re.findall(self.flag_pattern, filename)
                if not flag_matches:    # if no flags are found in a filename skip it
                    continue

                # for seperating flags vs name in filename
                first_flag = flag_matches[0]
                last_flag = flag_matches[-1]
                first_flag_index = filename.rfind(first_flag)
                last_flag_index = filename.rfind(last_flag) + len(last_flag)

                # everthing after the last flag
                new_name = filename[last_flag_index:]
                # everything between (including) the first and last flags
                all_flags = filename[first_flag_index:last_flag_index]

                # print(f"FLAG_MATCHES: {flag_matches}")
                # consecutuve flags already present in self.flag_dir_trie
                contained_flags = ""
                # flags not yet recorded
                remaining_flags = ""

                # starting at the last flag, find the longest series of 
                # consecutive flags that's in the trie
                for i in range(len(flag_matches) - 1, -1, -1):
                    candidate_flags = "".join(flag_matches[:i])
                    if candidate_flags not in self.flag_dir_trie:
                        continue
                    contained_flags = candidate_flags
                    remaining_flags = "".join(flag_matches[i:])
                    break

                #print(f"CONTAINED_FLAGS: {contained_flags} -> {self.flag_dir_trie[contained_flags]}")

                # convert remaining flags to path form, each representing a dir
                remaining_dir = remaining_flags.replace("__", "/")
                # print(f"REMAINING_FLAGS: {remaining_flags} -> {remaining_dir}")

                # set contained_flags -- if none, needs to be "~/"" for the path's start
                if len(contained_flags) > 0:
                    contained_dir = self.flag_dir_trie[contained_flags]
                else:
                    contained_dir = "~/"

                dest_dir = contained_dir + remaining_dir

                # update trie and config file if there were any new flags
                if all_flags not in self.flag_dir_trie:
                    self.flag_dir_trie[all_flags] = dest_dir
                    self.write_config(f"{all_flags} {dest_dir}")

                dest_path = Path(dest_dir + new_name).expanduser()
                # print(dest_path)

                # create the destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                # rename/move file to the destination indicated by its flags,
                # new name no longer contains flags
                shutil.move(os.path.join(str(self.__source_dir), filename), dest_path)

            # time delay to mitigate overhead of continuously running the loop
            time.sleep(0.1)
