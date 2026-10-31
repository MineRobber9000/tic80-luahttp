#!/usr/bin/python3
"""Generate the include header for the CA bundle."""
import os, os.path
import util
import sys

PERL = util.which("perl")
WGET = util.which("wget")
XXD = util.which("xxd")

MK_CA_BUNDLE = "https://github.com/curl/curl/raw/refs/heads/master/scripts/mk-ca-bundle.pl"

# Into the tool directory
os.chdir(os.path.dirname(__file__))

# Download curl's mk-ca-bundle.pl
try:
	util.call([WGET,"-N",MK_CA_BUNDLE])
except:
	print("WARNING: Downloading of mk-ca-bundle.pl failed!",file=sys.stderr)
	if os.path.exists("mk-ca-bundle.pl"):
		print("We have a version on disk, but it might be out of date...",file=sys.stderr)
		if os.isatty():
			if (input("Continue anyways? (y/N): ") or "n")[0].lower()=="y":
				pass
	raise

# Run it
util.call([PERL, "mk-ca-bundle.pl"])

# Package ca-bundle.crt for inclusion in our source tree
dump = util.call([XXD, "-i", "-n", "ca_bundle", "ca-bundle.crt"])
with open("../src/ca_bundle.h", "w") as f:
	f.write(dump)
