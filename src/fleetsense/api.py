"""Dependency-free HTTP API and dashboard."""
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse
from . import __version__
from .engine import FleetSenseEngine
from .models import Telemetry

DASHBOARD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>FleetSense</title><style>body{font-family:system-ui;margin:0;background:#f3f5f7;color:#14212b}header{background:#102a43;color:white;padding:20px}main{padding:20px;max-width:1200px;margin:auto}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}.card,table{background:white;border-radius:8px;padding:16px;box-shadow:0 1px 4px #0002}table{width:100%;border-collapse:collapse;margin-top:20px}th,td{text-align:left;padding:10px;border-bottom:1px solid #ddd}.critical,.high{color:#b42318}.medium{color:#b54708}.low{color:#067647}small{color:#52606d}</style></head><body><header><h1>FleetSense Automotive AI</h1><small>Explainable maintenance triage</small></header><main><div class="cards" id="cards"></div><table><thead><tr><th>VIN</th><th>Risk</th><th>Severity</th><th>Confidence</th><th>Top driver</th><th>Action</th></tr></thead><tbody id="rows"></tbody></table><p><small>Triage hypotheses only. Confirm with OEM diagnostics and qualified personnel.</small></p></main><script>async function refresh(){const d=await fetch('/v1/fleet').then(r=>r.json()),s=d.severity_counts;document.querySelector('#cards').innerHTML=`<div class=card><b>${d.vehicle_count}</b><br>Vehicles</div><div class=card><b>${d.average_risk_score}</b><br>Average risk</div><div class=card><b>${s.critical}</b><br>Critical</div><div class=card><b>${s.high}</b><br>High</div>`;document.querySelector('#rows').innerHTML=d.maintenance_queue.map(v=>`<tr><td>${v.vin}</td><td>${v.risk_score}</td><td class=${v.severity}>${v.severity}</td><td>${v.confidence}</td><td>${v.drivers[0]?.code||'—'}</td><td>${v.recommended_action}</td></tr>`).join('')}refresh();setInterval(refresh,5000);</script></body></html>'''

def make_handler(engine: FleetSenseEngine):
    class Handler(BaseHTTPRequestHandler):
        server_version = f"FleetSense/{__version__}"
        def _json(self, status: int, value: object) -> None:
            body=json.dumps(value,separators=(",",":")).encode(); self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.send_header("Cache-Control","no-store"); self.end_headers(); self.wfile.write(body)
        def do_GET(self) -> None:
            path=urlparse(self.path).path
            if path=="/":
                body=DASHBOARD.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
            elif path=="/health": self._json(200,{"status":"ok","version":__version__})
            elif path=="/v1/fleet": self._json(200,engine.fleet_summary())
            elif path.startswith("/v1/vehicles/"):
                item=engine.get(unquote(path.removeprefix("/v1/vehicles/"))); self._json(200,item.to_dict()) if item else self._json(404,{"error":"vehicle not found"})
            else: self._json(404,{"error":"not found"})
        def do_POST(self) -> None:
            if urlparse(self.path).path!="/v1/telemetry": self._json(404,{"error":"not found"}); return
            try:
                length=int(self.headers.get("Content-Length","0"))
                if length<=0 or length>1_000_000: raise ValueError("body must be 1..1000000 bytes")
                value=json.loads(self.rfile.read(length)); rows=value if isinstance(value,list) else [value]
                results=engine.ingest_many(Telemetry.from_dict(row) for row in rows)
                self._json(HTTPStatus.CREATED,{"accepted":len(results),"assessments":[i.to_dict() for i in results]})
            except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc: self._json(400,{"error":str(exc)})
        def log_message(self, format: str, *args: object) -> None: pass
    return Handler

def serve(engine: FleetSenseEngine, host: str="127.0.0.1", port: int=8080) -> None:
    server=ThreadingHTTPServer((host,port),make_handler(engine)); print(f"FleetSense listening on http://{host}:{port}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
