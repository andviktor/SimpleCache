# A Simple Data Caching Module with Cache Lifetime Control

This module stores data in a hash table format with a controlled cache lifetime. It includes good coverage with Pytest tests.

## Installation

1. Clone this repository to your working directory.
2. Create a virtual environment with the command: `python -m venv venv`
3. Activate your virtual environment with the command: `source ./venv/bin/activate`
4. Install dependencies with the command: `pip install -r requirements.txt`

## Usage

You can import the `Cache` class into your project using the following command: `from cache import Cache`.

Create a new cache object with the following syntax: `cache = Cache(ttl=3600, clean_timeout=60)`

- **`ttl`**: Time to live for the cache in seconds (optional, default is 3600 s)
- **`clean_timeout`**: Cache will be automatically cleared every N seconds (optional, default is 60 s)

You can work with the cache as if it were a dictionary:
- get data: **cache[key]**
- set data: **cache[key] = value**

### Methods

1. `cache.print()`: Prints values from the cache to the console.
2. `cache.size()`: Returns the number of elements in the cache at the moment.

## Testing

There are two ways to test:

1. Run a simple self-test in the console with the command: `python cache.py`
2. Run Pytest tests with the command: `pytest tests.py`
