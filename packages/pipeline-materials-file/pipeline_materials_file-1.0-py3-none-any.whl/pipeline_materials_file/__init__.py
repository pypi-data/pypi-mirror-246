"""Materials csv stuff."""
import os
import csv
from operator import attrgetter

from pipeline_material import PipeMaterial
from pipeline_csv import TypeHorWeld


class PipeType:
    """Weld type_id field values."""

    DIRECT = 0
    SPIRAL = 1
    EMPTY = 2


PIPE_TYPE_IV = {
  TypeHorWeld.HORIZONTAL: PipeType.DIRECT,
  TypeHorWeld.SECOND: PipeType.DIRECT,
  TypeHorWeld.NO_WELD: PipeType.EMPTY,
  TypeHorWeld.SPIRAL: PipeType.SPIRAL,
  TypeHorWeld.UNKNOWN: PipeType.DIRECT,
}


def float2str(val, decimal=2):
    """Format float as string."""
    if val is None:
        return ''
    mask = "%0.0" + str(decimal) + "f"
    ret = mask % val
    return ret.replace('.', ',')


def str2float(text):
    """Restore float from string."""
    return float(text.replace(',', '.'))


class Material(PipeMaterial):  # pylint: disable=too-many-instance-attributes
    """Pipe material."""

    DFLT_NAME = "Steel"
    DFLT_SMYS = 295
    DFLT_SMTS = 405
    DFLT_TOUG = 64

    def __init__(self):
        """Make new material."""
        super().__init__(self.DFLT_NAME, self.DFLT_SMYS)
        self.smts = self.DFLT_SMTS
        self.toughness = self.DFLT_TOUG

        self.type_id = None
        self.thick = None
        self.steel_class = ''
        self.pipe_count = 0

    @classmethod
    def from_csv_row(cls, row):
        """Create material from csv file row."""
        obj = cls()

        obj.name = row[6]
        obj.smys = str2float(row[2])
        obj.smts = str2float(row[3])
        if row[4]:
            obj.toughness = str2float(row[4])

        obj.type_id = int(row[5])
        obj.thick = int(str2float(row[0]) * 10)
        obj.steel_class = row[7]
        obj.pipe_count = int(row[8])

        return obj

    @property
    def key(self):
        """Pipe key."""
        return (self.thick, self.type_id)


class Materials:
    """List of materials for pipline."""

    file_name = "materials.csv"
    encoding = 'windows-1251'  # 'utf-8'

    def __init__(self):
        """Make new material list."""
        self.type_name = {
          PipeType.DIRECT: "Direct seam",
          PipeType.SPIRAL: "Spiral seam",
          PipeType.EMPTY: "No seam",
        }
        self.data = {}

    @classmethod
    def from_deftable(cls, deftable, warnings):
        """Create material from csv File object."""
        obj = cls()
        for pipe in deftable.get_tubes(warnings):
            key = (pipe.thick, PIPE_TYPE_IV[pipe.typ])
            if key not in obj.data:
                obj.data[key] = Material()
            obj.data[key].pipe_count += 1
            obj.data[key].thick = key[0]
            obj.data[key].type_id = key[1]

        return obj

    def to_csv(self, file_name):
        """Save data to csv file."""
        with open(file_name, 'wt', encoding=self.encoding) as output:
            writer = csv.writer(output, delimiter=';', lineterminator='\n')
            writer.writerow([
              "Thick, mm",
              "Type",
              "SMYS, MPa",
              "SMTS, MPa",
              "Toughness",
              "Code",
              "Steel mark",
              "Steel class",
              "Pipe count",
            ])
            for item in sorted(self.data.values(), key=attrgetter('thick', 'type_id')):
                writer.writerow([
                  float2str(item.thick / 10.0, decimal=1) if item.thick else '',
                  self.type_name[item.type_id],
                  float2str(item.smys),
                  float2str(item.smts),
                  float2str(item.toughness),
                  str(item.type_id),
                  item.name,
                  item.steel_class,
                  str(item.pipe_count),
                ])

        return len(self.data)

    @classmethod
    def from_csv(cls, file_path):
        """Restore materials from given csv file."""
        obj = cls()
        if not os.path.isfile(file_path):
            return obj

        with open(file_path, 'rt', encoding=cls.encoding) as inp:
            reader = csv.reader(inp, delimiter=';', lineterminator='\n')
            next(reader)  # skip column titles row
            for row in reader:
                item = Material.from_csv_row(row)
                obj.data[item.key] = item

        return obj

    def for_pipe(self, pipe):
        """Return material for pipeline_csv.tubes.Tube."""
        key = (pipe.thick, PIPE_TYPE_IV[pipe.typ])

        return self.data[key]
