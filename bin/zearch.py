#!/usr/bin/env python
import argparse, os
from zearch import Zearch, Config

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def main():
	parser = argparse.ArgumentParser(description='Zendesk Search Coding Exercise')
	parser.add_argument('--file_dir', type=dir_path,
        help='the firectory where the searc content json files are')
	args = parser.parse_args()
	Zearch(config=Config(args)).run()

if __name__ == "__main__":
	main()