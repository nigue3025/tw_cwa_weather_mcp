"""Validate server.json against MCP schema"""
import json
import requests
from jsonschema import validate, ValidationError, SchemaError

# Load the server.json
with open('server.json', 'r', encoding='utf-8') as f:
    server_data = json.load(f)

# Fetch the schema
schema_url = server_data.get('$schema')
if not schema_url:
    print("❌ Error: No $schema field found in server.json")
    exit(1)

print(f"📥 Fetching schema from: {schema_url}")
response = requests.get(schema_url)
response.raise_for_status()
schema = response.json()

# Validate
try:
    validate(instance=server_data, schema=schema)
    print("✅ server.json is valid according to the MCP schema!")
    print(f"   Server name: {server_data['name']}")
    print(f"   Title: {server_data['title']}")
    print(f"   Version: {server_data['version']}")
    if 'packages' in server_data:
        print(f"   Package type: {server_data['packages'][0]['registryType']}")
        print(f"   Package identifier: {server_data['packages'][0]['identifier']}")
except ValidationError as e:
    print(f"❌ Validation error: {e.message}")
    print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
    exit(1)
except SchemaError as e:
    print(f"❌ Schema error: {e.message}")
    exit(1)
