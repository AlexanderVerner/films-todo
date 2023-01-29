import sys

args = list(filter(lambda x: not x.startswith("--"), sys.argv[2:]))
app_name = args[0].split(".")[0]
exec("from %s.tests.settings import *" % app_name)  # pylint: disable=exec-used
