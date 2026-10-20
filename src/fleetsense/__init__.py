"""FleetSense Automotive AI public API."""
from .engine import FleetSenseEngine
from .models import Assessment, Telemetry
__all__ = ["Assessment", "FleetSenseEngine", "Telemetry"]
__version__ = "0.1.0"
