import logging

from ryujinx_mako._const import SCRIPT_NAME

logging.getLogger(SCRIPT_NAME).addHandler(logging.NullHandler())
