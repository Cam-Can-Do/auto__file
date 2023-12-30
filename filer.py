import os
import shutil
from pathlib import Path
import re
import time
import logging
import argparse
from pytrie import StringTrie

class Filer:
    # enable logging
    logging.basicConfig(filename='auto__file.log', format='%(message)s', encoding='utf-8', level=logging.INFO)
    __flag_pattern = r'[^_]+__'   # matches flags in a string
    __flag_dir_trie = StringTrie() # trie to store flag prefixes
    __source_dir = None

    # reads config file and initializes variables
    def __init__(self, conf_file):
        self.__config = conf_file
        with open(self.__config, 'r') as fin:
            # read flags and their corresponding path from each line of config
            for line in fin.readlines():
                line = line.strip()
                if line.startswith("#") or line == "":    # ignore comments and empty lines
                    continue
                # source dir is expected as the first valid line of the config
                if not self.__source_dir:   
                    self.__source_dir = Path(line).expanduser()
                else:
                    flag, conf_path = line.split("/->/")
                    self.__flag_dir_trie[flag] = conf_path

        # Log program start, config file import, and rules imported.
        logging.info("=" * 50)
        logging.info("AUTO__FILER RUNNING")
        logging.info("=" * 50)
        logging.info("Config file imported:")
        for flag, path in self.__flag_dir_trie.items():
            logging.info(f"\t{flag} -> {path}")
        logging.info("Files:")

    # writes a string to the config file
    def add_entry(self, flags, path):
        with open(self.__config, 'a') as fin:
            fin.write(f"{flags}/->/{path}\n")
            self.__flag_dir_trie[flags] = path
            logging.info(f"Added to config and program memory: {flags}/->/{path}")


    def run(self):
        # 'ls' in __source_dir to parse filenames
        files = os.listdir(self.__source_dir)
        for filename in files:
            flag_matches = re.findall(self.__flag_pattern, filename)
            if not flag_matches:    # if no flags are found in a filename skip it
                continue
            logging.info("-" * 50)
            logging.info(f"File {filename} has flags: {flag_matches}")

            if " " in filename:
                filename.replace(" ", "_")

            # for seperating flags vs name in filename
            first_flag = flag_matches[0]
            last_flag = flag_matches[-1]
            first_flag_index = filename.rfind(first_flag)
            last_flag_index = filename.rfind(last_flag) + len(last_flag)

            # everthing after the last flag
            new_name = filename[last_flag_index:]
            # everything between (including) the first and last flags
            all_flags = filename[first_flag_index:last_flag_index]


            # consecutuve flags already present in self.__flag_dir_trie
            contained_flags = ""
            # flags not yet recorded
            remaining_flags = ""

            # starting at the last flag, find the longest series of 
            # consecutive flags that's in the trie
            for i in range(len(flag_matches), -1, -1):
                candidate_flags = "".join(flag_matches[:i])
                if candidate_flags not in self.__flag_dir_trie:
                    continue
                else:   # if current candidate flags are in the trie
                    contained_flags = candidate_flags
                    remaining_flags = "".join(flag_matches[i:])
                    break

            # set contained_flags -- if none, needs to be "~/"" for the path's start
            if len(contained_flags) > 0:
                contained_dir = self.__flag_dir_trie[contained_flags]
            else:
                contained_dir = "~/"
                remaining_flags = all_flags

            # convert remaining flags to path form, each representing a dir
            remaining_dir = remaining_flags.replace("__", "/")


            logging.info(f"Contained flag mappings: {contained_flags} -> {contained_dir}")
            logging.info(f"Remaining flags: {remaining_flags} -> {remaining_dir}")

            dest_dir = contained_dir + remaining_dir

            # update trie and config file if there were any new flags
            if all_flags not in self.__flag_dir_trie:
                self.add_entry(all_flags, dest_dir)

            dest_path = Path(dest_dir).expanduser()
            dest_name = dest_path / new_name
            logging.info(f"Dest path: {dest_path}")

            # create the destination directory if it doesn't exist
            os.makedirs(dest_path, exist_ok=True)
            logging.info(f"Created dir: {Path(dest_dir).expanduser()}")
            # rename/move file to the destination indicated by its flags,
            # new name no longer contains flags
            logging.info(f"Moved {str(Path(self.__source_dir).joinpath(filename))} to {dest_name}")
            shutil.move(Path(self.__source_dir).joinpath(filename), dest_name)

# Run program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to config file.")
    parser.add_argument('config_file', help='Path to the configuration file')
    args = parser.parse_args()
    config_file_path = args.config_file
    instance = Filer(config_file_path)
    instance.run()