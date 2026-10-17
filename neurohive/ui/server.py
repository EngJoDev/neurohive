"""
NeuroHive - HTTP API Server & Web UI Engine.
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Dict, Any

from neurohive.orchestrator.swarm import SwarmOrchestrator

orchestrator = SwarmOrchestrator()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class NeuroHiveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/dashboard", "/index.html"):
            self._serve_static_html()
            return
        
        if self.path == "/api/status":
            self._send_json(200, {
                "status": "ONLINE",
                "system": "NeuroHive Swarm",
                "agents_count": 4
            })
            return

        self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        if self.path == "/api/swarm/dispatch":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            
            try:
                payload = json.loads(body)
                prompt = payload.get("prompt", "Default task")
                result = orchestrator.run_pipeline(prompt)
                self._send_json(200, result)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        self._send_json(404, {"error": "Not Found"})

    def _serve_static_html(self):
        try:
            static_dir = os.path.join(os.path.dirname(__file__), "static")
            html_file = os.path.join(static_dir, "index.html")
            with open(html_file, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self._send_json(500, {"error": f"Failed loading dashboard: {e}"})

    def _send_json(self, status: int, data: Dict[str, Any]):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return
