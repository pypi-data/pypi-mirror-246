from unittest import TestCase
from ..plugin_spec import KomandPluginSpec


class TestKomandPluginSpec(TestCase):
    def setUp(self) -> None:
        self.normal_spec = KomandPluginSpec(directory="icon_plugin_spec/tests/resources",
                                            spec_file_name="normal_plugin.spec.yaml")
        self.obsolete_spec = KomandPluginSpec(directory="icon_plugin_spec/tests/resources",
                                              spec_file_name="obsolete_plugin.spec.yaml")
        self.cloud_ready_spec = KomandPluginSpec(directory="icon_plugin_spec/tests/resources",
                                                 spec_file_name="cloud_ready_plugin.spec.yaml")

    def test_is_plugin_obsolete_false(self):
        is_obsolete = self.normal_spec.is_plugin_obsolete()
        self.assertFalse(is_obsolete)

    def test_is_plugin_obsolete_true(self):
        is_obsolete = self.obsolete_spec.is_plugin_obsolete()
        self.assertTrue(is_obsolete)

    def test_is_plugin_cloud_ready_false(self):
        cloud_ready = self.normal_spec.is_cloud_ready()
        self.assertFalse(cloud_ready)

    def test_is_plugin_cloud_ready_true(self):
        cloud_ready = self.cloud_ready_spec.is_cloud_ready()
        self.assertTrue(cloud_ready)

    def test_get_normal_plugin_plugin_version(self):
        got = self.normal_spec.plugin_version()
        want = "1.1.2"
        self.assertEqual(got, want)

    def test_get_normal_plugin_plugin_name(self):
        got = self.normal_spec.plugin_name()
        want = "base64"
        self.assertEqual(got, want)

    def test_get_normal_plugin_plugin_vendor(self):
        got = self.normal_spec.plugin_vendor()
        want = "rapid7"
        self.assertEqual(got, want)

    def test_get_normal_spec_dictionary(self):
        want = {'plugin_spec_version': 'v2', 'extension': 'plugin', 'products': ['insightconnect'], 'name': 'base64', 'title': 'Base64', 'description': 'Encode and decode data using the base64 alphabet', 'version': '1.1.2', 'vendor': 'rapid7', 'support': 'community', 'status': [], 'resources': {'source_url': 'https://github.com/rapid7/insightconnect-plugins/tree/master/base64', 'license_url': 'https://github.com/rapid7/insightconnect-plugins/blob/master/LICENSE'}, 'tags': ['base64', 'encoder', 'decoder', 'utilities'], 'hub_tags': {'use_cases': ['data_utility'], 'keywords': ['base64', 'encoder', 'decoder', 'utilities'], 'features': []}, 'actions': {'encode': {'title': 'Encoder', 'description': 'Encode data to Base64', 'input': {'content': {'type': 'string', 'description': 'Data to encode', 'required': True}}, 'output': {'data': {'title': 'Encoded Data', 'description': 'Encoded data result', 'type': 'bytes', 'required': True}}}, 'decode': {'title': 'Decoder', 'description': 'Decode Base64 to data', 'input': {'base64': {'type': 'bytes', 'description': 'Data to decode', 'required': True}, 'errors': {'type': 'string', 'description': 'How errors should be handled when decoding Base64', 'default': 'nothing', 'enum': ['replace', 'ignore', 'nothing'], 'required': False}}, 'output': {'data': {'title': 'Decoded Data', 'description': 'Decoded data result', 'type': 'string', 'required': True}}}}}
        got = self.normal_spec.spec_dictionary()
        self.assertEqual(got, want)

    def test_get_normal_spec_market_json(self):
        want = {'spec': 'plugin_spec_version: v2\nextension: plugin\nproducts: [insightconnect]\nname: base64\ntitle: Base64\ndescription: Encode and decode data using the base64 alphabet\nversion: 1.1.2\nvendor: rapid7\nsupport: community\nstatus: []\nresources:\n  source_url: https://github.com/rapid7/insightconnect-plugins/tree/master/base64\n  license_url: https://github.com/rapid7/insightconnect-plugins/blob/master/LICENSE\ntags:\n- base64\n- encoder\n- decoder\n- utilities\nhub_tags:\n  use_cases: [data_utility]\n  keywords: [base64, encoder, decoder, utilities]\n  features: []\nactions:\n  encode:\n    title: Encoder\n    description: Encode data to Base64\n    input:\n      content:\n        type: string\n        description: Data to encode\n        required: true\n    output:\n      data:\n        title: Encoded Data\n        description: Encoded data result\n        type: bytes\n        required: true\n  decode:\n    title: Decoder\n    description: Decode Base64 to data\n    input:\n      base64:\n        type: bytes\n        description: Data to decode\n        required: true\n      errors:\n        type: string\n        description: How errors should be handled when decoding Base64\n        default: nothing\n        enum:\n        - replace\n        - ignore\n        - nothing\n        required: false\n    output:\n      data:\n        title: Decoded Data\n        description: Decoded data result\n        type: string\n        required: true\n'}
        got = self.normal_spec.market_json()
        self.assertEqual(want, got)

