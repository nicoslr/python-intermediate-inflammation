#!/usr/bin/env python3
"""Software for managing and analysing patients' inflammation data in our imaginary hospital."""

import argparse
import os
import glob

from inflammation import models, views


class CSVDataSource:
    """
    Loads all the inflammation CSV files within a specified directory.
    """
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load_inflammation_data(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'inflammation*.csv'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation CSV files found in path {self.dir_path}")
        data = map(models.load_csv, data_file_paths)
        return list(data)

class JSONDataSource:
  """
  Loads patient data with inflammation values from JSON files within a specified folder.
  """
  def __init__(self, dir_path):
    self.dir_path = dir_path

  def load_inflammation_data(self):
    data_file_paths = glob.glob(os.path.join(self.dir_path, 'inflammation*.json'))
    if len(data_file_paths) == 0:
      raise ValueError(f"No inflammation JSON files found in path {self.dir_path}")
    data = map(models.load_json, data_file_paths)
    return list(data)

def main(args, extension=None):
    """The MVC Controller of the patient inflammation data system.

    The Controller is responsible for:
    - Selecting the necessary models and views for the current task
    - Passing data between models and views
    """
    infiles = args.infiles
    if not isinstance(infiles, list):
        infiles = [args.infiles]

    if args.full_data_analysis:
        _, extension = os.path.splitext(infiles[0])
        if extension == '.json':
                data_source = JSONDataSource(os.path.dirname(infiles[0]))
        elif extension == '.csv':
            data_source = CSVDataSource(os.path.dirname(infiles[0]))
        else:
            raise ValueError(f'Unsupported data file format: {extension}')
        data_result = models.analyse_data(data_source)
        graph_data = {
            'standard deviation by day': data_result,
        }
        views.visualize(graph_data)
        return

    for filename in infiles:
        inflammation_data = models.load_csv(filename)

        view_data = {
            'average': models.daily_mean(inflammation_data),
            'max': models.daily_max(inflammation_data),
            'min': models.daily_min(inflammation_data)
        }

        views.visualize(view_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'A basic patient inflammation data management system'
    )

    parser.add_argument(
        'infiles',
        nargs = '+',
        help = 'Input CSV(s) containing inflammation series for each patient'
    )

    parser.add_argument(
        '--full-data-analysis',
        action='store_true',
        dest='full_data_analysis')

    args = parser.parse_args()

    main(args)
