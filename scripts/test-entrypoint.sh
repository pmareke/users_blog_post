#!/bin/sh
set -eE

alembic upgrade head

"$@"

