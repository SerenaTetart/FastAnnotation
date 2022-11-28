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
<img src="https://user-images.githubusercontent.com/65224852/204236943-775d28a5-5db3-42e4-9bf5-c0178d8ec569.png">
</p>

And this is how the result look for both CSV files *(bounding boxes and key points)*:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/204236990-2fa52d18-493d-4d2e-ac01-b8c8bd6c2f6b.png">
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/204236984-a0b3cf4c-00b7-4658-9b63-a99caebcf57b.png">
</p>

And (a part of) the result for the XML File:

<p align="center">
<img src="https://user-images.githubusercontent.com/65224852/204237000-c5c3f5b3-e277-43ec-ba7b-f58cf9cb6f9a.png">
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
