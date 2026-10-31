"""Utilities common to both scripts."""
import os, os.path
import subprocess

def which(program):
	try:
		return subprocess.check_output(f"which {program}",shell=True).decode().strip()
	except subprocess.CalledProcessError:
		raise Exception(f"Cannot find {program}!")

def call(*args, **kwargs):
	return subprocess.check_output(*args, **kwargs).decode()
