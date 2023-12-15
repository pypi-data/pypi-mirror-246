import unittest
import unittest.mock as mocking
import uuid

from drb.drivers.odata import (
    ODataServiceNodeDias, ODataServiceType,
    ODataProductNode, ODataServiceNodeList,
    QueryFilter_Dias, ProductCollection)
from drb.drivers.odata.odata_utils import ODataUtils, ODataQueryPredicate
from tests.utils import start_mock_odata_dias, \
    stop_mock_odata_csc, dias_products


class TestODataDiasServiceNode(unittest.TestCase):
    geo_path = 'tests/resources/geo.json'
    svc_url = 'https://gael-systems.com/odata/dias'
    builder = None
    node = None

    @classmethod
    def setUpClass(cls) -> None:
        start_mock_odata_dias(cls.svc_url)
        cls.node = ODataServiceNodeDias(cls.svc_url)
        cls.node._type = ODataServiceType.ONDA_DIAS
        cls.builder = cls.node.get_filterquery_builder()

    @classmethod
    def tearDownClass(cls) -> None:
        stop_mock_odata_csc()
        cls.node._type = ODataServiceType.CSC

    def test_name(self):
        self.assertEqual(self.svc_url, self.node.name)

    def test_namespace_uri(self):
        self.assertEqual('Ens', self.node.namespace_uri)

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
                self.svc_url, 'da4cdfee-9fef-4ab1-b4a2-20f9ec8005bd'),
            ODataProductNode(
                self.svc_url, '34416861-c364-44be-8bc9-16829f32cf31'),
            ODataProductNode(
                self.svc_url, 'c3f89d3d-3a06-4e42-9903-a5d07ab5c642')
        ]
        with mocking.patch.object(ODataUtils, 'req_svc_products',
                                  return_value=(dias_products, -1)):
            children = self.node.children
            self.assertIsNotNone(children)
            self.assertIsInstance(children, list)
            self.assertEqual(expected[1],
                             children[1].get_impl(ODataProductNode))
            self.assertEqual(expected[-1],
                             children[-1].get_impl(ODataProductNode))
            self.assertIsInstance(children[:2], ODataServiceNodeList)
            self.assertIsInstance(children[1:-1], ODataServiceNodeList)

        with mocking.patch.object(ODataUtils, 'req_svc_products',
                                  return_value=dias_products):
            itr = iter(children)
            self.assertEqual(expected[0], next(itr).get_impl(ODataProductNode))
            self.assertEqual(expected[1], next(itr).get_impl(ODataProductNode))
            self.assertEqual(expected[2], next(itr).get_impl(ODataProductNode))

    def test_len(self):
        self.assertEqual(3, len(self.node))

    def test_bracket_browse(self):
        prd2 = {
            'uuid': '34416861-c364-44be-8bc9-16829f32cf31',
            'name': 'S2B_MSIL2A_20180328T120349_N0207_R066_'
                    'T29VLD_20180328T175102.zip'
        }

        # int
        with mocking.patch.object(ODataUtils, 'req_svc_products',
                                  return_value=(dias_products, -1)):
            node = self.node[1]
            self.assertEqual(prd2['uuid'], node.get_attribute('id'))
            node = self.node[-2].get_impl(ODataProductNode)
            self.assertEqual(prd2['uuid'], node.get_attribute('id'))
            with self.assertRaises(IndexError):
                n = self.node[42]

        # # tuple(str, str, int) -> by Name
        actual_node = self.node[prd2['name']].get_impl(ODataProductNode)
        self.assertEqual(prd2['uuid'], actual_node.get_attribute('id'))
        self.assertEqual(prd2['uuid'], actual_node @ 'id')

        n = self.node[ODataQueryPredicate(filter=f"Name eq '{prd2['name']}'")]
        self.assertIsInstance(n, list)
        self.assertEqual(3, len(n))

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
        self.assertEqual(self.node, ODataServiceNodeDias(self.svc_url))

    def test_prepare_filter(self):
        result = '%22creationDate:[1900-05-10T00:00:00.000Z TO NOW]%22'
        self.assertEqual(result, self.node.prepare_filter(None))

    def test_query_builder_tag(self):
        self.builder.clear_filter()
        self.assertIsInstance(self.builder, QueryFilter_Dias)

        self.assertEqual(
            self.builder.tag_product_name,
            'name'
        )
        self.assertEqual(
            self.builder.tag_cloud_attribute,
            'cloudCoverPercentage'
        )
        self.assertEqual(
            self.builder.tag_product_online,
            'Offline'
        )
        self.assertEqual(
            self.builder.tag_product_sensing_date,
            'beginPosition'
        )
        self.assertEqual(
            self.builder.tag_product_type_attribute,
            'productType'
        )
        self.assertEqual(
            self.builder.join_and,
            ' AND '
        )
        self.assertEqual(
            self.builder.build_filter().filter,
            '""'
        )

        self.builder.add_odata_filter('Toto')

        self.assertEqual(
            self.builder.build_filter().filter,
            '"Toto"'
        )

        self.builder.clear_filter()

        self.assertEqual(
            self.builder.build_filter().filter,
            '""'
        )

    def test_query_builder_string(self):
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, startswith='S2')[0],
            "name:S2*"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, startswith=('S2', 'S1'))[0],
            "(name:S2* OR name:S1*)"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, endswith='zip')[0],
            "name:*zip"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, endswith=('zip', 'tar'))[0],
            "(name:*zip OR name:*tar)"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name, contains='132456')[0],
            "name:*132456*"
        )
        self.assertEqual(
            self.builder.add_string_filter(
                tag=self.builder.tag_product_name,
                contains=('132', '456'))[0],
            "(name:*132* OR name:*456*)"
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
            "name:S2*"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(startswith=('S2', 'S1'))[0],
            "(name:S2* OR name:S1*)"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(endswith='zip')[0],
            "name:*zip"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(endswith=('zip', 'tar'))[0],
            "(name:*zip OR name:*tar)"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(contains='132456')[0],
            "name:*132456*"
        )
        self.assertEqual(
            self.builder.add_product_name_filter(contains=('132', '456'))[0],
            "(name:*132* OR name:*456*)"
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
            "beginPosition:[2023-01-01T01:00:00.0Z TO *]"
        )

        with self.assertRaises(ValueError):
            self.builder.add_date_filter(
                tag=self.builder.tag_product_sensing_date, date=('TOTO', None))

        self.assertEqual(
            self.builder.add_date_filter(
                tag=self.builder.tag_product_sensing_date,
                date=(None, '2023-01-02T01:00:00.0Z'))[0],
            "beginPosition:[* TO 2023-01-02T01:00:00.0Z]"
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
            "beginPosition:[2023-01-01T01:00:00.0Z TO *]"
        )
        with self.assertRaises(ValueError):
            self.builder.add_product_sensing_date_filter(
                date=('TOTO', None))

        self.assertEqual(
            self.builder.add_product_sensing_date_filter(
                date=(None, '2023-01-02T01:00:00.0Z'))[0],
            "beginPosition:[* TO 2023-01-02T01:00:00.0Z]"
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
            "name:S2*"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel1)[0],
            "name:S1*"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel2)[0],
            "name:S2*"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel3)[0],
            "name:S3*"
        )
        self.assertEqual(
            self.builder.add_product_collections_filter(
                ProductCollection.Sentinel5p)[0],
            "name:S5P*"
        )
        with self.assertRaises(ValueError):
            self.builder.add_product_collections_filter(1)

    def test_query_builder_geo(self):
        geo_query = ("footprint:\"Intersects(POLYGON(("
                     "100.0 0.0,101.0 0.0,101.0 1.0,100.0 1.0,100.0 0.0)))\"")

        self.assertEqual(
            self.builder.add_geometry_filter(self.geo_path)[0],
            geo_query
        )

    def test_query_builder_numerical(self):
        self.assertEqual(self.builder.add_numerical_filter(
            'ContentLength',
            1000,
            ">"
        )[0],
                         'ContentLength:[1001 TO *]'
                         )

        self.assertEqual(self.builder.add_numerical_filter(
            'ContentLength',
            1000.0,
            ">"
        )[0],
                         'ContentLength:[1000.000001 TO *]'
                         )

        self.assertEqual(self.builder.add_numerical_filter(
            'Online',
            True,
            "=="
        )[0],
                         'Online:True'
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
        self.assertIsInstance(self.builder, QueryFilter_Dias)
        self.assertEqual(self.builder.add_attribute_parameters(
            'attributes',
            1000,
            "=="
        )[0],
                         "attributes:1000"
                         )
        self.assertEqual(self.builder.add_attribute_parameters(
            'cover',
            10,
            "<"
        )[0],
                         "cover:[* TO 9]"
                         )

    def test_query_builder_cloud(self):
        self.assertIsInstance(self.builder, QueryFilter_Dias)
        self.assertEqual(self.builder.add_product_cloud_parameters(
            1000,
            "=="
        )[0],
                         "cloudCoverPercentage:1000.0"
                         )
        self.builder.clear_filter()
        self.assertEqual(self.builder.add_product_cloud_parameters(
            10,
            "<"
        )[0],
                         "cloudCoverPercentage:[* TO 9.999999]"
                         )
