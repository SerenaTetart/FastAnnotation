# FastAnnotation

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)

## General info

FastAnnotation is a simple framework to make dataset creation very quick.

Pascal VOC XML and CSV files are supported ! *(they are returned each time '**Validate**' button is pressed)*

Left Arrow, Right Arrow and Enter key are also supported for faster navigation.

Let's see an example:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/153765919-7876617e-25a1-4e9a-a961-427efe8c8cdb.PNG">
</p>

And this is how the result look for the CSV File:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/160229591-8d61638b-3c81-44d3-a4f9-f403d9973f34.PNG">
</p>

And (a part of) the result for the XML File:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/153766142-b6219221-2e4a-4b87-a8b2-dd702612f96e.PNG">
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
* Write in Object Class the name of the class to be assigned to the bounding box.
* Push the button '**Draw BB**' in order to draw a new bounding box, do it for every bounding box.
* When you are done push the button '**Validate**' or press the key '**Enter**' in order to save all the changes in 'annotations.csv'
* You can drag or resize a bounding box by pressing left click on top of it
* You can right click on top of a bounding box in order to change its class or remove it
* You can navigate freely between all your files and see the bounding boxes already placed. *(work with arrow keys)*
