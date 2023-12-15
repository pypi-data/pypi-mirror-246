import abc
import json
import os
from abc import ABC
from typing import Union
from datetime import datetime

from .odata_utils import ODataQueryPredicate

from enum import Enum


def footprint_extract(geojson_obj):
    """
    Extract the footprint from a GeoJson.

    :param geojson_obj: (dict) the data extracted from a json file.
    :return: A list of coordinates
    """
    if "coordinates" in geojson_obj:
        geo_obj = geojson_obj
    elif "geometry" in geojson_obj:
        geo_obj = geojson_obj["geometry"]
    else:
        geo_obj = {"type": "GeometryCollection", "geometries": []}
        for feature in geojson_obj["features"]:
            geo_obj["geometries"].append(feature["geometry"])

    def ensure_2d(geo_obj):
        if isinstance(geo_obj[0], (list, tuple)):
            return list(map(ensure_2d, geo_obj))
        else:
            return geo_obj[:2]

    def check_bounds(geo_obj):
        if isinstance(geo_obj[0], (list, tuple)):
            return list(map(check_bounds, geo_obj))
        else:
            if geo_obj[0] > 180 or geo_obj[0] < -180:
                raise ValueError("Longitude is out of bounds,"
                                 "check your JSON format or data ")
            if geo_obj[1] > 90 or geo_obj[1] < -90:
                raise ValueError("Latitude is out of bounds, "
                                 "check your JSON format or data")

    # Discard z-coordinate, if it exists
    if geo_obj["type"] == "GeometryCollection":
        for idx, geo in enumerate(geo_obj["geometries"]):
            geo_obj["geometries"][idx]["coordinates"] = ensure_2d(
                geo["coordinates"])
            check_bounds(geo["coordinates"])
    else:
        geo_obj["coordinates"] = ensure_2d(geo_obj["coordinates"])
        check_bounds(geo_obj["coordinates"])

    return geo_obj['geometries'][0]['coordinates'][0]


class ProductCollection(Enum):
    Sentinel1 = 1
    Sentinel2 = 2
    Sentinel3 = 3
    Sentinel5p = 5


