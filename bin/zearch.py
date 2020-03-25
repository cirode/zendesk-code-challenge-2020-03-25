#!/usr/bin/env python

import argparse, os
from zearch import Zearch, Config

def main():
	parser = argparse.ArgumentParser(description="Zearch, the Zendesk Search Cli")
	parser.add_argument('--file_dir',
        help='the firectory where the searc content json files are', required=True)
	args = parser.parse_args()
	Zearch(config=Config(args)).run()

if __name__ == "__main__":
	main()