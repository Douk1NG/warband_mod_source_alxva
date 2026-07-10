import bootstrap_paths
import os

SOURCE_ROOT = bootstrap_paths.SOURCE_ROOT
IDS_DIR = os.path.join(SOURCE_ROOT, "ids")


def id_file(entity_name):
	"""Return absolute path for a generated ID file (e.g. id_file('troops'))."""
	return os.path.join(IDS_DIR, "ID_%s.py" % entity_name)
