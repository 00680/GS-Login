import os
import sys

def _configure_bundled_runtime():
    if getattr(sys, 'frozen', False):
        base = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    else:
        base = os.path.dirname(__file__)

    pb = os.path.join(base, 'playwright_browsers')
    if os.path.exists(pb):
        os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', pb)

_configure_bundled_runtime()
