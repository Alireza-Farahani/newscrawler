#!/usr/bin/env bash

# for checking a specific command execution status, use:
#if [[ $? -ne 0 ]]; then
#    exit 1
#fi
# also see https://github.com/koalaman/shellcheck/wiki/SC2181

proj_dir="${PROJECT_DIR:-/home/alireza/PycharmProjects/CrawlerTest}"
if [ "$(pwd)" != "$proj_dir" ]; then  # cd fails when current directory is the target directory
  cd "$proj_dir" || exit
fi

source ./venv/bin/activate

#python_code="import os
#import sys
#PACKAGE_PARENT = '..'
#SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
#sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))"
#python3 -c "$python_code"
#python3 -c "import sys; import os; print(sys.path)"

# -s/--start-directory Directory to start discovery (default is current directory)
test_command="python3 -m unittest discover --start-directory $proj_dir/tests/unit/spiders"
if $test_command 2>test_res.log; then  # `unittest` result goes to stderr and I couldn't capture stderr in a variable.
  echo "Unit tests passed successfully"
else
  echo "Unit tests not passed" >>/dev/stderr
#  ./send_alert.py --subject "Unittests Failed" --body #TODO: send email, notif, whatever.
#  ./send_alert.sh "Unittests Failed" "$(cat test_res.log)"
  exit 1
fi
# TODO: online tests

trap cleanup INT
function cleanup() {
    printf "\ncleanup...\n"
    sudo service mongodb stop
}
function exit_with_code() {
  # $1: exit code
  cleanup
  exit "$1"
}

## start mongodb service. #TODO: mysql for badkubeei
#sudo service mongodb start
#echo "mongo started"
## execute all spiders. command > merged-output.txt 2>&1
#scrapy list|xargs -n 1 -I % scrapy crawl % -s JOBDIR=crawls/% 2> err.log 1> out.log
## stop mongodb service.
#sudo service mongodb stop

