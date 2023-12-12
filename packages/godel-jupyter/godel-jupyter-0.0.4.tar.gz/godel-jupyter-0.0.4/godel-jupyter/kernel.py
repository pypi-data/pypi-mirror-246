from __future__ import print_function

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Tuple

import pandas as pd
from IPython.display import HTML
from metakernel import MetaKernel
from .magics.db_magic import DBMagic
from .magics.save_to_magic import SaveToMagic

from . import __version__

OUPUT_RESULT_LIMIT = 10


def get_kernel_json():
    """Get the kernel json for the kernel.
    """
    here = os.path.dirname(__file__)
    with open(os.path.join(here, 'kernel.json')) as fid:
        data = json.load(fid)
    data['argv'][0] = sys.executable
    return data


def convert_output_2_df(output_path) -> Tuple[pd.DataFrame, str]:
    with open(output_path, 'r') as fp:
        json_str = fp.read()
        data = json.loads(json_str)

    if isinstance(data, list):
        return pd.DataFrame.from_records(data), json_str
    else:
        # Deal with multi output
        df_list = []
        for key, value in data.items():
            temp_df = pd.DataFrame.from_records(value,
                                                index=pd.MultiIndex.from_tuples(
                                                    [(key, i) for i in range(len(value))]))
            df_list.append(temp_df)
        df = pd.concat(df_list)
        return df, json_str


class GodelKernel(MetaKernel):
    app_name = 'godel'
    implementation = 'Godel kernel'
    implementation_version = __version__
    language = 'rust'
    language_version = __version__
    banner = "Godel kernel"
    help_links = [
        {
            'text': "Godel kernel Magics",
            'url': "https://sparrow.alipay.com",
        },
    ]
    language_info = {
        'mimetype': 'text/rust',
        'name': 'rust',
        'file_extension': '.gdl',
        "version": __version__,
        'help_links': help_links,
    }
    kernel_json = get_kernel_json()
    variables = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_magics(DBMagic)
        self.register_magics(SaveToMagic)

    def set_variable(self, name, value):
        """
        Set a variable to a Python-typed value.
        """
        self.variables[name] = value

    def get_variable(self, name):
        """
        Lookup a variable name and return a Python-typed value.
        """
        return self.variables.get(name, None)

    def get_usage(self):
        return "This is the Godel kernel."

    def process_code(self, code, output_dir) -> Tuple[str, Path]:
        output_dir = Path(output_dir)
        script_file_path: Path = output_dir / 'query.gdl'
        with script_file_path.open('w') as fp:
            fp.write(code)

        query_command = f'sparrow query run -gdl {str(script_file_path.absolute())} -f json -o {str(output_dir.absolute())}'

        db_path = self.get_variable('sparrow_database_path')
        self.Error(f'Sparrow database is set to: {db_path}')
        if db_path:
            query_command = f'{query_command} -d {db_path}'

        return query_command, script_file_path

    def do_execute_direct(self, code, silent=False):
        if not code.strip():
            return

        shell_magic = self.line_magics['shell']
        json_str = '[]'
        with tempfile.TemporaryDirectory(prefix='godel-jupyter-') as tmpdir:
            try:
                query_command, script_file_path = self.process_code(code, tmpdir)
                self.log.debug('execute: %s' % query_command)
                resp = shell_magic.eval(query_command)
                self.Print(resp)

                output_path = script_file_path.parent / f'{script_file_path.stem}.json'
                if output_path.exists():
                    df, json_str = convert_output_2_df(output_path)
                    if df.empty:
                        self.Print('[]')
                    else:
                        len_output_result = len(df)
                        self.Print(f'Total results: {len_output_result}')
                        self.Display(HTML(df.to_html(max_rows=OUPUT_RESULT_LIMIT, notebook=True)))
            except Exception as e:
                self.Error(e)
            finally:
                self.set_variable('previous_query_result', json_str)

    def get_completions(self, info):
        shell_magic = self.line_magics['shell']
        return shell_magic.get_completions(info)

    def get_kernel_help_on(self, info, level=1, none_on_fail=False):
        code = info['code'].strip()
        if not code or len(code.split()) > 1:
            if none_on_fail:
                return None
            else:
                return ""
        shell_magic = self.line_magics['shell']
        return shell_magic.get_help_on(info, 1)
