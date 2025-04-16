# rentry

<a href="https://rentry.co/"><img width="110" height="110" src="https://rentry.co/static/logo-border-fit.png" align="right" alt="rentry.co markdown paste repository"></a>

[Rentry.co](https://rentry.co) is a markdown-powered paste/publishing service with preview, custom URLs and editing. 

This package provides a Python client for the Rentry.co API, enabling programmatic creation, editing, and deletion of Rentry entries.

> **Note:** This is a fork of the original Rentry project, created to provide a modern, pip-installable package since the official "rentry" package on PyPI hasn't been updated in over 6 years and is inactive. This repository makes it easy to install and use the latest version of the Rentry client directly from GitHub.

## Installation

```sh
pip install git+https://github.com/spignelon/rentry.git
```

This makes the package easily installable while avoiding the outdated version on PyPI.

## Command-line Usage

Once installed, the `rentry` command will be available in your terminal:

```console
$ rentry --help

Usage: rentry {new | edit | raw | fetch | delete} [options] [text]

Commands:
  new     create a new entry
  edit    edit an existing entry
  raw     get raw markdown text of an existing entry
  fetch   fetch details about an entry
  delete  delete an entry
    
Options:
  -h, --help                 show this help message and exit
  -u, --url URL              url for the entry, random if not specified
  -p, --edit-code EDIT-CODE  edit code for the entry, random if not specified
  -m, --metadata METADATA    metadata for the entry (new/edit)
  -a, --auth AUTH            authentication header for raw endpoint
```

### Examples

```sh
# Create a new entry with random URL and edit code
rentry new 'markdown text'

# Create with custom edit code and URL
rentry new -p mypassword -u myurl 'text'

# Edit an existing entry
rentry edit -p mypassword -u myurl 'updated text'

# Add metadata when creating or editing
rentry new -m 'OPTION_DISABLE_VIEWS = true' 'text'

# Read from a file and post
cat README.md | rentry new

# Get raw markdown content
rentry raw -u myurl

# Fetch entry details (requires edit code)
rentry fetch -u myurl -p mypassword

# Delete an entry
rentry delete -u myurl -p mypassword
```

## Python API Usage

You can also use Rentry as a Python library:

```python
import rentry

# Create a new entry
result = rentry.new('My markdown text')
print(f"Created: {result['url']} with edit code: {result['edit_code']}")

# Edit an existing entry
rentry.edit('myurl', 'myeditcode', 'Updated content')

# Get raw content
content = rentry.raw('myurl')

# Fetch entry details
details = rentry.fetch('myurl', 'myeditcode')

# Delete an entry
rentry.delete('myurl', 'myeditcode')

# Using the client class for multiple operations
client = rentry.RentryClient()
result = client.new('My text with custom url', 'customurl', 'myeditcode')
```

### Working with Metadata

Rentry supports metadata to customize the appearance of your entries:

```python
metadata = '''
OPTION_DISABLE_VIEWS = true
CONTAINER_MAX_WIDTH = 600px
CONTENT_TEXT_COLOR = red
'''

# Create with metadata
rentry.new('My text', metadata=metadata)

# Update only specific metadata fields
rentry.edit('myurl', 'myeditcode', 'My text', 
            metadata='CONTENT_FONT_WEIGHT = 600',
            update_mode='upsert')
```

## Configuration

Rentry uses environment variables for configuration. Create a `.env` file in your working directory:

```
BASE_PROTOCOL="https://"
BASE_URL="rentry.co"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
