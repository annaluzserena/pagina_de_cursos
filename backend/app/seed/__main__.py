import sys

from app.seed.seed import run

run(demo="--demo" in sys.argv[1:])