class QueryFilter(abc.ABC):
    """
    Abstract class for building filter queries

    Attributes:
    ----------

    Methods:
    -------


    """
    _filter_list = None

    def __init__(self):
        self._filter_list = []

    @property
    def tag_product_name(self):
        raise NotImplementedError

    @property
    def tag_product_sensing_date(self):
        raise NotImplementedError

    @property
    def tag_cloud_attribute(self):
        raise NotImplementedError

    @property
    def tag_product_type_attribute(self):
        raise NotImplementedError

    @property
    def tag_product_online(self):
        raise NotImplementedError

    @property
    def join_and(self) -> str:
        raise NotImplementedError

    def _format_full_predicate(self, predicate: str):
        return predicate

    def build_filter(self):
        """
        build the full filter query by joining each query with and operator

        Returns
        ----------
        the full query predicate filter

        """
        full_predicate = self.join_and.join(self._filter_list)
        full_predicate = self._format_full_predicate(full_predicate)
        return ODataQueryPredicate(filter=full_predicate)

    def add_odata_filter(self, filters: str = None) -> None:
        """
        Add a odata filter written by user
        Ex : startswith({key_name}, 'S2')

        Parameters
        ----------
        filters : str
            an Odata query written by user and ready to be applied.
            by default None.
        """

        if filters is not None and len(filters) > 0:
            self._filter_list.append(filters)

    def clear_filter(self):
        """
        Clear the list of filter prepared
        """
        self._filter_list = []

    @abc.abstractmethod
    def add_string_filter(self, tag: str = None,
                          startswith: Union[tuple, str] = (),
                          endswith: Union[tuple, str] = (),
                          contains: Union[tuple, str] = (),
                          contains_all: Union[tuple, str] = ()
                          ):
        """
        Add a filter on a string product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "Name".
        startswith : Union[tuple, str]
            the substring or list of substring that tag content must start with
            (ex: the tag content starts with "g" or
            starts either with "g" or "h")
        endswith : Union[tuple, str]
            the substring or list of substring that tag data must end with
            (ex: the tag content ends with "g" or
            ends either with "g" or "h")
        contains : Union[tuple, str]
            the substring or list of substring that tag data must contain
            (ex: the tag content contains "g" or
            contains either "g" or "h")
        contains_all : Union[tuple, str]
            the tag data must contains all the substrings
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_date_filter(self, tag: str = None,
                        date: tuple = (None, None)):
        """
        Add a filter on a date product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "ContentDate/Start".
        date : tuple = (None, None)
            a tuple of datetime or str indicating
            the starting date (first) and ending date (last) for the request
            if the date is provided as a str the expected format is
            yyyy-MM-ddThh:mm:ss.0Z
        """
        raise NotImplementedError

    def add_product_name_filter(self,
                                startswith: Union[tuple, str] = (),
                                endswith: Union[tuple, str] = (),
                                contains: Union[tuple, str] = (),
                                contains_all: Union[tuple, str] = ()
                                ):
        """
        Add a filter on a product name

        Parameters
        ----------
        startswith : Union[tuple, str]
            the substring or list of substring that tag content must start with
            (ex: the tag content starts with "g" or
            starts either with "g" or "h")
        endswith : Union[tuple, str]
            the substring or list of substring that tag data must end with
            (ex: the tag content ends with "g" or
            ends either with "g" or "h")
        contains : Union[tuple, str]
            the substring or list of substring that tag data must contain
            (ex: the tag content contains "g" or
            contains either "g" or "h")
        contains_all : Union[tuple, str]
            the tag data must contains all the substrings
        """

        return self.add_string_filter(self.tag_product_name,
                                      startswith=startswith,
                                      endswith=endswith,
                                      contains=contains,
                                      contains_all=contains_all)

    def add_product_collections_filter(
            self,
            collection_name: Union[ProductCollection, str] = ()
    ):
        """
        Add a filter on a product collection

        Parameters
        ----------
        collection_name : Union[ProductCollection, str]
            ProductionCollection Enum contains a predefined list of collection
            of sentinel products
            if CollectionName is a string, search all product whose name starts
            with this string
        """
        f = []

        if isinstance(collection_name, str):
            f = self.add_product_name_filter(startswith=collection_name)
        elif collection_name == ProductCollection.Sentinel1:
            f = self.add_product_name_filter(startswith="S1")
        elif collection_name == ProductCollection.Sentinel2:
            f = self.add_product_name_filter(startswith="S2")
        elif collection_name == ProductCollection.Sentinel3:
            f = self.add_product_name_filter(startswith="S3")
        elif collection_name == ProductCollection.Sentinel5p:
            f = self.add_product_name_filter(startswith="S5P")
        else:
            raise ValueError(f'Invalid argument {collection_name} '
                             f'must be str or a ProductCollection')

        return f

    def add_product_sensing_date_filter(self, date: tuple = (None, None)):
        """
        Add a filter on the sensing product date

        Parameters
        ----------
        date : tuple = (None, None)
            a tuple of datetime or str indicating
            the starting date (first) and ending date (last) for the request
            if the date if provided as a str the expected format is
            yyyy-MM-ddThh:mm:ss.0Z
        """
        return self.add_date_filter(self.tag_product_sensing_date, date)

    @abc.abstractmethod
    def add_geometry_filter(self,
                            geometry: Union[tuple, str] = ()):
        """
        Add a filter to select only product having a footprint that intersects
        the wanted Region of Interest

        Parameters
        ----------
        geometry : Union[tuple, str]
            Can be a path to the geojson file containing a footprint
            or a series of coordinate containing in a tuple separated
            by a coma. default ()
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_numerical_filter(self, tag: str,
                             valcmp,
                             operator: str
                             ):
        """
        Add a filter on a numerical product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "ContentLength".
        valcmp : int, float, bool
            the numerical value which with th tag content value
            must be compared
        operator : str
            use the buil-in pythonn operator
            "<", "=<", "!=", "==", ">", ">="
            or
            "lt", "le", "ne", "eq", "gt", "ge"
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_product_online_filter(self, valcmp, operator: str):
        """
        Filter product depending on the Online parameters value

        Parameters
        ----------
        valcmp : int, float, bool
            the numerical value which with th tag content value
            must be compared
        operator : str
            use the buil-in pythonn operator
           "!=", "=="
            or
            "ne", "eq"
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_attribute_parameters(self,
                                 attribute_name: str,
                                 attribute_valcmp,
                                 operator: str = "=="):
        """
        Add a filter to select a product having a attribute value that fit the
        requirements

        Parameters
        ----------
        attribute_name : str
            the name of the attribute
        attribute_valcmp :
            the value to compare
        operator : str
            "<", "=<", "!=", "==", ">", ">="
        """
        raise NotImplementedError

    def add_product_cloud_parameters(self, valcmp, operator: str):
        """
        Add a filter to select a product having a specifying cloud coverage
        value

        Parameters
        ----------
        valcmp :
            the value to compare
        operator : str
            "<", "=<", "!=", "==", ">", ">="
        """
        return self.add_attribute_parameters(self.tag_cloud_attribute,
                                             float(valcmp),
                                             operator)

    def query_builder(self,
                      filters: str = None,
                      sensingdate: tuple = (None, None),
                      footprint: Union[tuple, str] = (),
                      mission: Union[ProductCollection, str] = (),
                      product_type: str = None):

        # id: Union[tuple, str, uuid.UUID] = (),
        # name: Union[tuple, str] = (),
        # instrument: str = None,
        # cloud: str = None, order: str = None) -> tuple:
        """
        Help to build the odata query corresponding to a series of
        filter given in argument,
        the user can give a filter already wrote and this builder
        will append it with a logical
        and to the query built.

        Parameters
        ----------
        filters: (str)
                an Odata query ready to be applied. By default None.
        sensingdate: (tuple[str, str])
                A tuple of date corresponding respectively to the
                sensing date start and sensing date stop.
                (by default (None, None)
        footprint:
            Can be a path to the geojson file containing a footprint
            or a series of coordinate containing in a tuple separated
            by a coma. default ()
        mission: Filter on the product mission which corresponds to
                the sentinel collections or a string name indicating
                the starting name convention.
                by default None
        product_type: Filter on the product type you want ot retrieve.
                         by default None
        """
        self.add_odata_filter(filters)
        self.add_product_sensing_date_filter(sensingdate)
        self.add_geometry_filter(footprint)
        self.add_product_collections_filter(mission)
        self.add_attribute_parameters(
            attribute_name=self.tag_product_type_attribute,
            attribute_valcmp=product_type)


