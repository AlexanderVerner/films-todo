import sys
import importlib

args = list(filter(lambda x: not x.startswith("--"), sys.argv[2:]))
app_name = args[0].split(".")[0]

# Safely import test settings using importlib instead of exec
settings_module = importlib.import_module(f"{app_name}.tests.settings")

# Copy all public settings to globals
for name in dir(settings_module):
    if not name.startswith("_"):
        globals()[name] = getattr(settings_module, name)
