# FastAnnotation

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)

## General info

This is a simple framework to make object detection dataset very quickly !

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/150709016-6619a8ec-3139-4409-86d4-f004247ebe4a.PNG">
</p>

## Requirements

Use Run.bat to execute the program.

Libraries:
* Numpy
* Pandas
* Pillow

## Setup

**I-** Put all the files to be annoted in '**/DataRaw**' directory

**II-** Launch Run.bat

**III-**
* Write in Object Class the name of the class to be asigned to the bounding box.
* Push the button '**Draw BB**' in order to draw a new bounding box, do it for every bounding box.
* When you are done push the button '**Validate**' in order to save all the changes in 'annotations.csv'
* You can navigate freely between all your files and see the bounding boxes already placed.
