# Pipeline materials file for static integrity calculation
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/pipeline.materials.file/pep257.yml?label=Pep257&style=plastic&branch=main)](https://github.com/vb64/pipeline.materials.file/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/pipeline.materials.file/py3.yml?label=Python%203.7-3.11&style=plastic&branch=main)](https://github.com/vb64/pipeline.materials.file/actions?query=workflow%3Apy3)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/69be4438e2824797b75fc9ef3058f84d)](https://app.codacy.com/gh/vb64/pipeline.materials.file/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

## Installation

```bash
pip install pipeline-materials-file
```

## Usage

```python
from pipeline_materials_file import Materials
from pipeline_csv.csvfile import File
from pipeline_csv.csvfile.row import Row

deftable = File(1000)
deftable.data = [
  Row.as_weld(1000),
  Row.as_thick(1010, 105),
  Row.as_weld(12000),
  Row.as_thick(12010, 110),
  Row.as_weld(24000),
  Row.as_thick(12010, 110),
  Row.as_weld(36000),
]

warnings = []
data = Materials.from_deftable(deftable, warnings)

assert len(data.data) == 2
assert not warnings

data.to_csv('materials.csv')

```

## Development

```
$ git clone git@github.com:vb64/pipeline.material.git
$ cd pipeline.material
$ make setup PYTHON_BIN=/path/to/python3
$ make tests
```
