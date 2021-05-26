# Dev instruction

## Install lib

```
# install
python setup.py install
# run
labelme
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
# pip install https://github.com/Veronishi/labelText/releases/download/v4.5.8/labelme-4.5.8-py3-none-any.whl
```