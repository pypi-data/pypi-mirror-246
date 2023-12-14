"""Create endpoint for FastAPI."""
from typing import Callable

from jpzipcode import read_csv_file, read_official_URL
from jpzipcode.resolver import Zip


def create_endopoint(file_path: str | None = None) -> Callable[[str], list[Zip]]:
    """Create endpoint for FastAPI."""
    if file_path is None:
        resolver = read_official_URL()
    else:
        resolver = read_csv_file(file_path)

    def zipresolver(zipcode: str) -> list[Zip]:
        return resolver.resolve(zipcode)

    return zipresolver
