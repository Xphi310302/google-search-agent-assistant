LLM = {
    "gpt-3.5-turbo": {
        "model": "gpt-3.5-turbo",
        "price_in": 0.001,
        "price_out": 0.002,
        "max_tokens": 2048,
    },
    "gpt-4-turbo": {
        "model": "gpt-4o-2024-08-06",
        "price_in": 0.005,
        "price_out": 0.015,
        "max_tokens": 16384,
    },
    "gpt-4o-mini": {
        "model": "gpt-4o-mini",
        "price_in": 0.00015,
        "price_out": 0.0006,
        "max_tokens": 16384,
    },
    "gpt-4": {
        "model": "gpt-4",
        "price_in": 0.03,
        "price_out": 0.06,
        "max_tokens": 2048,
    },
    "gemini-pro": {
        "model": "models/gemini-1.5-pro-latest",
        "price_in": 0.00175,
        "price_out": 0.0105,
        "max_tokens": 8192,
    },
    "gemini-flash": {
        "model": "models/gemini-1.5-flash-latest",
        "price_in": 0.00035,
        "price_out": 0.00105,
        "max_tokens": 8192,
    },
    "gemini-2.0-flash": {
        "model": "models/gemini-2.0-flash-exp",
        "price_in": 0.00175,
        "price_out": 0.0105,
        "max_tokens": 8192,
    },
    "claude-pro": {
        "model": "claude-3-opus-20240229",
        "price_in": 0.015,
        "price_out": 0.075,
        "max_tokens": 4096,
    },
    "claude-fast": {
        "model": "claude-3-5-haiku-20241022",
        "price_in": 0.001,
        "price_out": 0.005,
        "max_tokens": 8192,
    },
    "claude-medium": {
        "model": "claude-3-5-sonnet-20241022",
        "price_in": 0.003,
        "price_out": 0.015,
        "max_tokens": 8192,
    },
}

EMBEDDING = {
    "embedv3-small": {"model": "text-embedding-3-small", "price": 0.00002},
    "embedv3-large": {"model": "text-embedding-3-large", "price": 0.00013},
    "adav2": {"model": "text-embedding-ada-002", "price": 0.0001},
}