# FastAnnotation

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)

## General info

This is a simple framework to make object detection dataset very quickly.

Pascal VOC XML and CSV files are supported ! *(they are returned each time '**Validate**' button is pressed)*

Let's see an example:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/151023217-d429bca1-6ff7-407d-b805-455dd2cab384.PNG">
</p>

And this is how the result look:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/150709583-b323e8dc-782a-4e06-ae7a-b0b1a275f49a.PNG">
</p>

## Requirements

Use Run.bat to execute the program.

Libraries:
* Numpy
* Pandas
* Pillow

## Setup

**I-** Launch Run.bat

**II-** Pick a working directory by clicking on the button with a folder on it.

**III-**
* Write in Object Class the name of the class to be asigned to the bounding box.
* Push the button '**Draw BB**' in order to draw a new bounding box, do it for every bounding box.
* When you are done push the button '**Validate**' in order to save all the changes in 'annotations.csv'
* You can navigate freely between all your files and see the bounding boxes already placed.
