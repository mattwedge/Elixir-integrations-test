# README

## Purpose

This is a scale model of torx make, with the basic models and a simple api, it uses django rest framework to create a viewable api in the browser.

It is designed as a way to learn the mechanics of torx make.

## Setup

There is a Makefile, it has `make build` and `make start` which should be enough to get you up and running I think.

Please see the Makefile for specifics.

## Usage

There is a web server that starts up and has some common end points

http://localhost:8000/
http://localhost:8000/customer-api/

The first url is for use in the web browser, the second is a POST ONLY end point allowing for a developer to post data to ingest it into the system

While the models can be used to represent anything (due to their abstract nature) I used data from the following services as examples:

- https://pokemontcg.io/
- https://scryfall.com/docs/api
- https://developer.marvel.com/

In reality any service can be used, but why not have a bit of fun with it?

The customer api supposed both creation and updating and returns a json object with the status of the change

And example of a post is here:

```curl -X POST localhost:8000/customer-api/ -d '{"service": "Scryfall", "objects": [{"human_id": "Scryfall-7", "fields": [{"name": "CMC", "value": 4}]}, {"fields": [{"name": "CMC", "value": 2, "type": "INTEGER"}]}]}' -H "Content-Type: application/json"```