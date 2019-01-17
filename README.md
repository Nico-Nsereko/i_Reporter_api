# iReporter

[![Build Status](https://travis-ci.org/Nico-Nsereko/i_Reporter_api.svg?branch=develop)](https://travis-ci.org/Nico-Nsereko/i_Reporter_api) [![Coverage Status](https://coveralls.io/repos/github/Nico-Nsereko/i_Reporter_api/badge.svg?branch=develop)](https://coveralls.io/github/Nico-Nsereko/i_Reporter_api?branch=develop)

## Description
IReporter is an application aiming at helping the users bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention.

#### Getting Started
Clone the project using the [link](https://github.com/Nico-Nsereko/i_Reporter)
#### Prerequisites

 A browser with a good internet access
#### Installing
* clone the project on your local machine

 ##### Accessing the frontend of the application
The front-end of the application is hosted on gh pages and can be accessed from [here](https://nico-nsereko.github.io/i_Reporter/)

## Features

* Users can create an account with iReporter.
* User can log in.
* Users can create a red-flag record to bring any form of corruption to notice.
* Users can create an intervention to call for government intervention.
* Users can edit the red-flag or intervention details
* Users can delete their red-flag or intervention records.
* Users can add geolocation (Lat Long Coordinates) to their red-flag or intervention records.
* Users can change the geolocation (Lat Long Coordinates) attached to their red-flag or intervention records.
* Admin can change the status of a record to either under investigation, rejected (in the event of a false claim) or resolved (in the event that the claim has been investigated and resolved).

 

### End points
 HTTP method|End point|functionality 
 -----------|---------|--------------
 GET|/api/v1|A welcome route to the application for users
 GET|/api/v1/red-flags/|Return all red-flags available
 GET|/api/v1/red-flags/<red_flag_id>|Used to get a specific red-flag record's details.
 POST|/api/v1/red-flags|Used to create a red-flag record
 PATCH|/api/v1/red-flags/<red_flag_id>/location|Used to edit the location of a given red-flag record 
 PATCH|/api/v1/red-flags/<red_flag_id>/comment|Used to edit the comment of a given red-flag record
 DELETE|/api/v1/red-flags/<red_flag_id>|Used to delete a specific red-flag record 
 
 ### Tools Used
 * [Flask](http://flask.pocoo.org/) - micro web framework for Python
 * [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create a virtual environment
 * [PIP](https://pip.pypa.io/en/stable/) - A python package installer
 
 ### Deployment
 
 The API is hosted on [Heroku](https://nicoireporter.herokuapp.com/)
 
 ### Built with 
 * python/ Flask
 ### Authors
 Nsereko Nicodemus
