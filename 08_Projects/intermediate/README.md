# 🟡 Intermediate Projects

| Project | Skills Used | Description |
|---------|------------|-------------|
| 01 — Web Scraper | requests, regex, OOP | Scrape and store news articles |
| 02 — REST API Client | requests, classes, error handling | Build a robust API wrapper class |
| 03 — Data Pipeline | Pandas, file I/O, decorators | ETL pipeline for tabular data |
| 04 — Async API Fetcher | asyncio, aiohttp, generators | Fetch 100 URLs concurrently |
| 05 — ML Model Trainer | sklearn, Pandas, argparse | CLI tool to train and evaluate a model |

## Starter Code: REST API Client
```python
import requests
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class APIConfig:
    base_url: str
    api_key: str
    timeout: int = 30
    max_retries: int = 3

class APIClient:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        })
    
    def get(self, endpoint: str, params: dict = None) -> dict:
        url = f"{self.config.base_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: dict) -> dict:
        url = f"{self.config.base_url}/{endpoint}"
        response = self.session.post(url, json=data, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()
```
