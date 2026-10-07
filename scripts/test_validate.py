import json
import unittest
from validate import CANONICAL, validate

class PublicBoundary(unittest.TestCase):
    def setUp(self):
        self.settings = {"config/import-settings-url": CANONICAL, "config/source-ip-label-list": "[]"}

    def test_public_settings(self):
        validate(self.settings)
        validate({**self.settings, "config/icon": "https://zzpice.github.io/assets/icons/example.png"})

    def test_rejects_device_labels_even_without_an_ip(self):
        with self.assertRaisesRegex(ValueError, "device-map"):
            validate({**self.settings, "config/source-ip-label-list": '[{"label":"example-device"}]'})

    def test_rejects_sensitive_data_inside_exported_json_strings(self):
        for value in [
            {"apiToken":"example"}, {"url":"https://example.invalid/?client=192.168.1.2"},
            {"url":"http://example-device.local/"}, {"url":"http://[fd12::1]/"},
            {"url":"https://example:password@example.invalid/"}, {"url":"vless://example"},
            {"path":"/Users/example/private"},
        ]:
            with self.subTest(kind=next(iter(value))):
                with self.assertRaises(ValueError):
                    validate({**self.settings, "config/custom":json.dumps(value)})

    def test_import_source_must_be_exact(self):
        with self.assertRaisesRegex(ValueError, "canonical-import"):
            validate({**self.settings, "config/import-settings-url":"https://example.invalid/settings.json"})

if __name__ == "__main__":
    unittest.main()
