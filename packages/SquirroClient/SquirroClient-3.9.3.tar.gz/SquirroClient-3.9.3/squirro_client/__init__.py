"""This root level directives are imported from submodules. They are made
available here as well to keep the number of imports to a minimum for most
applications.
"""

import os

from .base import SquirroClient
from .document_uploader import DocumentUploader
from .exceptions import *  # noqa: F403
from .item_uploader import ItemUploader

__version__ = os.environ.get("SQUIRRO_VERSION", "0.1")
