import io
import unittest
import uuid
import re

import drb.drivers.tar
from drb.exceptions.core import DrbException

from drb.drivers.odata import ODataServiceNodeCSC, \
    ODataServiceType, ODataProductNode, ODataServiceNodeList, \
    ODataQueryPredicate, QueryFilter_CSC, ProductCollection
from tests.utils import start_mock_odata_csc, stop_mock_odata_csc


class TestODataServiceNode(unittest.TestCase):
    geo_path = 'tests/resources/geo.json'
    svc_url = 'https://gael-systems.com/odata/csc'
    node = None
    builder = None

    @classmethod
    def setUpClass(cls) -> None:
        start_mock_odata_csc(cls.svc_url)
        cls.node = ODataServiceNodeCSC(cls.svc_url)
        cls.builder = cls.node.get_filterquery_builder()

    @classmethod
    def tearDownClass(cls) -> None:
        stop_mock_odata_csc()

    def test_type_service(self):
        self.assertEqual(ODataServiceType(1), self.node.type_service)
        self.node._type = None
        self.assertEqual(ODataServiceType(1), self.node.type_service)

    def test_name(self):
        self.assertEqual(self.svc_url, self.node.name)

    def test_namespace_uri(self):
        self.assertEqual('OData.CSC', self.node.namespace_uri)

    def test_value(self):
        self.assertIsNone(self.node.value)

    def test_path(self):
        self.assertEqual(self.svc_url, self.node.path.name)

    def test_parent(self):
        self.assertIsNone(self.node.parent)

    def test_attributes(self):
        self.assertEqual({}, self.node.attributes)

    def test_children(self):
        expected = [
            ODataProductNode(
                self.svc_url, '0723d9a4-3bbe-305e-b712-5e820058e065'),
            ODataProductNode(
                self.svc_url, '0723d9bf-02a2-3e99-b1b3-f6d81de84b62'),
            ODataProductNode(
                self.svc_url, '0723ddbc-b0e7-4702-abeb-de257b9f4094'),
        ]
        children = self.node.children
        self.assertIsNotNone(children)
        self.assertIsInstance(children, list)
        self.assertEqual(expected[1], children[1].get_impl(ODataProductNode))
        self.assertEqual(expected[-1], children[-2].get_impl(ODataProductNode))

        self.assertIsInstance(children[:2], ODataServiceNodeList)

        itr = iter(children)
        self.assertEqual(expected[0], next(itr).get_impl(ODataProductNode))
        self.assertEqual(expected[1], next(itr).get_impl(ODataProductNode))
        self.assertEqual(expected[2], next(itr).get_impl(ODataProductNode))

    def test_len(self):
        self.assertEqual(3, len(self.node))

    def test_get_attribute(self):
        with self.assertRaises(DrbException):
            att = self.node.get_attribute('foo')

    def test_has_impl(self):
        self.assertFalse(self.node.has_impl(io.BytesIO))

    def test_has_child(self):
        self.assertFalse(self.node.has_child('Banana'))
        self.assertTrue(self.node.has_child(
            'S2B_OPER_MSI_L0__GR_EPAE_20180703T214414_S201807'
            '03T165907_D05_N02.06.tar'
        ))
        self.assertFalse(self.node.has_child(
            'S2B_OPER_MSI_L0__GR_EPAE_20180703T214414_S2'
            '0180703T165907_D05_N02.06.tar',
            'Test'))

    def test_hash(self):
        self.assertEqual(hash(self.svc_url),
                         self.node.__hash__())

    def test_bracket_browse(self):
        prd2 = {
            'uuid': '0723d9bf-02a2-3e99-b1b3-f6d81de84b62',
            'name': 'S2B_OPER_MSI_L0__GR_EPAE_20180703T214414_S20180703T165907'
                    '_D05_N02.06.tar',
        }

        # FIXME: odata.children[0] represents a Tar data and view as a TarNode
        #        due to the children auto resolution. The received TarBaseNode
        #        not really wrap its base node. So we change expected attribute
        self.assertIsInstance(self.node[1], drb.drivers.tar.DrbBaseTarNode)
        self.assertEqual(self.node[1].name, prd2['name'])
        self.assertIsInstance(self.node[-3], drb.drivers.tar.DrbBaseTarNode)
        self.assertEqual(self.node[-3].name, prd2['name'])
        with self.assertRaises(IndexError):
            n = self.node[42]

        # tuple(str, str, int) -> by Name
        actual_node = self.node[prd2['name'], None, 0]
        self.assertEqual(actual_node.name, prd2['name'])
        actual_node = self.node[prd2['name'], 0]
        self.assertEqual(actual_node.name, prd2['name'])
        actual_node = self.node[prd2['name']]
        self.assertEqual(actual_node.name, prd2['name'])

        n = self.node[ODataQueryPredicate(filter=f"Name eq '{prd2['name']}'")]
        self.assertIsInstance(n, list)
        self.assertEqual(1, len(n))
        self.assertEqual(prd2['name'], n[0].name)

        with self.assertRaises(KeyError):
            n = self.node['test']
        with self.assertRaises(KeyError):
            n = self.node['test', 1]
        with self.assertRaises(KeyError):
            n = self.node[prd2['name'], 'ns']
        with self.assertRaises(KeyError):
            n = self.node[prd2['name'], 'ns', 1]

        # UUID -> by Id
        self.assertEqual(prd2['name'], self.node[uuid.UUID(prd2['uuid'])].name)
        with self.assertRaises(KeyError):
            fake_uuid = prd2['uuid'][:-2] + 'f'
            n = self.node[fake_uuid]

        with self.assertRaises(TypeError):
            n = self.node[b"helloWorld"]

    def test_equals(self):
        self.assertEqual(self.node, ODataServiceNodeCSC(self.svc_url))

    def test_prepare_filter(self):
        pat = r"\d{4}-\d{2}-\d{2}\w{3}\W\w{2}\W\w{3}"

        self.assertTrue(re.search(pat,
                                  self.node.prepare_filter(None)))
        self.assertIn('PublicationDate', self.node.prepare_filter(None))
        self.assertEqual('PublicationDate',
                         self.node.prepare_filter('PublicationDate'))
        self.assertIn('foo', self.node.prepare_filter('foo'))

    def test_query_builder_tag(self):
        self.builder.clear_filter()
        self.assertIsInstance(self.builder, QueryFilter_CSC)

        self.assertEqual(
            self.builder.tag_product_name,
            'Name'
        )
        self.assertEqual(
            self.builder.tag_cloud_attribute,
            'cloudCover'
        )
        self.assertEqual(
            self.builder.tag_product_online,
            'Online'
        )
        self.assertEqual(
            self.builder.tag_product_sensing_date,
            'ContentDate/Start'
        )
        self.assertEqual(
            self.builder.tag_product_type_attribute,
            'productType'
        )
        self.assertEqual(
            self.builder.join_and,
            ' and '
        )
        self.assertEqual(
            self.builder.build_filter().filter,
            ''
        )

        self.builder.add_odata_filter('Toto')

        self.assertEqual(
            self.builder.build_filter().filter,
            'Toto'
        )

        self.builder.clear_filter()

        self.assertEqual(
            self.builder.build_filter().filter,
            ''
        )

    def test_query_builder_string(self):
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, startswith='S2')[0],
            "startswith(Name,'S2')"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, startswith=('S2', 'S1'))[0],
            "(startswith(Name,'S2') or startswith(Name,'S1'))"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, endswith='zip')[0],
            "endswith(Name,'zip')"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, endswith=('zip', 'tar'))[0],
            "(endswith(Name,'zip') or endswith(Name,'tar'))"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, contains='132456')[0],
            "contains(Name,'132456')"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name,
                contains=('132', '456'))[0],
            "(contains(Name,'132') or contains(Name,'456'))"
        )
        self.assertIsInstance(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name,
                startswith='S2',
                endswith='zip',
                contains='123456'),
            list
        )
        self.assertEqual(
            self.builder.add_product_name_filter(startswith='S2')[0],
            "startswith(Name,'S2')"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(startswith=('S2', 'S1'))[0],
            "(startswith(Name,'S2') or startswith(Name,'S1'))"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(endswith='zip')[0],
            "endswith(Name,'zip')"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(endswith=('zip', 'tar'))[0],
            "(endswith(Name,'zip') or endswith(Name,'tar'))"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(contains='132456')[0],
            "contains(Name,'132456')"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(contains=('132', '456'))[0],
            "(contains(Name,'132') or contains(Name,'456'))"
        )
        self.assertIsInstance(
            self.builder.add_product_name_filter(
                startswith='S2',
                endswith='zip',
                contains='123456'),
            list
        )

    def test_query_builder_date(self):
        self.assertEqual(
            self.builder.add_date_filter(
                tag=self.builder.tag_product_sensing_date,
                date=('2023-01-01T01:00:00.0Z', None))[0],
            "ContentDate/Start gt 2023-01-01T01:00:00.0Z"
        )
        with self.assertRaises(ValueError):
            self.builder.add_date_filter(
                tag=self.builder.tag_product_sensing_date, date=('TOTO', None))

        self.assertEqual(
            self.builder.add_date_filter(
                tag=self.builder.tag_product_sensing_date,
                date=(None, '2023-01-02T01:00:00.0Z'))[0],
            "ContentDate/Start lt 2023-01-02T01:00:00.0Z"
        )
        self.assertIsInstance(
            self.builder.add_date_filter(
                tag=self.builder.tag_product_sensing_date,
                date=('2023-01-01T01:00:00.0Z', '2023-01-02T01:00:00.0Z')),
            list
        )
        self.assertEqual(
            self.builder.add_product_sensing_date_filter(
                date=('2023-01-01T01:00:00.0Z', None))[0],
            "ContentDate/Start gt 2023-01-01T01:00:00.0Z"
        )
        with self.assertRaises(ValueError):
            self.builder.add_product_sensing_date_filter(
                date=('TOTO', None))

        self.assertEqual(
            self.builder.add_product_sensing_date_filter(
                date=(None, '2023-01-02T01:00:00.0Z'))[0],
            "ContentDate/Start lt 2023-01-02T01:00:00.0Z"
        )
        self.assertIsInstance(
            self.builder.add_product_sensing_date_filter(
                date=('2023-01-01T01:00:00.0Z',
                      '2023-01-02T01:00:00.0Z')),
            list
        )

    def test_query_builder_product_type(self):
        self.assertEqual(
            self.builder.add_product_collections_filter('S2')[0],
            "startswith(Name,'S2')"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel1)[0],
            "startswith(Name,'S1')"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel2)[0],
            "startswith(Name,'S2')"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel3)[0],
            "startswith(Name,'S3')"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel5p)[0],
            "startswith(Name,'S5P')"
        )
        with self.assertRaises(ValueError):
            self.builder.add_product_collections_filter(1)

    def test_query_builder_geo(self):
        geo_query = "OData.CSC.Intersects(" \
                    "area=geography'SRID=4326;POLYGON(" \
                    "(100.0 0.0,101.0 0.0,101.0 1.0,100.0 1.0,100.0 0.0))')"

        self.assertEqual(
            self.builder.add_geometry_filter(self.geo_path)[0],
            geo_query
        )

    def test_query_builder_numerical(self):
        self.assertEqual(self.builder.add_numerical_filter(
            'ContentLength',
            1000,
            ">"
        ),
            'ContentLength gt 1000'
        )

        self.assertEqual(self.builder.add_numerical_filter(
            'ContentLength',
            1000.0,
            ">"
        ),
            'ContentLength gt 1000.0'
        )

        self.assertEqual(self.builder.add_numerical_filter(
            'Online',
            True,
            "=="
        ),
            'Online eq True'
        )

        self.assertEqual(
            self.builder.add_product_online_filter(
                True,
                '=='
            ),
            self.builder.add_numerical_filter(
                self.builder.tag_product_online,
                True,
                '=='
            )
        )

        self.assertEqual(
            self.builder.add_product_online_filter(
                False,
                '!='
            ),
            self.builder.add_numerical_filter(
                self.builder.tag_product_online,
                False,
                '!='
            )
        )

    def test_query_builder_parameters(self):
        self.assertIsInstance(self.builder, QueryFilter_CSC)
        self.assertEqual(self.builder.add_attribute_parameters(
            'attributes',
            1000,
            "=="
        )[0],
                         "Attributes/OData.CSC.IntegerAttribute/any("
                         "att:att/Name eq 'attributes' and "
                         "att/OData.CSC.IntegerAttribute/Value eq 1000)"
                         )
        self.assertEqual(self.builder.add_attribute_parameters(
            'cover',
            10,
            "<"
        )[0],
                         "Attributes/OData.CSC.IntegerAttribute/any("
                         "att:att/Name eq 'cover' and "
                         "att/OData.CSC.IntegerAttribute/Value lt 10)"
                         )

    def test_query_builder_cloud(self):
        self.assertIsInstance(self.builder, QueryFilter_CSC)
        self.assertEqual(self.builder.add_product_cloud_parameters(
            1000,
            "=="
        )[0],
                         "Attributes/OData.CSC.DoubleAttribute/any("
                         "att:att/Name eq 'cloudCover' and "
                         "att/OData.CSC.DoubleAttribute/Value eq 1000.0)"
                         )
        self.builder.clear_filter()
        self.assertEqual(self.builder.add_product_cloud_parameters(
            10,
            "<"
        )[0],
                         "Attributes/OData.CSC.DoubleAttribute/any("
                         "att:att/Name eq 'cloudCover' and "
                         "att/OData.CSC.DoubleAttribute/Value lt 10.0)"
                         )