class QueryFilterStdOdata(QueryFilter, ABC):
    """
    Class for building filter queries common to several catalogue
    """

    @property
    def tag_product_name(self):
        return "Name"

    @property
    def tag_product_sensing_date(self):
        return "ContentDate/Start"

    @property
    def tag_cloud_attribute(self):
        return "cloudCover"

    @property
    def tag_product_type_attribute(self):
        return "productType"

    @property
    def tag_product_online(self):
        return "Online"

    @property
    def join_and(self) -> str:
        return ' and '

    def build_function_filter(self,
                              name: str, tag: str,
                              values: Union[tuple, str] = (),
                              operator: str = " or "):
        """
        build the Odata string for a function name

        Parameters
        ----------
        name : name of the function
        tag : tag name to be check
        values : value(s) that must be compared with the tag content value
        operator : conditional operator used to concatenate the values
        """
        query_str = ""
        if isinstance(values, str):
            query_str = f"{name}({tag},'{values}')"
        else:
            query_tmp = ''
            for strn in values:
                if len(query_tmp) > 0:
                    query_tmp += operator
                query_tmp += f"{name}({tag},'{strn}')"
            query_str = f"({query_tmp})"

        return query_str

    def add_string_filter(self, tag: str = None,
                          startswith: Union[tuple, str] = (),
                          endswith: Union[tuple, str] = (),
                          contains: Union[tuple, str] = (),
                          contains_all: Union[tuple, str] = ()
                          ):
        """
        Add a filter on a string product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "Name".
        startswith : Union[tuple, str]
            the substring or list of substring that tag content must start with
            (ex: the tag content starts with "g" or
            starts either with "g" or "h")
        endswith : Union[tuple, str]
            the substring or list of substring that tag data must end with
            (ex: the tag content ends with "g" or
            ends either with "g" or "h")
        contains : Union[tuple, str]
            the substring or list of substring that tag data must contain
            (ex: the tag content contains "g" or
            contains either "g" or "h")
        contains_all : Union[tuple, str]
            the tag data must contains all the substrings
        """

        newfilter = []

        # tag content starts with ....
        if len(startswith) > 0:
            q = self.build_function_filter(name="startswith",
                                           tag=tag, values=startswith,
                                           operator=" or ")

            newfilter.append(q)

        # tag content ends with ....
        if len(endswith) > 0:
            q = self.build_function_filter(name="endswith",
                                           tag=tag, values=endswith,
                                           operator=" or ")

            newfilter.append(q)

        # tag content contains one of the listed substrings ....
        if len(contains) > 0:
            q = self.build_function_filter(name="contains",
                                           tag=tag, values=contains,
                                           operator=" or ")

            newfilter.append(q)

        # tag content contains all the listed substrings ....
        if len(contains_all) > 0:
            q = self.build_function_filter(name="contains",
                                           tag=tag, values=contains_all,
                                           operator=self.join_and)

            newfilter.append(q)

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter

    def _build_cmp_filter(self,
                          tag: str = None,
                          dateval: Union[datetime, str] = (),
                          operator: str = " eq "):
        """
        build the Odata cmp filter

        Parameters
        ----------
        tag : tag name to be check
        dateval : date to be evaluate with the comparison operator
        operator : operator as a string
        """
        datecmp = ""
        query_str = ""
        if isinstance(dateval, datetime):
            datecmp = dateval.strftime('%Y-%m-%dT%H:%M:%S.0Z')
        if isinstance(dateval, str):
            # check if it is correctly formated
            try:
                date_time_obj = datetime.strptime(
                    dateval, '%Y-%m-%dT%H:%M:%S.0Z')
                datecmp = date_time_obj.strftime('%Y-%m-%dT%H:%M:%S.0Z')
            except ValueError:
                raise ValueError(f"""Invalid date format {dateval}.
                    The expected date format is yyyy-MM-ddThh:mm:ss.0Z""")

        if len(datecmp) > 0:
            query_str = f"{tag} {operator} {datecmp}"

        return query_str

    def add_date_filter(self, tag: str = None,
                        date: tuple = (None, None)):
        """
        Add a filter on a date product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "ContentDate/Start".
        date : tuple = (None, None)
            a tuple of datetime or str indicating
            the starting date (first) and ending date (last) for the request
            if the date if provided as a str the expected format is
            yyyy-MM-ddThh:mm:ss.0Z
        """
        newfilter = []

        if date[0] is not None:
            q = self._build_cmp_filter(tag, date[0], "gt")
            newfilter.append(q)
        if date[1] is not None:
            q = self._build_cmp_filter(tag, date[1], "lt")
            newfilter.append(q)

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter

    def add_numerical_filter(self, tag: str,
                             valcmp,
                             operator: str
                             ):
        """
        Add a filter on a numerical product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "ContentLength".
        valcmp : int, float, bool
            the numerical value which with th tag content value
            must be compared
        operator : str
            use the buil-in pythonn operator
            "<", "=<", "!=", "==", ">", ">="
            or
            "lt", "le", "ne", "eq", "gt", "ge"
        """
        newfilter = []

        odata_operator = ""
        if operator == "<" or operator == "lt":
            odata_operator = "lt"
        elif operator == "=<" or operator == "le":
            odata_operator = "le"
        elif operator == "!=" or operator == "ne":
            odata_operator = "ne"
        elif operator == "==" or operator == "eq":
            odata_operator = "eq"
        elif operator == ">" or operator == "gt":
            odata_operator = "gt"
        elif operator == ">=" or operator == "ge":
            odata_operator = "ge"
        else:
            raise ValueError('Operator not recognize')

        newfilter = f"{tag} {odata_operator} {valcmp}"

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter

    def add_attribute_parameters(self,
                                 attribute_name: str,
                                 attribute_valcmp,
                                 operator: str = "=="):
        """
        Add a filter to select a product having a attribute value that fit the
        requirements

        Parameters
        ----------
        attribute_name : str
            the name of the attribute
        attribute_valcmp
        attribute_type
        operator : str
            "<", "=<", "!=", "==", ">", ">="
        """

        newfilter = []

        attribute_type = ""
        if isinstance(attribute_valcmp, float):
            attribute_type = "DoubleAttribute"
        elif isinstance(attribute_valcmp, int):
            attribute_type = "IntegerAttribute"
        elif isinstance(attribute_valcmp, bool):
            attribute_type = "BooleanAttribute"
        elif isinstance(attribute_valcmp, str):
            attribute_type = "StringAttribute"
        else:
            return newfilter

        odata_operator = ""
        # for all attribute type
        if operator == "!=" or operator == "ne":
            odata_operator = "ne"
        if operator == "==" or operator == "eq":
            odata_operator = "eq"

        # and now only for numerical attributes
        if attribute_type == "DoubleAttribute" or \
                attribute_type == "IntegerAttribute":
            if operator == "<" or operator == "lt":
                odata_operator = "lt"
            if operator == "=<" or operator == "le":
                odata_operator = "le"
                odata_operator = "eq"
            if operator == ">" or operator == "gt":
                odata_operator = "gt"
            if operator == ">=" or operator == "ge":
                odata_operator = "ge"

        if odata_operator and attribute_type:
            newfilter = [''.join(
                [f"Attributes/OData.CSC.{attribute_type}/any(",
                 f"att:att/Name eq '{attribute_name}' and ",
                 f"att/OData.CSC.{attribute_type}/Value {odata_operator}",
                 f" {attribute_valcmp})"])]

            self._filter_list.extend(newfilter)

        return newfilter

    def add_product_online_filter(self, valcmp, operator: str):
        """
        Filter product depending on the Online parameters value

        Parameters
        ----------
        valcmp : int, float, bool
            the numerical value which with th tag content value
            must be compared
        operator : str
            use the build-in python operator
           "!=", "=="
            or
            "ne", "eq"
        """
        return self.add_numerical_filter(
            self.tag_product_online, valcmp, operator)


