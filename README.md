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
<img src="https://user-images.githubusercontent.com/65224852/153765830-cb40c53f-22fa-4b54-9b48-c0680fe63c34.PNG">
</p>

And this is how the result look for the CSV File:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/151023589-bdbdf776-0396-4891-8254-e62636e5e1d2.PNG">
</p>

And (a part of) the result for the XML File:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/151024255-47d25847-9b00-4de4-b851-5e7874b48af8.PNG">
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
