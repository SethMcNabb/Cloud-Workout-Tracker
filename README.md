# Overview

I have been very curious about learning about different types of databases so for this module I wanted to practice connecting to a cloud noSQL database for the first time. I developed this simple command line Cloud Workout Tracker to practice to do just that as well as to be something to actually use!

This software connects to a cloud database via an API wrapper, which allows users to log, manage, filter, and delete weight training session data through a simple command line interface.

My purpose for writing this is to pracice remote API authtication, connecting to cloud noSql database for the first time, and building something with many possibly future impletmentations for personal and other use.

[Software Demo Video](https://www.youtube.com/watch?v=OullZpqaZLw)

# Cloud Database

This application uses Google Cloud Firesbase, which is a fully managed, scalable noSql document database that uses flexible key value pairs.

It has two collections:

workouts Collection: Stores parent session metadata, including date, workout split, duration in minutes, and session notes.

exercise_logs Collection: Stores individual movement sets containing exercise names, set counts, rep counts, and weights, linked back to parent sessions via a relational workout_id document reference.

# Development Environment

Tools: Python, Firebase, Firebase 


# Cloud-Workout-Tracker