class QueryFilter_CSC(QueryFilterStdOdata):
    """
    Class for building filter queries for CSC GSS catalog
    """

    def __init__(self):
        super().__init__()

    def add_geometry_filter(self,
                            geometry: Union[tuple, str] = ()):
        """
        Add a filter to select only product having a footprint that intersects
        the wanted Region of Interest. Convention pair of (long,lat) values

        Parameters
        ----------
        geometry : Union[tuple, str]
            Can be a path to the geojson file containing a footprint
            or a series of coordinate containing in a tuple separated
            by a coma. default ()
        """

        # specify geographic area
        newfilter = []

        if len(geometry) == 0:
            return newfilter

        geo = []
        if len(geometry) == 1 or isinstance(geometry, str):
            if os.path.exists(geometry[0]):
                with open(geometry[0]) as f:
                    geo = json.load(f)
            elif os.path.exists(geometry):
                with open(geometry) as f:
                    geo = json.load(f)
            geo = footprint_extract(geo)
        else:

            if isinstance(geometry[0], str):
                for e in geometry:
                    geo.append((
                        float(e.split(',')[0]),
                        float(e.split(',')[1])))
            else:
                for e in geometry:
                    geo.append((float(e[0]), float(e[1])))

        if len(geo) > 0:
            spointlist = [f"{point[0]} {point[1]}" for point in geo]
            sallpoint = ",".join(spointlist)
            filterby_geographicArea = ''.join([
                f"OData.CSC.Intersects(",
                f"area=geography'SRID=4326;POLYGON(({sallpoint}))')"])
            newfilter.append(filterby_geographicArea)

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter


