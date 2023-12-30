# auto__filer
A file sorter application for Linux that follows rules stored in a configuration file, but also sorts dynamically in the absense of an appropriate rule.

A program that monitors a "source" directory (expected to be specified in the first non-commented line of config file) for files that contain "__" (double underscores) in their name. Text followed by a double underscore is a flag. Flags can be specified in .config.txt, and act as a shortcut to a path on the system. See comments in '.config.txt' for more information.

The source directory and flags are read into the program and stored in a trie. I chose a trie because I wanted to be able to chain multiple flags together consecutively, and a trie is an efficient way to store and search strings with common prefixes.

When the program detects a filename in the source directory that contains a flag, it constructs a destination path and renames the file to strip the original flags and move it to the appropriate directory. If a filename contains flags that are not present in the config file, the program assumes that the first flag should be a directory within the user's home directory. New flags and their assumed paths are automatically added to the trie and config file.

Each action performed by the program is logged in `auto__file.log`.
