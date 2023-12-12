import os.path
import sys
from logging import getLogger
from typing import List, Optional

# make sure turcar folder is in sys.path (relevant in dev)
turcar_container = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if turcar_container not in sys.path:
    sys.path.insert(0, turcar_container)

from turcar.plugins.micropython.bare_metal_backend import (
    BareMetalMicroPythonBackend,
    launch_bare_metal_backend,
)

# Can't use __name__, because it will be "__main__"
logger = getLogger("turcar.plugins.micropython.microbit_backend")


class MicrobitMicroPythonBackend(BareMetalMicroPythonBackend):
    def _get_sys_path_for_analysis(self) -> Optional[List[str]]:
        return [
            os.path.join(os.path.dirname(__file__), "api_stubs"),
        ]


if __name__ == "__main__":
    launch_bare_metal_backend(MicrobitMicroPythonBackend)
