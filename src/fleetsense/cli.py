"""FleetSense command line interface."""
import argparse, json
from pathlib import Path
from .api import serve
from .engine import FleetSenseEngine
from .io import read_telemetry
from .synthetic import generate_fleet

def _write(value: dict, path: str | None) -> None:
    text = json.dumps(value, indent=2)
    if path: Path(path).write_text(text+"\n", encoding="utf-8"); print(f"Wrote {path}")
    else: print(text)

def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="fleetsense", description="Explainable fleet-health intelligence")
    commands = root.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo"); demo.add_argument("--vehicles", type=int, default=12); demo.add_argument("--samples", type=int, default=20); demo.add_argument("--seed", type=int, default=42); demo.add_argument("--output")
    analyze = commands.add_parser("analyze"); analyze.add_argument("input"); analyze.add_argument("--output")
    server = commands.add_parser("serve"); server.add_argument("--input"); server.add_argument("--host", default="127.0.0.1"); server.add_argument("--port", type=int, default=8080)
    return root

def main(argv: list[str] | None = None) -> int:
    args, engine = parser().parse_args(argv), FleetSenseEngine()
    if args.command == "demo": engine.ingest_many(generate_fleet(args.vehicles,args.samples,args.seed)); _write(engine.fleet_summary(),args.output)
    elif args.command == "analyze": engine.ingest_many(read_telemetry(args.input)); _write(engine.fleet_summary(),args.output)
    elif args.command == "serve":
        if args.input: engine.ingest_many(read_telemetry(args.input))
        serve(engine,args.host,args.port)
    return 0

if __name__ == "__main__": raise SystemExit(main())