class QueryFilter_DHUS(QueryFilterStdOdata):
    """
    Class for building filter queries for DHUS catalog
    """

    def __init__(self):
        super().__init__()

    def add_geometry_filter(self,
                            geometry: Union[tuple, str] = ()):
        """
        Add a filter to select only product having a footprint that intersects
        the wanted Region of Interest

        Parameters
        ----------
        geometry : Union[tuple, str]
            Can be a path to the geojson file containing a footprint
            or a series of coordinate containing in a tuple separated
            by a coma. default ()
        """
        raise NotImplementedError


class QueryFilter_DAS(QueryFilterStdOdata):
    """
    Class for building filter queries for DAS catalog
    """

    def __init__(self):
        super().__init__()

    def add_geometry_filter(self,
                            geometry: Union[tuple, str] = ()):
        """
        Add a filter to select only product having a footprint that intersects
        the wanted Region of Interest

        Parameters
        ----------
        geometry : Union[tuple, str]
            Can be a path to the geojson file containing a footprint
            or a series of coordinate containing in a tuple separated
            by a coma. default ()
        """

        # specify geographic area
        newfilter = []

        if len(geometry) == 0:
            return newfilter

        geo = []
        if len(geometry) == 1 or isinstance(geometry, str):
            if os.path.exists(geometry[0]):
                with open(geometry[0]) as f:
                    geo = json.load(f)
            elif os.path.exists(geometry):
                with open(geometry) as f:
                    geo = json.load(f)
            geo = footprint_extract(geo)
        else:

            if isinstance(geometry[0], str):
                for e in geometry:
                    geo.append((
                        float(e.split(',')[0]),
                        float(e.split(',')[1])))
            else:
                for e in geometry:
                    geo.append((float(e[0]), float(e[1])))

        if len(geo) > 0:
            spointlist = [f"{point[0]} {point[1]}" for point in geo]
            sallpoint = ",".join(spointlist)
            filterby_geographicArea = ''.join([
                f"OData.CSC.Intersects(",  # remove location=footprint
                f"area=geography'SRID=4326;POLYGON(({sallpoint}))')"])
            newfilter.append(filterby_geographicArea)

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter


