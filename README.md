<h1 align="center">
  <img src="labelme/icons/icon.png"><br/>LabelText
</h1>

<h4 align="center">
  Image Polygonal Annotation with Python
</h4>

<div align="center">
  <a href="https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue"><img src="https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue "></a>
</div>

<div align="center">
  <a href="#tutorial"><b>Tutorial</b></a> |
  <a href="#installation"><b>Installation</b></a> |
  <a href="#usage"><b>Usage</b></a> |
  <a href="https://github.com/Veronishi/labelText/tree/master/examples/tutorial#tutorial-single-image-example"><b>Advanced Tutorial</b></a> |
  <a href="https://github.com/Veronishi/labelText/tree/master/examples"><b>Examples</b></a> |
  <a href="https://www.youtube.com/playlist?list=PLI6LvFw0iflh3o33YYnVIfOpaO0hc5Dzw"><b>Youtube FAQ</b></a>
</div>

<br/>


## Description

LabelText is an image annotation tool suitable for creation of ground truth for an image dataset for example OCR, segmentation, detection, classification, ...   
It's a fork of [Labelme](https://github.com/wkentaro/labelme).  

Labelme is a graphical image annotation tool inspired by <http://labelme.csail.mit.edu>.  
It is written in Python and uses Qt for its graphical interface.

## Tutorial

If you want detailed instructions on how to use Labelme go [here](examples/how_to_use).

## Features

- [x] Image annotation for polygon, rectangle, circle, line and point. ([tutorial](examples/tutorial))
- [x] Image flag annotation for classification and cleaning. ([#166](https://github.com/wkentaro/labelme/pull/166))
- [x] Video annotation. ([video annotation](examples/video_annotation))
- [x] GUI customization (predefined labels / flags, auto-saving, label validation, etc). ([#144](https://github.com/wkentaro/labelme/pull/144))
- [x] Exporting VOC-format dataset for semantic/instance segmentation. ([semantic segmentation](examples/semantic_segmentation), [instance segmentation](examples/instance_segmentation))
- [x] Exporting COCO-format dataset for instance segmentation. ([instance segmentation](examples/instance_segmentation))
- [x] Text auto-detection with Tesseract
- [x] Save annotations in JSON


## Requirements

- Ubuntu / macOS / Windows
- Python2 / Python3
- [PyQt4 / PyQt5](http://www.riverbankcomputing.co.uk/software/pyqt/intro)
- [Tesseract](https://pypi.org/project/pytesseract/)
- [opencv](https://pypi.org/project/opencv-python/)

## Installation

Installation for Windows:  
[click here to download .exe](https://github.com/Veronishi/labelmePyCharm/releases/download/v4.5.8/labelme-4.5.8.win-amd64.exe)

Installation for other OS:  

1. Install [python](https://www.python.org/downloads/)  
#### Conda
2. Install [conda](https://docs.conda.io/en/latest/)
3. If you need create a conda env:
```bash
conda create --name myenv
conda activate myenv
```
4.  Install the software:
```bash
conda install https://github.com/Veronishi/labelText/releases/download/v4.5.8/labelme-4.5.8-py3-none-any.whl
```
5. run with:
```bash
labelme
```

#### Pip
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
3.  Install the software:
```bash
pip install https://github.com/Veronishi/labelText/releases/download/v4.5.8/labelme-4.5.8-py3-none-any.whl
```
4. run with:
```bash
labelme
```


## Installation for DEV

Go [here](DEV.md) if you are a developer.


## Usage

Run `labelme --help` for detail.  
The annotations are saved as a [JSON](http://www.json.org/) file.

```bash
labelme  # just open gui

# tutorial (single image example)
cd examples/tutorial
labelme apc2016_obj3.jpg  # specify image file
labelme apc2016_obj3.jpg -O apc2016_obj3.json  # close window after the save
labelme apc2016_obj3.jpg --nodata  # not include image data but relative image path in JSON file
labelme apc2016_obj3.jpg \
  --labels highland_6539_self_stick_notes,mead_index_cards,kong_air_dog_squeakair_tennis_ball  # specify label list

# semantic segmentation example
cd examples/semantic_segmentation
labelme data_annotated/  # Open directory to annotate all images in it
labelme data_annotated/ --labels labels.txt  # specify label list with a file
```

For more advanced usage, please refer to the examples:

* [Tutorial (Single Image Example)](examples/tutorial)
* [Semantic Segmentation Example](examples/semantic_segmentation)
* [Instance Segmentation Example](examples/instance_segmentation)
* [Video Annotation Example](examples/video_annotation)

### Command Line Arguments
- `--output` specifies the location that annotations will be written to. If the location ends with .json, a single annotation will be written to this file. Only one image can be annotated if a location is specified with .json. If the location does not end with .json, the program will assume it is a directory. Annotations will be stored in this directory with a name that corresponds to the image that the annotation was made on.
- The first time you run labelme, it will create a config file in `~/.labelmerc`. You can edit this file and the changes will be applied the next time that you launch labelme. If you would prefer to use a config file from another location, you can specify this file with the `--config` flag.
- Without the `--nosortlabels` flag, the program will list labels in alphabetical order. When the program is run with this flag, it will display labels in the order that they are provided.
- Flags are assigned to an entire image. [Example](examples/classification)
- Labels are assigned to a single polygon. [Example](examples/bbox_detection)

## FAQ

- **How to convert JSON file to numpy array?** See [examples/tutorial](examples/tutorial#convert-to-dataset).
- **How to load label PNG file?** See [examples/tutorial](examples/tutorial#how-to-load-label-png-file).
- **How to get annotations for semantic segmentation?** See [examples/semantic_segmentation](examples/semantic_segmentation).
- **How to get annotations for instance segmentation?** See [examples/instance_segmentation](examples/instance_segmentation).

## How to build standalone executable

Below shows how to build the standalone executable on macOS, Linux and Windows.  

```bash
# Setup conda
conda create --name labelme python==3.6.0
conda activate labelme

# Build the standalone executable
pip install .
pip install pyinstaller
pyinstaller labelme.spec
dist/labelme --version
```

## Cite This Project

If you use this project in your research or wish to refer to the baseline results published in the README, please use the following BibTeX entry.

```bash
@misc{labelText,
  author =       {Venturino Veronika},
  title =        {{LabelText : un tool per la creazione di dataset di immagini con groundtruth}},
  howpublished = {\url{https://link.pdf}},
  year =         {2021}
}
```
