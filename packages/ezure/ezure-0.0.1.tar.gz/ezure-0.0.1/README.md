## Overview

ezure (Easy Azure) is a Python package that serves as a comprehensive wrapper for Azure utilities. It simplifies and streamlines interactions with various Azure services, providing easy-to-use functions for downloading and uploading blobs, managing tables, handling queues, and more.

## Features

- **Blob Management**: Easily download and upload blobs to your Azure storage account.
- **Table Management**: Efficiently manage your Azure tables.
- **Queue Management**: Simplify interactions with Azure queues.
- **Azure Key Vault Utility**: Simplify interactions with Azure Keys.


## Installation

You can install ezure using pip:

```bash
pip install ezure
```

## Usage

Here's a simple example of how to use ezure:

```python
import ezure

# Initialize the ezure client
ez = ezure.Client()

ez.connection_string = 'connection_string'

# Download a blob
ez.download_blob('your-container-name', 'your-blob-name', 'output-file-path')

# Upload a blob
ez.upload_blob('your-container-name', 'your-blob-name','input-file-path')
```

## Contributing

We welcome contributions!
