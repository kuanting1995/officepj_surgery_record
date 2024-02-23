# [Production](<https://ing2.kfsyscc.org/hookap> "Title") 

# 使用方式
## 安裝

### CREATE VENV
```sh
cd app
virtualenv -p ~/.pyenv/versions/3.8.6/bin/python env
source ./env/bin/activate
```

### PIP ERROR FOR PYTHON3.7
```sh
curl -sS https://bootstrap.pypa.io/get-pip.py |  python
pip install -U pip setuptools==57.5.0
```
### pip install package
```sh
pip install -r requirements.txt
```

### start
```sh
cd app
bask start.sh
```
