

import argparse

def main():
    parser = argparse.ArgumentParser(description="pdf4md: convert markdown to pdf")
    parser.add_argument("files", type=str, nargs='+', help="markdown filename", metavar='FILE')
    args = parser.parse_args()
    print(args.files)
