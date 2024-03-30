#! /bin/bash

# activate python venv
. venv/bin/activate

pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# migrate database
alembic upgrade head

if [ -f "run.pid" ]; then
    kill $(cat run.pid)
fi

# run bot
nohup python main.py -c default >"logs/$(date +"nohup_%Y%m%d_%H%M%S").log" 2>&1 &
echo $! >run.pid

echo "deploy success!"
