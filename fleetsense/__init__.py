"""FleetSense automotive intelligence public API."""
from .engine import FleetIntelligenceEngine
from .models import FleetDataset, SignalDefinition, TelemetryRecord

__all__ = ["FleetDataset", "FleetIntelligenceEngine", "SignalDefinition", "TelemetryRecord"]
__version__ = "0.1.0"
