"""Validate public UI settings without printing settings or personal values."""
import ipaddress
import json
import re
from urllib.parse import urlsplit, unquote
from pathlib import Path

CANONICAL = "https://raw.githubusercontent.com/zzpice/zashboard-config/main/zashboard-settings.json"
SENSITIVE = ("password", "passwd", "secret", "token", "private_key", "private-key", "api_key", "api-key", "apikey", "authorization", "credential", "cookie", "subscription")
NODE = re.compile(r"(?i)(?:ss|ssr|vmess|vless|trojan|hysteria2?|tuic|ssh)://")
AUTH = re.compile(r"(?i)https?://[^/\s:@]+:[^@\s/]+@")
IP = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
PRIVATE_V6 = re.compile(r"(?i)(?:\[|^|\s)((?:f[cd][0-9a-f]{2}|fe[89ab][0-9a-f]):[0-9a-f:]+|::1)(?:\]|$|\s)")
LOCAL_PATH = re.compile(r"(?i)(?:/Users/|/home/|[a-z]:\\Users\\)")

def validate(data):
    if not isinstance(data, dict):
        raise ValueError("structure")
    if data.get("config/import-settings-url") != CANONICAL:
        raise ValueError("canonical-import")
    labels = data.get("config/source-ip-label-list", "[]")
    if isinstance(labels, str):
        try:
            labels = json.loads(labels)
        except json.JSONDecodeError:
            raise ValueError("device-map") from None
    if labels != []:
        raise ValueError("device-map")

    def walk(value, depth=0):
        if depth > 32:
            raise ValueError("nested-depth")
        if isinstance(value, dict):
            for key, item in value.items():
                if any(term in str(key).lower() for term in SENSITIVE) and item not in (None, "", [], {}):
                    raise ValueError("credential-field")
                walk(item, depth+1)
        elif isinstance(value, list):
            for item in value:
                walk(item, depth+1)
        elif isinstance(value, str):
            decoded = unquote(value)
            for match in re.finditer(r"(?i)https?://[^\s\"'<>]+", decoded):
                try:
                    url = urlsplit(match.group())
                    if url.username is not None or url.password is not None:
                        raise ValueError("credential-value")
                    hostname = url.hostname or ""
                    if hostname.lower() in {"localhost"} or hostname.lower().endswith((".local", ".lan", ".internal", ".home")):
                        raise ValueError("private-host")
                    try:
                        ipaddress.ip_address(hostname)
                    except ValueError:
                        pass
                    else:
                        raise ValueError("network-address")
                except ValueError as error:
                    if str(error) in {"credential-value", "private-host", "network-address"}: raise
                    raise ValueError("invalid-url") from None
            if NODE.search(decoded) or AUTH.search(decoded) or "-----BEGIN " in decoded:
                raise ValueError("credential-value")
            if LOCAL_PATH.search(decoded) or PRIVATE_V6.search(decoded):
                raise ValueError("private-address")
            for address in IP.findall(decoded):
                try:
                    ip = ipaddress.ip_address(address)
                except ValueError:
                    continue
                raise ValueError("network-address")
            if re.search(r"(?i)(?:https?://)?[a-z0-9.-]+\.(?:local|lan|internal|home)(?=[:/\s\"']|$)", decoded):
                raise ValueError("private-host")
            if value.strip().startswith(("{", "[")):
                try:
                    nested = json.loads(value)
                except json.JSONDecodeError:
                    return
                walk(nested, depth+1)
    walk(data)

if __name__ == "__main__":
    try:
        validate(json.loads(Path("zashboard-settings.json").read_text()))
    except (ValueError, OSError):
        raise SystemExit("Public settings validation failed; inspect locally (values withheld).")
    print("Public settings: OK")
