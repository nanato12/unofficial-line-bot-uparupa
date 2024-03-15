# unofficial LINE Bot うぱるぱ

Used [CHRLINE](https://github.com/DeachSword/CHRLINE).

You can add this account [here](https://line.me/R/nv/profilePopup/mid=uaf64c300fb85813724ab77a2748502f6).

## Usage

```bash
$ python main.py --help
usage: main.py [-h] [-c CONFIG_NAME] [-d DEVICE] [-t TOKEN] [-l LOG_NAME]

options:
  -h, --help            show this help message and exit
  -c CONFIG_NAME, --config-name CONFIG_NAME
                        設定名
  -d DEVICE, --device DEVICE
                        デバイス名
  -t TOKEN, --token TOKEN
                        トークン
  -l LOG_NAME, --log-name LOG_NAME
                        ログファイル名
```

## venv

```bash
$ python3.12 -m venv venv
$ . venv/bin/activate
(venv) $ make init
(venv) $ make run
```

## Linter & formatter

- black
- isort
- flake8
- mypy
