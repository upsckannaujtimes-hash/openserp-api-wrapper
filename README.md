# OpenSerp API Wrapper

A comprehensive, production-ready wrapper for the **OpenSerp** multi-engine search API. This project provides Python and Go clients with advanced search capabilities, filtering, caching, rate limiting, and comprehensive error handling.

## 🎯 Project Overview

**OpenSerp** is a powerful meta-search engine that aggregates results from multiple search engines (Google, Bing, DuckDuckGo, Yandex, Baidu, etc.). This wrapper simplifies integration and adds enterprise-grade features.

### Key Features

- ✅ **Multi-Engine Search** - Search across all engines simultaneously
- ✅ **Advanced Filtering** - Date range, language, result limits
- ✅ **Client Libraries** - Python (requests/httpx) and Go implementations
- ✅ **Caching Layer** - Redis/in-memory cache support
- ✅ **Rate Limiting** - Built-in request throttling
- ✅ **Error Handling** - Comprehensive exception management
- ✅ **Async Support** - Non-blocking operations (Python)
- ✅ **Docker Support** - Containerized API server
- ✅ **CLI Tools** - Command-line search utility
- ✅ **Comprehensive Tests** - Unit and integration tests
- ✅ **API Documentation** - Swagger/OpenAPI specs

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Advanced Usage](#advanced-usage)
5. [Configuration](#configuration)
6. [Examples](#examples)
7. [Development](#development)
8. [Contributing](#contributing)

---

## 🚀 Installation

### Python Client

```bash
# Clone repository
git clone https://github.com/upsckannaujtimes-hash/openserp-api-wrapper.git
cd openserp-api-wrapper

# Install Python dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Go Client

```bash
# Clone and build
git clone https://github.com/upsckannaujtimes-hash/openserp-api-wrapper.git
cd openserp-api-wrapper

# Build Go binary
go build -o openserp-wrapper ./cmd/cli

# Run the CLI
./openserp-wrapper search "golang" --engines duckduckgo,bing --limit 10
```

---

## ⚡ Quick Start

### Python Example

```python
from openserp_wrapper import OpenSerpClient

# Initialize client
client = OpenSerpClient(base_url="http://localhost:7000")

# Search all engines
results = client.search("golang", limit=10)
print(results)

# Search specific engines
results = client.search(
    text="machine learning",
    engines=["duckduckgo", "bing"],
    limit=15
)

# Advanced filtering
results = client.search(
    text="artificial intelligence",
    engines=["google", "duckduckgo"],
    limit=20,
    date_from="2025-01-01",
    date_to="2025-12-31",
    language="EN"
)
```

### Go Example

```go
package main

import (
    "fmt"
    "log"
    "github.com/upsckannaujtimes-hash/openserp-api-wrapper/pkg/client"
)

func main() {
    // Create client
    c := client.NewClient("http://localhost:7000")
    
    // Search all engines
    results, err := c.Search(context.Background(), &client.SearchRequest{
        Text:  "golang",
        Limit: 10,
    })
    
    if err != nil {
        log.Fatalf("Search error: %v", err)
    }
    
    for _, result := range results.Items {
        fmt.Printf("Title: %s\nURL: %s\n\n", result.Title, result.URL)
    }
}
```

### cURL Examples

```bash
# Search all engines
curl "http://localhost:7000/mega/search?text=golang&limit=10"

# Search specific engines
curl "http://localhost:7000/mega/search?text=golang&engines=duckduckgo,bing&limit=15"

# Advanced filtering with date range
curl "http://localhost:7000/mega/search?text=golang&engines=google,bing&limit=20&date=20250101..20251231&lang=EN"

# Filter by multiple parameters
curl "http://localhost:7000/mega/search?text=python+development&engines=duckduckgo&limit=25&sort=relevance"
```

---

## 📡 API Reference

### Core Endpoints

#### `GET /mega/search`

Search across multiple search engines simultaneously.

**Query Parameters:**
- `text` (required): Search query
- `limit` (optional): Number of results (default: 10, max: 100)
- `engines` (optional): Comma-separated engine list (duckduckgo, bing, google, yandex, baidu)
- `date` (optional): Date range filter (format: YYYYMMDD..YYYYMMDD)
- `lang` (optional): Language filter (EN, ES, FR, DE, etc.)
- `sort` (optional): Sort order (relevance, date)
- `offset` (optional): Result offset for pagination

**Response:**
```json
{
  "query": "golang",
  "total_results": 1500000,
  "search_time_ms": 245,
  "results": [
    {
      "title": "The Go Programming Language",
      "url": "https://golang.org",
      "description": "Go is an open source programming language...",
      "engine": "duckduckgo",
      "rank": 1
    }
  ]
}
```

---

## 🔧 Advanced Usage

### Caching Results

```python
from openserp_wrapper import OpenSerpClient
from openserp_wrapper.cache import RedisCache

# With Redis cache
cache = RedisCache(host="localhost", port=6379)
client = OpenSerpClient(
    base_url="http://localhost:7000",
    cache=cache,
    cache_ttl=3600
)

# Results are automatically cached
results = client.search("python", limit=10)
```

### Rate Limiting

```python
from openserp_wrapper import OpenSerpClient, RateLimiter

# Create rate limiter (5 requests per minute)
rate_limiter = RateLimiter(max_requests=5, window_seconds=60)

client = OpenSerpClient(
    base_url="http://localhost:7000",
    rate_limiter=rate_limiter
)

results = client.search("api", limit=10)
```

### Async Operations

```python
import asyncio
from openserp_wrapper.async_client import AsyncOpenSerpClient

async def search_multiple():
    client = AsyncOpenSerpClient(base_url="http://localhost:7000")
    
    tasks = [
        client.search("golang"),
        client.search("python"),
        client.search("rust")
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# Run async operations
results = asyncio.run(search_multiple())
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# OpenSerp server configuration
OPENSERP_HOST=localhost
OPENSERP_PORT=7000
OPENSERP_TIMEOUT=30

# Cache configuration
CACHE_TYPE=redis  # or 'memory'
REDIS_HOST=localhost
REDIS_PORT=6379

# Rate limiting
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
```

### Configuration File (config.yaml)

```yaml
openserp:
  host: localhost
  port: 7000
  timeout: 30
  
cache:
  type: redis
  ttl: 3600
  redis:
    host: localhost
    port: 6379
    
rate_limit:
  enabled: true
  max_requests: 60
  window_seconds: 60
  
logging:
  level: INFO
  format: json
```

---

## 📚 Examples

### Example 1: Research Project (Python)

```python
from openserp_wrapper import OpenSerpClient
from datetime import datetime, timedelta

client = OpenSerpClient(base_url="http://localhost:7000")

# Search for recent AI research papers
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")

results = client.search(
    text="artificial intelligence research papers 2025",
    engines=["duckduckgo", "bing"],
    limit=50,
    date_from=date_str,
    language="EN"
)

for result in results:
    print(f"{result['title']}\n{result['url']}\n")
```

### Example 2: Price Comparison (Go)

```go
package main

import (
    "fmt"
    "github.com/upsckannaujtimes-hash/openserp-api-wrapper/pkg/client"
)

func main() {
    c := client.NewClient("http://localhost:7000")
    
    // Search for product prices
    results, _ := c.Search(context.Background(), &client.SearchRequest{
        Text:    "OnePlus 13 price India 2025",
        Engines: []string{"bing", "google"},
        Limit:   20,
    })
    
    // Parse and compare prices
    for _, result := range results.Items {
        fmt.Println(result.Title)
    }
}
```

---

## 🛠️ Development

### Project Structure

```
openserp-api-wrapper/
├── README.md
├── LICENSE
├── requirements.txt
├── go.mod
├── go.sum
├── setup.py
│
├── python/
│   ├── openserp_wrapper/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── async_client.py
│   │   ├── cache.py
│   │   ├── rate_limiter.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   ├── tests/
│   │   ├── test_client.py
│   │   ├── test_cache.py
│   │   └── test_rate_limiter.py
│   └── examples/
│       ├── basic_search.py
│       ├── advanced_filtering.py
│       └── async_search.py
│
├── go/
│   ├── pkg/
│   │   └── client/
│   │       ├── client.go
│   │       ├── types.go
│   │       └── cache.go
│   ├── cmd/
│   │   └── cli/
│   │       └── main.go
│   └── tests/
│       └── client_test.go
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── docs/
│   ├── API.md
│   ├── INSTALLATION.md
│   ├── EXAMPLES.md
│   └── CONTRIBUTING.md
│
└── .github/
    └── workflows/
        ├── tests.yml
        └── daily-updates.yml
```

### Running Tests

```bash
# Python tests
python -m pytest tests/ -v --cov=openserp_wrapper

# Go tests
go test ./... -v -cover
```

### Building Docker Image

```bash
docker build -t openserp-wrapper:latest -f docker/Dockerfile .
docker run -p 8000:8000 openserp-wrapper:latest
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Resources

- [OpenSerp Official Repo](https://github.com/karust/openserp)
- [OpenSerp Documentation](https://github.com/karust/openserp/wiki)
- [Python Requests Documentation](https://requests.readthedocs.io)
- [Go HTTP Documentation](https://golang.org/pkg/net/http)

---

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/upsckannaujtimes-hash/openserp-api-wrapper/issues)
- Start a [Discussion](https://github.com/upsckannaujtimes-hash/openserp-api-wrapper/discussions)
- Email: your-email@example.com

---

**Last Updated:** January 1, 2026  
**Maintained by:** OpenSerp API Wrapper Team
