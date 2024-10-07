import logging
import os
from os import path

logger = logging.getLogger(__name__)

class Cache:
    def __init__(self, key):
        cache_dir = path.join(path.dirname(path.abspath(__file__)), 'cache')
        if not path.exists(cache_dir):
            logger.info('Creating cache directory')
            os.mkdir(cache_dir)
        self.cache_dir = cache_dir
        self.key = key

    def file(self) -> str:
        return path.join(self.cache_dir, f'{self.key}.csv')

    def write(self, entries: [dict]):
        """
        This function writes the cache to a CSV file.
        :param entries: A dictionary with the entries to write.
        :return:
        """
        # Get the keys of all the entries
        keys = entries[0].keys()
        # Create the CSV file
        with open(self.file(), 'w') as file:
            # Write the header
            file.write(','.join(keys) + '\n')
            # Write the entries
            for entry in entries:
                # We also replace commas and new lines with their escape sequences
                file.write(','.join(value.replace('\n', '\\n').replace(',', '\\u002c') for value in entry.values()) + '\n')

    def read(self) -> [dict]:
        """
        This function reads the cache from a CSV file.
        :return:
        """
        if not path.exists(self.file()):
            return []
        entries = []
        with open(self.file(), 'r') as file:
            keys = file.readline().strip().split(',')
            for line in file.readlines():
                values = (value.replace('\\n', '\n').replace('\\u002c', ',') for value in line.strip().split(','))
                entries.append(
                    dict(zip(keys, values))
                )
        return entries
