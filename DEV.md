# Dev instruction

1. Install [python](https://www.python.org/downloads/)
2. Install [conda](https://docs.conda.io/en/latest/) or [pip](https://pip.pypa.io/en/stable/installing/)
3. Use conda env or virtualenv


## Install lib

```
# download the code
git clone https://github.com/Veronishi/labelText.git
#go in labelText folder
cd labelText
# install
python setup.py install
# run
labeltext
```

## Release windows

```
# from a windows pc do
python setup.py bdist_wininst
```

## Make wheel python package
```
pip install wheel
python setup.py bdist_wheel
# load to the release and install with
# pip install https://github.com/Veronishi/labelText/releases/download/v4.6/labeltext-4.6-py3-none-any.whl
```

## Linux Mint 19.3 Cinnamon exception
This procedure work on linux mint:
```
# at list you need python3.7
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pyqt5
python setup.py install
```
