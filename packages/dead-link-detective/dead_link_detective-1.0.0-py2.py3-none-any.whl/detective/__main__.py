import argparse
import asyncio
import time
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from detective import __version__

# Maximum number of concurrent coroutines
MAX_NUM_OF_COROUTINES = 10


# Asynchronous function to check if a link is active or dead
async def check_link_async(
    semaphore: asyncio.Semaphore,
    client: httpx.AsyncClient,
    url: str,
    active: list,
    dead: list,
):
    """
    Asynchronously checks if a link is active or dead.

    Args:
        semaphore (asyncio.Semaphore): Semaphore to limit the number of concurrent tasks.
        client (httpx.AsyncClient): The HTTP client.
        url (str): The URL to check.
        active (list): List to append active links to.
        dead (list): List to append dead links to.
    """
    async with semaphore:
        try:
            response = await client.head(url)
            active.append(
                (url, response.status_code)
            ) if not response.is_error else dead.append((url, response.status_code))

        except httpx.HTTPError:
            dead.append((url, 0))


# Function to extract all links from a webpage
def get_links(url: str):
    """
    Extracts all links from a webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        generator: A generator that yields the URLs.
    """
    try:
        response = httpx.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            yield urljoin(url, href)

    except httpx.HTTPError as e:
        print(f"An error occurred while fetching the URL {url}: {e}")


# Asynchronous worker function to check all links from a webpage
async def aworker(url: str, num_coroutines: int) -> tuple[list, list]:
    """
    Asynchronously checks all links from a webpage.

    Args:
        url (str): The URL of the webpage.
        num_coroutines (int): The number of coroutines to use.

    Returns:
        tuple: A tuple containing two lists: the active links and the dead links.
    """
    urls = get_links(url)
    active, dead = [], []

    semaphore = asyncio.Semaphore(num_coroutines)

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            for link in urls:
                tg.create_task(check_link_async(semaphore, client, link, active, dead))

    return active, dead


# Synchronous worker function to check all links from a webpage
def worker(url: str) -> tuple[list, list]:
    """
    Synchronously checks all links from a webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        tuple: A tuple containing two lists: the active links and the dead links.
    """
    urls = get_links(url)
    active, dead = [], []

    with httpx.Client() as client:
        for url in urls:
            try:
                response = client.head(url)
                active.append(
                    (url, response.status_code)
                ) if not response.is_error else dead.append((url, response.status_code))

            except httpx.RequestError:
                dead.append((url, 0))

    return active, dead


def argsetup():
    """
    Sets up command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Detective: A simple link checker for websites"
    )

    # Add version argument
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s v{__version__}"
    )

    # Add URL argument
    parser.add_argument(
        "url",
        metavar="url",
        type=str,
        help="The url of the website to be checked",
    )

    # Create mutually exclusive group for synchronous and asynchronous requests
    group = parser.add_mutually_exclusive_group(required=True)

    # Add synchronous requests argument
    group.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="Use synchronous requests",
    )

    # Add asynchronous requests argument
    group.add_argument(
        "-a",
        action="store_true",
        help="Use asynchronous requests",
    )

    # Add benchmark argument
    parser.add_argument(
        "-b",
        "--benchmark",
        action="store_true",
        help="Benchmark the performance of the program",
    )

    return parser.parse_args()


def write_results(args, active: list, dead: list, time_taken: float):
    """
    Writes the results to the console.

    Args:
        args (argparse.Namespace): The command line arguments.
        active (list): The active links.
        dead (list): The dead links.
        time_taken (float): The time taken to check the links.
    """
    print(f"Active links: {len(active)}")
    print(f"Dead links: {len(dead)}")

    if len(dead) > 0:
        print("Dead links:")
        for link in dead:
            print(f"  {link[0]} - {link[1]}")

    if args.benchmark:
        print(f"Checked {len(active) + len(dead)} links in {time_taken:.2f} seconds")


def main():
    """
    Main function. Parses command line arguments and checks the links.
    """
    try:
        args = argsetup()

        if args.sync:
            start = time.perf_counter()
            active, dead = worker(args.url)
            end = time.perf_counter()
            write_results(args, active, dead, end - start)

        else:
            start = time.perf_counter()
            active, dead = asyncio.run(aworker(args.url, MAX_NUM_OF_COROUTINES))
            end = time.perf_counter()
            write_results(args, active, dead, end - start)

    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
