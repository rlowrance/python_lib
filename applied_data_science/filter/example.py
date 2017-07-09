'''node usage

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

def main():
    output = SQLiteSelect(
        input='path/to/csv file',
        output='result of query',
        settings={
            'statement': 'select a, avg(b), max(c) where c > 10 ordered by d'
        }
    )
    file1 = CSVReader(
        input='path/to/file',
        settings={
            'has_header': True,
        },
    )
    n1 = ColumnFilter(
        setting={
            exclude='id',
        },
        inputs={
            input_file=file1,
        },
    )
    rf_model = RandomForestsRegressor(
        settings={
            max_depth=10,
            n_estimators=100,
        },
        inputs={
            input_files=n1,
        }
    )
    predictions = Predict(
        inputs={
            fitted_model=n1,  # bad practice
            ...
        },
    )