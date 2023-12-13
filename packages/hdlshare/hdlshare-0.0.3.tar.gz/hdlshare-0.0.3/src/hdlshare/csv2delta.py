
import argparse
from pathlib import Path

import rich
import pandas as pd
from deltalake import write_deltalake



def main():

    parser = argparse.ArgumentParser(prog='csv2delta',
                                     description='Converts csv-file to deltalake format.')

    # positional argument
    parser.add_argument("csv_file",  help="csv-file")
    # parser.add_argument("-H","--header",  help="csv-file", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)
    print(df)

    delta_file = Path(args.csv_file)
    delta_folder = delta_file.parent / delta_file.stem
    print(delta_folder)

    write_deltalake(delta_folder, df)


if __name__ == '__main__':
    main()