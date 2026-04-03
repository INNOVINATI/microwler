from collections import Counter
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import pytest


@dataclass(frozen=True)
class CrawlSite:
    base_url: str
    request_counts: Counter[str]


@pytest.fixture
def crawl_site() -> CrawlSite:
    request_counts: Counter[str] = Counter()
    pages = {
        "/": """
            <html>
              <head>
                <title>Microwler Test Root</title>
                <meta name="description" content="Root page for crawler tests" />
              </head>
              <body>
                <h1>Microwler Test Root</h1>
                <h2>Fixtures</h2>
                <p>Follow the internal links to crawl this miniature site.</p>
                <a href="/inspirational">Inspirational quotes</a>
                <a href="/plain">Plain quotes</a>
                <a href="/brochure.pdf">Download brochure</a>
              </body>
            </html>
        """,
        "/inspirational": """
            <html>
              <head><title>Inspirational Quotes</title></head>
              <body>
                <h1>Inspirational Quotes</h1>
                <p>Stay hungry, stay foolish.</p>
                <a href="/inspirational/deeper">Read more inspiration</a>
              </body>
            </html>
        """,
        "/inspirational/deeper": """
            <html>
              <head><title>Daily Inspiration</title></head>
              <body>
                <h1>Daily Inspiration</h1>
                <p>Consistency beats intensity.</p>
              </body>
            </html>
        """,
        "/plain": """
            <html>
              <head><title>Plain Quotes</title></head>
              <body>
                <h1>Plain Quotes</h1>
                <p>Keep it simple.</p>
                <a href="/plain/deeper">Read more plain quotes</a>
              </body>
            </html>
        """,
        "/plain/deeper": """
            <html>
              <head><title>Plain Follow Up</title></head>
              <body>
                <h1>Plain Follow Up</h1>
                <p>Still simple.</p>
              </body>
            </html>
        """,
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            request_counts[self.path] += 1

            if self.path == "/brochure.pdf":
                body = b"%PDF-1.4 fake brochure"
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            page = pages.get(self.path)
            if page is None:
                self.send_error(404)
                return

            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield CrawlSite(
            base_url=f"http://127.0.0.1:{server.server_port}/",
            request_counts=request_counts,
        )
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
