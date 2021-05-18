#!/bin/bash

python setup.py bdist_wheel
wget -O ./dist/appimage-builder.AppImage https://github.com/AppImageCrafters/appimage-builder/releases/download/v0.8.8/appimage-builder-0.8.8-4e7c15f-x86_64.AppImage
chmod +x ./dist/appimage-builder.AppImage
./dist/appimage-builder.AppImage --recipe AppImageBuilder.yml --skip-test
