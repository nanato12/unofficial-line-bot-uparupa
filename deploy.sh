#! /bin/bash

git pull;

# activate python venv
. venv/bin/activate

pip install -r requirements.txt

# migrate database
alembic upgrade head

if [ -f "run.pid" ]; then
    kill $(cat run.pid);
fi

# run bot
nohup python main.py -c default > nohup.log 2>&1 &
echo $! > run.pid

echo "deploy success!";