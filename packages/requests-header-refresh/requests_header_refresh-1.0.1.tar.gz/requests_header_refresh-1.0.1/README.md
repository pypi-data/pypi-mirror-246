# requests_header_refresh

## Description

This Python module provides a function to handle HTTP refresh headers in the `requests` library. It parses the refresh header, extracts or infers the refresh time and URL, and makes a subsequent request to the refresh URL if the refresh time is in a valid range. It also supports a refresh timeout to ignore the refresh if the refresh time is greater than the timeout.

## Installation

You can use this module by importing it in your Python script. Make sure to have the `requests-header-refresh` library installed in your environment. If not, you can install it using pip:

```bash
pip install requests-header-refresh
```

You will also need the [requests]('https://pypi.org/project/requests/') library to use this package.

## Usage

First, import the necessary functions and classes:

```python
import requests
from requests_header_refresh import create_hook
```

Then, create a session and a refresh handler with a timeout of 5 seconds:

```python
session = requests.Session()
refresh_hook = create_hook(refresh_timeout=5)
```

Add the handler as a response hook:

```python
session.hooks = {'response': [refresh_hook]}
```

Finally, make a request:

```python
response = session.get(url)
```

In this example, `refresh_hook` will ignore the refresh if the refresh time is greater than 5 seconds. Replace `url` with the actual URL you want to make a request to. Also, adjust the `refresh_timeout` based on your needs.


The hook could also be used for a single request instead of entire session:

```python
response = requests.get(url, hooks={'response': [refresh_hook]})
```

## Contributing

Contributions are welcome.