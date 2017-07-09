'''
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
import sqlite3

class SQLLiteCreateTableAsSelect(object):
    def __init__(self, input, output, settings):
        self.input = input
        self.output = output
        self.settings = settings
        required_settings = ('selected_statement',)
        for required_setting in required_settings:
            assert required_setting in settings

    def run(self):
        # problem: need connection for input and for output
        # maybe: read the input and create a temp table in the output database
        conn = sqlite3.connect(self.input)
        c = conn.cursor()
        create_table_statement = 'create temp table %s as %s' % (
            self.output,
            self.settings['select_statement'],
        )
        c.execute(self.make_create_table_statement(self.settings['statement']))
        c.write()  # TODO: figure out how to write the resulting table