class QueryFilter_Dias(QueryFilter):
    """
    Class for building filter queries for Dias catalog
    """

    def __init__(self):
        super().__init__()

    @property
    def tag_product_name(self):
        return "name"

    @property
    def tag_product_sensing_date(self):
        return "beginPosition"

    @property
    def tag_cloud_attribute(self):
        return "cloudCoverPercentage"

    @property
    def tag_product_online(self):
        return "Offline"

    @property
    def tag_product_type_attribute(self):
        return "productType"

    @property
    def join_and(self) -> str:
        return ' AND '

    def _format_full_predicate(self, predicate: str):
        return f'"{predicate}"'

    def build_string_filter(self, tag: str,
                            values: Union[tuple, str] = (),
                            operator: str = " OR "):
        """
        build the Odata string for a function name

        Parameters
        ----------
        name : name of the function
        tag : tag name to be check
        values : value(s) that must be compared with the tag content value
        operator : conditional operator used to concatenate the values
        """
        query_str = ""
        if isinstance(values, str):
            query_str = f"{tag}:{values}"
        else:
            query_tmp = ''
            for strn in values:
                if len(query_tmp) > 0:
                    query_tmp += operator
                query_tmp += f"{tag}:{strn}"
            query_str = f"({query_tmp})"
        return query_str

    def add_string_filter(self, tag: str = None,
                          startswith: Union[tuple, str] = (),
                          endswith: Union[tuple, str] = (),
                          contains: Union[tuple, str] = (),
                          contains_all: Union[tuple, str] = ()
                          ):
        """
        Add a filter on a string product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "Name".
        startswith : Union[tuple, str]
            the substring or list of substring that tag content must start with
            (ex: the tag content starts with "g" or
            starts either with "g" or "h")
        endswith : Union[tuple, str]
            the substring or list of substring that tag data must end with
            (ex: the tag content ends with "g" or
            ends either with "g" or "h")
        contains : Union[tuple, str]
            the substring or list of substring that tag data must contain
            (ex: the tag content contains "g" or
            contains either "g" or "h")
        contains_all : Union[tuple, str]
            the tag data must contains all the substrings
        """

        newfilter = []

        # tag content starts with ....
        if len(startswith) > 0:
            values = ""
            if isinstance(startswith, str):
                values = f"{startswith}*"
            else:
                values = tuple(f"{val}*" for val in startswith)

            q = self.build_string_filter(tag=tag, values=values,
                                         operator=" OR ")

            newfilter.append(q)

        # tag content ends with ....
        if len(endswith) > 0:
            values = ""
            if isinstance(endswith, str):
                values = f"*{endswith}"
            else:
                values = tuple(f"*{val}" for val in endswith)

            q = self.build_string_filter(tag=tag, values=values,
                                         operator=" OR ")

            newfilter.append(q)

        # tag content contains one of the listed substrings ....
        if len(contains) > 0:
            values = ""
            if isinstance(contains, str):
                values = f"*{contains}*"
            else:
                values = tuple(f"*{val}*" for val in contains)

            q = self.build_string_filter(tag=tag, values=values,
                                         operator=" OR ")

            newfilter.append(q)

        # tag content contains all the listed substrings ....
        if len(contains_all) > 0:
            values = ""
            if isinstance(contains_all, str):
                values = f"*{contains_all}*"
            else:
                values = tuple(f"*{val}*" for val in contains_all)

            q = self.build_string_filter(tag=tag, values=values,
                                         operator=self.join_and)

            newfilter.append(q)

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter

    def _build_cmp_filter(self,
                          tag: str = None,
                          dateval: Union[datetime, str] = (),
                          operator: str = "* TO "):
        """
        build the Odata cmp filter

        Parameters
        ----------
        tag : tag name to be check
        dateval : date to be evaluate with the comparison operator
        operator : operator as a string
        """
        datecmp = ""
        query_str = ""
        if isinstance(dateval, datetime):
            datecmp = dateval.strftime('%Y-%m-%dT%H:%M:%S.0Z')
        if isinstance(dateval, str):
            # check if it is correctly formated
            try:
                date_time_obj = datetime.strptime(
                    dateval, '%Y-%m-%dT%H:%M:%S.0Z')
                datecmp = date_time_obj.strftime('%Y-%m-%dT%H:%M:%S.0Z')
            except ValueError:
                raise ValueError(f"""Invalid date format {dateval}.
                    The expected date format is yyyy-MM-ddThh:mm:ss.0Z""")

        if len(datecmp) > 0 and len(operator) > 0:
            if operator[0] == '*':
                query_str = f"{tag}:[{operator} {datecmp}]"
            if operator[-1] == '*':
                query_str = f"{tag}:[{datecmp} {operator}]"

        return query_str

    def add_date_filter(self, tag: str = None,
                        date: tuple = (None, None)):
        """
        Add a filter on a date product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "ContentDate/Start".
        date : tuple = (None, None)
            a tuple of datetime or str indicating
            the starting date (first) and ending date (last) for the request
            if the date if provided as a str the expected format is
            yyyy-MM-ddThh:mm:ss.0Z
        """
        newfilter = []

        if date[0] is not None:
            q = self._build_cmp_filter(tag, date[0], "TO *")
            newfilter.append(q)
        if date[1] is not None:
            q = self._build_cmp_filter(tag, date[1], "* TO")
            newfilter.append(q)

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter

    def add_geometry_filter(self,
                            geometry: Union[tuple, str] = ()):
        """
        Add a filter to select only product having a footprint that intersects
        the wanted Region of Interest

        Parameters
        ----------
        geometry : Union[tuple, str]
            Can be a path to the geojson file containing a footprint
            or a series of coordinate containing in a tuple separated
            by a coma. default ()
        """

        # specify geographic area
        newfilter = []

        if len(geometry) == 0:
            return newfilter

        geo = []
        if len(geometry) == 1 or isinstance(geometry, str):
            if os.path.exists(geometry[0]):
                with open(geometry[0]) as f:
                    geo = json.load(f)
            elif os.path.exists(geometry):
                with open(geometry) as f:
                    geo = json.load(f)
            geo = footprint_extract(geo)
        else:

            if isinstance(geometry[0], str):
                for e in geometry:
                    geo.append((
                        float(e.split(',')[0]),
                        float(e.split(',')[1])))
            else:
                for e in geometry:
                    geo.append((float(e[0]), float(e[1])))

        if len(geo) > 0:
            spointlist = [f"{point[0]} {point[1]}" for point in geo]
            sallpoint = ",".join(spointlist)
            filterby_geographicArea = \
                f'footprint:"Intersects(POLYGON(({sallpoint})))"'
            newfilter.append(filterby_geographicArea)

        if len(newfilter) > 0:
            self._filter_list.extend(newfilter)

        return newfilter

    def add_numerical_filter(self, tag: str,
                             valcmp,
                             operator: str
                             ):
        """
        Add a filter on a numerical product metadata

        Parameters
        ----------
        tag : str
            the name of the tag , for example "ContentLength".
        valcmp : int, float, bool
            the numerical value which with th tag content value
            must be compared
        operator : str
            use the buil-in pythonn operator
            "<", "=<", "!=", "==", ">", ">="
            or
            "lt", "le", "ne", "eq", "gt", "ge"

        """
        newfilter = []

        odata_operator = ""
        # for all type
        if operator == "!=" or operator == "ne":
            odata_operator = ""
        if operator == "==" or operator == "eq":
            odata_operator = f"{valcmp}"

        # for numerical field
        if isinstance(valcmp, float) or isinstance(valcmp, int):
            dec = 1
            if isinstance(valcmp, float):
                dec = 0.000001
            if operator == "<" or operator == "lt":
                val = valcmp - dec
                odata_operator = f"[* TO {val}]"
            if operator == "=<" or operator == "le":
                odata_operator = f"[* TO {valcmp}]"

            if operator == ">" or operator == "gt":
                val = valcmp + dec
                odata_operator = f"[{val} TO *]"
            if operator == ">=" or operator == "ge":
                odata_operator = f"[{valcmp} TO *]"

        if odata_operator != 'None':
            newfilter = [f"{tag}:{odata_operator}"]

            self._filter_list.extend(newfilter)

        return newfilter

    def add_attribute_parameters(self,
                                 attribute_name: str,
                                 attribute_valcmp,
                                 operator: str = "=="):
        """
        Add a filter to select a product having a attribute value that fit the
        requirements

        Parameters
        ----------
        attribute_name : str
            the name of the attribute
        valcmp :
            the value to compare
        operator : str
            "<", "=<", "!=", "==", ">", ">="
        """

        return self.add_numerical_filter(attribute_name,
                                         attribute_valcmp,
                                         operator)

    def add_product_online_filter(self, valcmp, operator: str):
        """
        Filter product depending on the Online parameters value

        Parameters
        ----------
        valcmp : int, float, bool
            the numerical value which with th tag content value
            must be compared
        operator : str
            use the buil-in pythonn operator
           "!=", "=="
            or
            "ne", "eq"
        """
        return self.add_numerical_filter(
            self.tag_product_online, valcmp, operator)
