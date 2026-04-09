from __future__ import annotations

import argparse
import json
from functools import partial
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .service import review_source_text


WEB_DIR = Path(__file__).with_name("web")
DEFAULT_OUTPUT_DIR = Path("output") / "web"


class MetaToolRequestHandler(BaseHTTPRequestHandler):
    server_version = "MetaToolWeb/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            self._send_file(WEB_DIR / "index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/static/style.css":
            self._send_file(WEB_DIR / "style.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/static/app.js":
            self._send_file(WEB_DIR / "app.js", "application/javascript; charset=utf-8")
            return
        if parsed.path == "/api/example":
            self._handle_example(parsed.query)
            return

        self._send_json({"error": "Not found."}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/review":
            self._send_json({"error": "Not found."}, status=HTTPStatus.NOT_FOUND)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(raw_body or "{}")
            source = str(payload.get("source", ""))
            source_name = str(payload.get("source_name", "snippet.py")).strip() or "snippet.py"
            provider_name = str(payload.get("provider_name", "demo")).strip() or "demo"
            persist_output = bool(payload.get("persist_output", True))
            result = review_source_text(
                source=source,
                source_name=source_name,
                provider_name=provider_name,
                output_dir=DEFAULT_OUTPUT_DIR if persist_output else None,
            )
        except json.JSONDecodeError:
            self._send_json({"error": "Request body must be valid JSON."}, status=HTTPStatus.BAD_REQUEST)
            return
        except ValueError as error:
            self._send_json({"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
            return

        response = {key: value for key, value in result.items() if key != "finding_objects"}
        self._send_json(response)

    def _handle_example(self, query_string: str) -> None:
        query = parse_qs(query_string)
        example_path = query.get("path", ["examples/bad_main.py"])[0]
        candidate = Path(example_path)
        if not candidate.exists() or candidate.suffix != ".py":
            self._send_json({"error": f"Example file not found: {example_path}"}, status=HTTPStatus.NOT_FOUND)
            return

        self._send_json(
            {
                "source_name": candidate.name,
                "source": candidate.read_text(encoding="utf-8"),
            }
        )

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="review_web",
        description="Start the Meta-Tool web dashboard.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server to.")
    parser.add_argument("--port", default=8123, type=int, help="Port for the web dashboard.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    handler = partial(MetaToolRequestHandler)
    with ThreadingHTTPServer((args.host, args.port), handler) as server:
        print(f"Meta-Tool web dashboard running at http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nMeta-Tool web dashboard stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
