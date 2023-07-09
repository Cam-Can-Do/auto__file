import os
import shutil
from pathlib import Path
import re
import time
from pytrie import StringTrie

class Filer:
    flag_pattern = r'[^_]+__'
    flag_dir_trie = StringTrie()
    source_dir = ""

    def __init__(self, conf_file):
        with open(conf_file, 'r') as fin:
            self.source_input = fin.readline().strip()
            self.source_dir = Path(self.source_input).expanduser()

            for line in fin.readlines():
                flag, conf_path = line.split(' ')
                self.flag_dir_trie[flag] = conf_path.strip()

            for key, val in self.flag_dir_trie.items():
                print(f"{key}, {val}")

    def run(self):
        while True:
            files = os.listdir(self.source_dir)
            for filename in files:
                remaining_flags = ""
                flag_matches = re.findall(self.flag_pattern, filename)
                if not flag_matches:
                    continue

                last_flag = flag_matches[-1]
                last_flag_index = filename.rfind(last_flag) + len(last_flag)
                new_name = filename[last_flag_index:]

                print(f"FLAG_MATCHES: {flag_matches}")
                dest_dir = "~/"
                for i in range(len(flag_matches) - 1, -1, -1):
                    print(f"i: {i}")
                    print(f"flag match: {flag_matches[i]}")
                    contained_flags = "".join(flag_matches[:i])
                    print(f"CONTAINED_FLAGS: {contained_flags}")
                    '''
                    if contained_flags not in self.flag_dir_trie:
                        continue
                    '''

                    remaining_flags = "".join(flag_matches[i:])
                    print(f"REMAINING_FLAGS: {remaining_flags}")
                    remaining_dir = remaining_flags.replace("__", "/")
                    print(remaining_dir)
                    contained_dir = self.flag_dir_trie[contained_flags] if len(contained_flags) > 0 else "~/"
                    dest_dir = contained_dir + remaining_dir + new_name
                    break

                dest_path = Path(dest_dir).expanduser()

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                shutil.move(os.path.join(str(self.source_dir), filename), dest_path)

            time.sleep(0.01)
