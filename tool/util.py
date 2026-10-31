"""Utilities common to both scripts."""
import os, os.path
import pathlib
import subprocess

def which(program):
	try:
		return subprocess.check_output(f"which {program}",shell=True).decode().strip()
	except subprocess.CalledProcessError:
		raise Exception(f"Cannot find {program}!")

def call(*args, **kwargs):
	return subprocess.check_output(*args, **kwargs).decode()

def ensure_project_root():
	# __file__ = <root>/tool/util.py
	root = pathlib.Path(__file__).resolve().parent.parent
	os.chdir(root)

class chdir:
	"""Context manager which runs a block of code in a given directory."""
	def __init__(self, target):
		self.current = os.getcwd()
		self.target = target
	def __enter__(self):
		os.chdir(self.target)
	def __exit__(self, *exc_info):
		os.chdir(self.current)
		# let any exceptions bubble up
		return False
