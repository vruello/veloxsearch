This project implements a versatile **prefix-based autocomplete system**. It serves as a practical study and solution, supporting multiple search algorithms to retrieve word suggestions based on a given prefix.

The system is designed to allow easy switching between three core algorithmic backends:

1. **Naive Search (`naive`):** A straightforward linear scan across the entire, unsorted word list, included primarily for **baseline performance measurement**.
2. **Binary Search (`bisect`):** The **recommended default**. This approach uses Python's highly optimized `bisect` module on a pre-sorted word list. Benchmarks demonstrate **superior speed** for in-memory operations across huge datasets in the Python environment.
3. **Prefix Tree (`prefixtree`):** This is the classic implementation using a prefix tree. While theoretically considered the optimal algorithm for prefix search, its practical application in pure Python suffers from slow construction time (building the tree) and significant overhead from Python's dictionary lookups, making it slower than the native bisect approach in my benchmarks.

The project is structured to easily switch between these backends, allowing developers to choose the optimal balance of complexity, memory usage, and execution speed.

## API Endpoint

The autocomplete system is exposed via a simple web server.

### Route

A single endpoint is used to retrieve suggestions based on a query prefix:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/autocomplete` | Retrieves suggestions matching the `query` prefix. |

### Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | Yes | The prefix string to search against (e.g., `po`). |

### Example Request

```bash
GET /autocomplete?query=pom
```

### Example Response

The API returns a JSON array containing the list of suggestions, sorted alphabetically:
```json
[
    "pomme",
    "pommeraie"
]
```

## Configuration

The service is configured via a configuration file in toml format. By default, it tries to read `/etc/veloxsearch.conf.toml`, except if a `--config` argument is given in command line.

A commented example of the configuration structure is provided below:
```toml
[http_server]
# HTTP server listening address
listen_addr = "0.0.0.0"
# HTTP server listening port
listen_port = 10000

[search]
# Wordlist file to load and search into
wordlist = "data/eff_large_wordlist.txt"
# Search algorithm to use. Valid values are:
# - naive: Linear scan, unsorted list (Baseline)
# - bisect: Binary search on a sorted list (Recommended Default)
# - prefixtree: Trie/Prefix Tree structure
algorithm = "bisect"
# Maximum number of words to return in suggestions
limit = 10

[logging]
# Minimum logging level to display. Available values: debug, info, warning, error, critical
level = "debug"
```

## Installation & Usage

### Using Docker

* Build Docker image:
```
$ docker build -t veloxsearch .
```

* Create a config.toml file, with `http_server.listen_addr` set to `0.0.0.0`.

* Run locally:
```
$ docker run --rm -v ./config.toml:/etc/veloxsearch.conf.toml:ro -p 127.0.0.1:10000:10000 veloxsearch
```

### Using pip

#### Prerequisites

* Python 3.13+
* The system uses only Python's standard library.

#### Installation

```
$ pip install .
```

#### Running the Server

```
$ veloxsearch [--config CONFIG]
```

## Tests

Tests can be run using:
```
$ make test
```

## Performance Benchmarks

Empirical testing confirms the efficiency of the `bisect` approach, making it the fastest choice for Python in-memory string search. All tests have been performed on `11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz`.

Benchmark can be run using:
```
$ make bench
```

### Wordlist Load Time

| Dataset Size (N) | `naive` Load Time (Avg. ms) |  `bisect` Load Time (Avg. ms) | `prefixtree` Load Time (Avg. ms) |
| :--- | :--- | :--- | :--- |
| 8,000 words | **0.99** | 2.6 | 10 | 
| 336,530 words | **57** | 94 | 1100 |
| 14,344,392 words | **1602** | 3209 | 70062 |

The `naive` approach is unsurprisingly the best regarding loading time, but `bisect` performs quite reasonnably. However, `prefixtree` performs very bad when loading huge wordlists.

### Prefix Completion Time

| Dataset Size (N) | `naive` Completion Time (Avg. ms) |  `bisect` Completion Time (Avg. ms) | `prefixtree` Completion Time (Avg. ms) |
| :--- | :--- | :--- | :--- |
| 8,000 words | 0.169 | **0.003** | 0.016 | 
| 336,530 words | 9.18 | **0.0079** | 0.0097 |
| 14,344,392 words | 425 | **0.012** | 0.028 |

As expected, the `naive` approach performs quite bad, even on small datasets. However, the `bisect` algorithm performs surprisingly well and even outperforms `prefixtree`, which is supposed to be one of the most optmized method to do prefix completion. This may be due to the speed of the C-implemented binary search (`bisect`) which outperforms the cumulative overhead of dictionnary lookups and recursion inherent to the pure Python prefix tree implementation.

