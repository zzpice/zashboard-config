import json
import unittest
from validate import CANONICAL, validate

class PublicBoundary(unittest.TestCase):
    def setUp(self):
        self.settings = {"config/import-settings-url": CANONICAL, "config/source-ip-label-list": "[]"}

    def test_public_settings(self):
        validate(self.settings)
        validate({**self.settings, "config/icon": "https://zzpice.github.io/assets/icons/example.png"})
        validate({**self.settings,"config/icon-reflect-list":json.dumps([{"uuid":"example-ui-row","name":"Example","icon":"https://example.invalid/icon.png"}])})

    def test_rejects_device_labels_even_without_an_ip(self):
        with self.assertRaisesRegex(ValueError, "device-map"):
            validate({**self.settings, "config/source-ip-label-list": '[{"label":"example-device"}]'})

    def test_rejects_sensitive_data_inside_exported_json_strings(self):
        for value in [
            {"apiToken":"example"}, {"url":"https://example.invalid/?client=192.168.1.2"},
            {"url":"http://example-device.local/"}, {"url":"http://[fd12::1]/"},
            {"url":"https://example:password@example.invalid/"}, {"url":"vless://example"},
            {"path":"/Users/example/private"},
            {"url":"https://[2001:db8::1]/"}, {"url":"https://203.0.113.1/"},
            {"url":"https://example@service.example/"},
            {"url":"http://localhost/"}, {"url":"https://device.internal/"},
            {"url":"https%3A%2F%2Fexample%3Apassword%40service.example%2F"},
            {"subscription":"synthetic"}, {"cookie":"synthetic"},
            {"address":"192%2E168%2E1%2E2"}, {"path":"%2FUsers%2Fexample%2Fprivate"},
            {"uuid":"synthetic-connection-credential"},
        ]:
            with self.subTest(kind=next(iter(value))):
                with self.assertRaises(ValueError):
                    validate({**self.settings, "config/custom":json.dumps(value)})

    def test_import_source_must_be_exact(self):
        with self.assertRaisesRegex(ValueError, "canonical-import"):
            validate({**self.settings, "config/import-settings-url":"https://example.invalid/settings.json"})

if __name__ == "__main__":
    unittest.main()
