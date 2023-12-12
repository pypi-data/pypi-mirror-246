from pathlib import Path

import pandas as pd
from metakernel import Magic, option


class SaveToMagic(Magic):

    def cell_save_to(self, filepath):
        """
        %%save_to PATH - save the query result to a JSON file.

        This cell magic will save the Sparrow query result to a file.

        Example:
            %%save_to /path/to/file.json
        """
        json_str = self.kernel.get_variable('previous_query_result')
        if json_str is None:
            self.kernel.Error('No previous Sparrow query result found')
            return

        if not isinstance(json_str, str):
            self.kernel.Error('The previous query result is not a string!')
            return

        filepath = Path(filepath).expanduser().absolute()
        with filepath.open('w') as fp:
            fp.write(json_str)

        self.kernel.Print(f'Query result saved to {str(filepath)}')


def register_magics(kernel):
    kernel.register_magics(SaveToMagic)
