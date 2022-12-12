[![CodeFormat](https://github.com/LinusThorsell/fmeca-app/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/LinusThorsell/fmeca-app/actions/workflows/main.yml)

# FMECA Visualizer

Project developed during the course TDDI17 at Linköping University for customer SAAB Aeronautics.

## Purpose

The purpose of this project to provide a prototype for visualizing FMECA analytics for easier viewing and accessbility.

## Features

The project is split into three separate application which together create the fmeca-analysis tool. \
These are:

### - Backend

A backend framework consisting of a django database and a rest-api capable \
 of posting and retrieving data from said database. \
 More information can be found in **/backend**

### - Parser

A parser specified for parsing fmeca related data written in XML to JSON objects \
before being sent to the backend api through http post-requests. \
More information can be found in **/parser**

### - Frontend

A web application made to look similar to the old Excel way of analysing data while \
attempting to provide better functionality. Retrives JSON data from backend api and displays \
in the app. Here the data can also be filtered.

This is a work in progress and should more serve as a suggestion for future development. \
More information can be found in **/frontend**

## Database Design

Here the database design is visualized through a enhanced entity reletionship schema.\
This design has been interpreted from the latest XML project input. Currently named "Project 3". \
Head to **/backend** and **/backend/api/models.py** for information how it has been implemented.

![bild](https://user-images.githubusercontent.com/98834894/206992735-691d0260-accf-4da7-93b4-616cf2d35130.png)

## Technical Stack

Developed with the following stack:

### - Backend

- Django
- Django Rest Framework
- MariaDB / mySQL

### - Parser

- python3
- XML
- ElementTree

### - Frontend

- Vue.js
- ResizeObserver
