# IOT Device Backbone - Client (Python)

## Getting Started

```command
pip install iot-device-backbone-client
```

## Usage

```python
from iot_device_backbone_client.client import IotDeviceBackboneClient
import asyncio

# Replace with your connection string
connection_string = "http://clq2kqjsy0jgqvvlq7tm1mlyt:e3c2216a-cfff-4924-8420-2c65dd2c5d58@localhost:4900/"

# Create a client to connect to the backbone
client = IotDeviceBackboneClient(
    f"{connection_string}graphql",
    {
        # Required for ensuring we bypass the CSRF protection from the backbone
        "Apollo-Require-Preflight": "1"
    },
)
```

For a full example, see the `example` directory.

## Development

Generate the client by running:

```
ariadne-codegen
```

Install dependencies:

```
pip install -r requirements.txt
```

Install locally:

```command
python -m pip install -e .
```

See `example` directoy for a complete. You can run them with:

```command
python -m example.main
```

## Publishing

```command
python -m pip install build twine

python -m build

twine check dist/*

twine upload dist/*
```
