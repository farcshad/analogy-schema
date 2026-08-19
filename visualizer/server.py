import os
import json
import urllib.parse
from typing import Optional, List, Dict, Any
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from visualizer.adapters import adapt_causal_backbone_to_vis, adapt_rich_event_graph_to_vis

OUTPUTS_DIR = Path("outputs")
STATIC_DIR = Path(__file__).parent / "static"


class VisualizerRequestHandler(SimpleHTTPRequestHandler):
    """
    Lightweight, dependency-free HTTP handler for the Analogy Schema Visualizer.
    Serves REST endpoints and static UI assets.
    """

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, message: str, status: int = 404):
        self._send_json({"error": message, "status": status}, status=status)

    def _sanitize_output_id(self, output_id: str) -> Optional[Path]:
        """Prevents path traversal attacks and validates folder existence."""
        clean_id = os.path.basename(urllib.parse.unquote(output_id))
        target_dir = OUTPUTS_DIR / clean_id
        if target_dir.exists() and target_dir.is_dir():
            return target_dir
        return None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. API: List available outputs
        if path == "/api/outputs":
            if not OUTPUTS_DIR.exists():
                return self._send_json({"outputs": []})
            
            subdirs = [
                d.name for d in OUTPUTS_DIR.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ]
            subdirs.sort()
            return self._send_json({"outputs": subdirs})

        # 2. API: Get Causal Backbone
        if path.startswith("/api/outputs/") and path.endswith("/backbone"):
            parts = path.split("/")
            if len(parts) == 5:
                output_id = parts[3]
                target_dir = self._sanitize_output_id(output_id)
                if not target_dir:
                    return self._send_error_json(f"Output folder '{output_id}' not found.", 404)

                bb_file = target_dir / "causal_backbone.json"
                if not bb_file.exists():
                    return self._send_error_json(f"causal_backbone.json not found in '{output_id}'.", 404)

                try:
                    with open(bb_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    vis_data = adapt_causal_backbone_to_vis(data, output_id, OUTPUTS_DIR)
                    return self._send_json(vis_data)
                except Exception as e:
                    return self._send_error_json(f"Error parsing causal_backbone.json: {str(e)}", 500)

        # 3. API: Get Rich Event Graph
        if path.startswith("/api/outputs/") and path.endswith("/rich"):
            parts = path.split("/")
            if len(parts) == 5:
                output_id = parts[3]
                target_dir = self._sanitize_output_id(output_id)
                if not target_dir:
                    return self._send_error_json(f"Output folder '{output_id}' not found.", 404)

                rich_file = target_dir / "rich_event_graph.json"
                if not rich_file.exists():
                    return self._send_error_json(f"rich_event_graph.json not found in '{output_id}'.", 404)

                try:
                    with open(rich_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    vis_data = adapt_rich_event_graph_to_vis(data, output_id, OUTPUTS_DIR)
                    return self._send_json(vis_data)
                except Exception as e:
                    return self._send_error_json(f"Error parsing rich_event_graph.json: {str(e)}", 500)

        # 4. Static Files & Root UI
        if path == "/" or path == "/index.html":
            index_file = STATIC_DIR / "index.html"
            if index_file.exists():
                content = index_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                return self.wfile.write(content)

        if path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            clean_filename = os.path.basename(rel_path)
            target_static = STATIC_DIR / clean_filename
            if target_static.exists() and target_static.is_file():
                content_type = "text/plain"
                if clean_filename.endswith(".js"):
                    content_type = "application/javascript"
                elif clean_filename.endswith(".css"):
                    content_type = "text/css"
                elif clean_filename.endswith(".html"):
                    content_type = "text/html"

                content = target_static.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", f"{content_type}; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                return self.wfile.write(content)

        self._send_error_json(f"Not found: {path}", 404)


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def run_server(port: int = 8000, host: str = "127.0.0.1", max_port_attempts: int = 10):
    current_port = port
    httpd = None
    
    for attempt in range(max_port_attempts):
        try:
            server_address = (host, current_port)
            httpd = ReusableHTTPServer(server_address, VisualizerRequestHandler)
            break
        except OSError as e:
            if "Address already in use" in str(e) or e.errno == 48:
                print(f"⚠️ Port {current_port} is busy, trying port {current_port + 1}...")
                current_port += 1
            else:
                raise e

    if not httpd:
        print(f"❌ Error: Could not bind to any port from {port} to {current_port}.")
        return

    print(f"================================================================")
    print(f"🔬 Analogy Schema Graph Explorer (Local Visualizer)")
    print(f"🌐 Server active at: http://localhost:{current_port}")
    print(f"📁 Consuming outputs from: {OUTPUTS_DIR.resolve()}/")
    print(f"⚡ Press Ctrl+C to stop.")
    print(f"================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping visualizer server...")
        httpd.server_close()
