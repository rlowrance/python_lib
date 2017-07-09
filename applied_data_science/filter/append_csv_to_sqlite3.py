'''filter to append a csv file to a sqlite3 data base file with a specfied table name

INVOCATION
 python append_csv_to_sqlite3.py in_csv in_db out_db --table_name TABLENAME

Copyright 2017 Roy E. Lowrance

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on as "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing premission and
limitation under the license.
'''
import pdb

from applied_data_science.filter.Control import Control


def do_work(control):
    pdb.set_trace()
    pass


def main():
    pdb.set_trace()
    control = Control(
        input_file_names=['csv'],
        output_file_names=['sqlite3'],
        settings_value=['table_name'],
        executable_name='append_csv_to_sqlite3',
    )
    control.parse_invocation()  # take invocation from sys.argv
    return_code = control.do_work(do_work)
    control.terminate(return_code)


if __name__ == '__main__':
    main()
    if False:
        pdb
