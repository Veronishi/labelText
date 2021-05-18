# Dev instruction

## Install lib

```
python setup.py install
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
# load to the release and when the repo will be public you can install with
# pip install https://github.com/Veronishi/labelmePyCharm/releases/download/v4.5.8/labelme-4.5.8-py3-none-any.whl
```