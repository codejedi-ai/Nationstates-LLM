#! /bin/bash
git pull
source ./venv/bin/activate
python main.py
# commit the git with the given time as message in the form of "ISSUE-SOLVED: <time>"
git add .
git fetch
git commit -m "$(date) XPERIA-COMMIT"
git push

