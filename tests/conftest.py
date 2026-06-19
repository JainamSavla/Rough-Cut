import os
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def Rough Cut():
    """Load Rough Cut.py as a namespace dict without launching the GUI."""
    path = os.path.join(ROOT, "Rough Cut.py")
    src = open(path, encoding="utf-8").read().replace("App().mainloop()", "pass")
    ns = {"__file__": path, "__name__": "Rough Cut_under_test"}
    exec(compile(src, path, "exec"), ns)
    return ns


@pytest.fixture(scope="session")
def app(Rough Cut):
    """A single shared App (one Tk root per session — repeated Tk() creation
    in one process eventually fails to load init.tcl). GUI tests must not
    destroy it."""
    a = Rough Cut["App"]()
    yield a
    try:
        a.destroy()
    except Exception:
        pass
