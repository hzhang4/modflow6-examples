import os
import pathlib as pl
import sys
import time

import matplotlib.pyplot as plt
from IPython import get_ipython

# Setup working directories
work_directories = (
    pl.Path("../examples"),
    pl.Path("../figures"),
    pl.Path("../tables"),
)
for work_dir in work_directories:
    work_dir.mkdir(parents=True, exist_ok=True)

# run settings
buildModel = True
writeModel = True
runModel = True
plotModel = True
plotSave = True
createGif = True


# Test if being run as a script
def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print(f"{method.__name__}  {(te - ts) * 1000:,.2f} ms")
        return result

    return timed


# common figure settings
figure_ext = ".png"
plt.rcParams["image.cmap"] = "jet_r"

# parse command line arguments
if is_notebook():
    if "CI" in os.environ:
        plotSave = True
    else:
        plotSave = False
else:
    for idx, arg in enumerate(sys.argv):
        if arg in ("-nr", "--no_run"):
            runModel = False
        elif arg in ("-nw", "--no_write"):
            writeModel = False
        elif arg in ("-np", "--no_plot"):
            plotModel = False
        elif arg in ("-ng", "--no_gif"):
            createGif = False
        elif arg in ("-fe", "--figure_extension"):
            if idx + 1 < len(sys.argv):
                extension = sys.argv[idx + 1]
                if not extension.startswith("."):
                    extension = "." + extension
                figure_exts = tuple(plt.gcf().canvas.get_supported_filetypes().keys())
                if extension.lower() in figure_exts:
                    figure_ext = extension

# base example workspace
base_ws = pl.Path("../examples")
for idx, arg in enumerate(sys.argv):
    if arg in ("--destination"):
        if idx + 1 < len(sys.argv):
            base_ws = sys.argv[idx + 1]
            base_ws = pl.Path(base_ws).resolve()
assert base_ws.is_dir()

# data files required for examples
data_ws = pl.Path("../data")

# set executable extension
eext = ""
soext = ".so"
if sys.platform.lower() == "win32":
    eext = ".exe"
    soext = ".dll"
if sys.platform.lower() == "darwin":
    soext = ".dylib"