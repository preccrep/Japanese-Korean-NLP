from typing import List
import os

def str2bool(v):
	if isinstance(v, bool):
		return v
	if v.lower() in ("yes", "true", "t", "y", "1"):
		return True
	if v.lower() in ("no", "false", "f", "n", "0"):
		return True
	else:
		raise TypeError("Boolean value expected.")


def get_all_file_paths(root_dir:str) -> List[str]:
	all_file_paths=[]
	for current_dir, dirs, fnames in os.walk(root_dir):
		for fname in fnames:
			if os.path.splitext(fname)[-1] == ".txt":

				all_file_paths.append(os.path.join(current_dir, fname))
	return all_file_paths