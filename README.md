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
- https://rapidapi.com/omgvamp/api/hearthstone

In reality any service can be used, but why not have a bit of fun with it?

The customer api supposed both creation and updating and returns a json object with the status of the change

And example of a post is here:

```curl -X POST localhost:8000/customer-api/ -d '{"service": "Scryfall", "objects": [{"human_id": "Scryfall-7", "fields": [{"name": "CMC", "value": 4}]}, {"fields": [{"name": "CMC", "value": 2, "type": "INTEGER"}]}]}' -H "Content-Type: application/json"```

## The test

Using the django admin panel create a service for one of the APIs listed above, you will then have to analyse the data from the api and create fields and forms to represent a single object returned from the api in the django api. It is important to think carefully how to represent a given object, once you have designed the object representation you will ingest data from the api.

You will write your implementation in `core/management/commands/{service}.py` as this can easily be run as a management command.

Running your code is as simple as `make <service>` where the service is one of:

- mtg
- hearthstone
- pokemon
- marvel

Use the models directly to create the data in the system.
