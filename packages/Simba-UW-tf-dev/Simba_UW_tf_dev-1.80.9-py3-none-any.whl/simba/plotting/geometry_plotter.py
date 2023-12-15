import os

from shapely.geometry import (Polygon,
                              LineString,
                              Point,
                              MultiPolygon,
                              MultiLineString,
                              GeometryCollection,
                              MultiPoint)

from typing import Optional, List, Union, Tuple, Iterable
from simba.mixins.config_reader import ConfigReader
from simba.utils.checks import (check_file_exist_and_readable,
                                check_instance,
                                check_iterable_length)
from simba.utils.errors import InvalidInputError

ACCEPTED_TYPES = [Polygon, LineString]

class GeometryPlotter(ConfigReader):

    def __init__(self,
                 config_path: Union[str, os.PathLike],
                 geometries: List[List[Union[Polygon, LineString]]]):

        check_file_exist_and_readable(file_path=config_path)
        check_instance(source=self.__class__.__name__, instance=geometries, accepted_types=list)
        check_iterable_length(source=self.__class__.__name__, val=len(geometries), min=1)
        shape_types = set()
        for i in geometries: shape_types.update(set([type(x) for x in i]))
        for i in shape_types:
            if i not in [Polygon, LineString]:
                raise InvalidInputError(msg=f'geometries contain an invalid datatype {i}. Accepted: {ACCEPTED_TYPES}', source=self.__class__.__name__)

        ConfigReader.__init__(self, config_path=config_path)
