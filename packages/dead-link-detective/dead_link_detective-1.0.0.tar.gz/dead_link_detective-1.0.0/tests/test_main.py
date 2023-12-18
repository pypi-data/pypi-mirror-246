import argparse
import asyncio
import unittest
from unittest.mock import MagicMock, patch

import httpx

from detective.__main__ import check_link_async, get_links, worker, write_results


class TestMain(unittest.TestCase):
    @patch("httpx.get")
    def test_get_links(self, mock_get):
        # Setup
        mock_get.return_value.text = '<a href="https://example.com"></a>'
        url = "https://test.com"

        # Exercise
        links = list(get_links(url))

        # Verify
        self.assertEqual(links, ["https://example.com"])

    @patch("httpx.AsyncClient.head")
    @patch("asyncio.Semaphore")
    async def test_check_link_async(self, mock_semaphore, mock_head):
        # Setup
        mock_semaphore.return_value.__aenter__.return_value = None
        mock_head.return_value.is_error = False
        mock_head.return_value.status_code = 200
        semaphore = asyncio.Semaphore()
        client = httpx.AsyncClient()
        url = "https://test.com"
        active = []
        dead = []

        # Exercise
        await check_link_async(semaphore, client, url, active, dead)

        # Verify
        self.assertEqual(active, [(url, 200)])
        self.assertEqual(dead, [])

    @patch("builtins.print")
    def test_write_results(self, mock_print):
        # Setup
        args = argparse.Namespace(benchmark=True)
        active = [("https://active1.com", 200), ("https://active2.com", 200)]
        dead = [("https://dead1.com", 404)]
        time_taken = 1.23

        # Exercise
        write_results(args, active, dead, time_taken)

        # Verify
        mock_print.assert_any_call("Active links: 2")
        mock_print.assert_any_call("Dead links: 1")
        mock_print.assert_any_call("Dead links:")
        mock_print.assert_any_call("  https://dead1.com - 404")
        mock_print.assert_any_call("Checked 3 links in 1.23 seconds")

    @patch("detective.__main__.get_links")
    @patch("httpx.Client")
    def test_worker(self, mock_client, mock_get_links):
        # Setup
        url = "https://test.com"
        mock_get_links.return_value = ["https://link1.com", "https://link2.com"]
        mock_response = MagicMock()
        mock_response.is_error = False
        mock_response.status_code = 200
        mock_client.return_value.__enter__.return_value.head.return_value = (
            mock_response
        )

        # Exercise
        active, dead = worker(url)

        # Verify
        mock_get_links.assert_called_once_with(url)
        mock_client.assert_called_once()
        self.assertEqual(
            active, [("https://link1.com", 200), ("https://link2.com", 200)]
        )
        self.assertEqual(dead, [])


if __name__ == "__main__":
    unittest.main()
