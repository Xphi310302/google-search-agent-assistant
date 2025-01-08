
from bs4 import BeautifulSoup
from typing import Dict, List, Union
from loguru import logger
import asyncio
import aiohttp
import requests
from langchain_core.tools import tool
import os
import httpx

@tool
async def process_search_results(input: str) -> list:
    """
    Processes a list of search queries to collect URLs, their frequencies, descriptions, and ages from search results.
    This function must be invoked **only once** per query as it fetches search results.

    Args:
        input (str): The query to process.
    """
    queries = [input]
    search_results_list = []
    for query in enumerate(queries):
        search_results = await async_get_search_results(query)
        for result in search_results:
            search_results_list.append({
                "title": result["title"],
                "url": result["link"],
                "snippet": result["snippet"],
            })
    return search_results_list



async def async_get_search_results(
    input: str, freshness: Union[str, None] = None
) -> List:
    """
    Fetches search results from Brave's search API based on the input query and freshness parameter.

    Note: This function must only be called **only once** per question to avoid exceeding rate limits.

    Parameters:
    input (str): The search query.
    freshness (Optional[str]): Optional freshness parameter for filtering results.

    Returns:
    List: JSON response containing search results.

    Raises:
    HTTPStatusError: If the API request fails
    """
    url = "https://customsearch.googleapis.com/customsearch/v1"
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    params = {
        "q": input,
        "key": api_key,
        "cx": search_engine_id,
        "num": 3,  # number of returned results
        "safe": "active",  # Enables SafeSearch filtering
        "sort": "date:d",  # latest news on top
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=10.0)
        if response.status_code == 200:
            results = response.json().get("items", [])
            return results
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []


def get_page_content(input: str) -> str:
    """
    Fetches and extracts the main content from a webpage.

    Note: This function must be used **only once** per URL to minimize redundant requests.

    Parameters:
    input (str): The URL to fetch.

    Returns:
    str: Extracted text content of the webpage.
    """
    html = requests.get(input).text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(strip=True, separator="\n")


async def fetch(session, url, timeout=8):
    async with session.get(url, timeout=timeout) as response:
        return await response.text()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(strip=True, separator="\n")


async def fetch_and_parse(session, url):
    # logger.info(f"Fetch url: {url}")
    try:
        html = await fetch(session, url)
        paras = parse(html)
        return paras
    except Exception as e:
        return f"Can not fetch the {url}"


@tool
async def async_get_page_content(url: str):
    """
    Fetches and extracts the main content from a webpage asynchronously.
    Note: This function must be used **only once** if you found enough information.

    Args:
        url (str): The URL to fetch.
    """
    async with aiohttp.ClientSession() as session:
        return await fetch_and_parse(session, url)


# Configure tools
web_tools = [process_search_results, async_get_page_content]