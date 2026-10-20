"""Dependency-free metadata backend for the reference repository."""

def get_requires_for_build_wheel(config_settings=None):
    return []

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    raise RuntimeError("Wheel building is intentionally outside the reference scope")
