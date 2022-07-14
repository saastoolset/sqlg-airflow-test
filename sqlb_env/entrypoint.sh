#!/usr/bin/env bash

# set -euo pipefail
# conda activate sqlb
# exec python run.py
# setup crlf 

/bin/bash -c "source activate sqlb"
# set -e
echo current Conda Env is: ["$CONDA_DEFAULT_ENV"]

echo  'command1:' "$@"
# shift 
# echo  'command2:' "$@"

case "$1" in
  tbd)
    # other command than logetl, like similairity
    echo "$@"
    ;;
  *)
    # The command is something like bash, not an airflow subcommand. Just run it in the right environment.
    # exec "$@"
    # exec "conda run -n sqlb python3 " "$@"

	# conda  run -n sqlb python /usr/src/app/sqlglib/bin_log/logetlgs.py iv
	echo  Running [conda  run -n sqlb python "$@"]
	conda  run -n sqlb --no-capture-output python "$@"
    # exec "/opt/conda/bin/conda  run -n sqlb python /usr/src/app/sqlglib/bin_log/logetlgs.py iv"
    ;;
esac

