#!/usr/bin/env python

# flake8: noqa E501


from automatic_script_generator import all_files_generator


def main_func(args):
    excel_sheet = args.excelfile
    base_script = args.basescript
    results_dir = args.resultsdir
    all_files_generator(excel_sheet, base_script, results_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="count words or characters")
    parser.add_argument("excelfile", type=str, nargs="?", help="Input excel sheet")
    parser.add_argument(
        "basescript",
        type=str,
        nargs="?",
        help="Input base script for high-throughput run",
    )
    parser.add_argument(
        "resultsdir",
        type=str,
        nargs="?",
        help="Input results directory for storing generated files",
    )

    args = parser.parse_args()
    main_func(args)
