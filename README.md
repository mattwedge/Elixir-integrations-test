# README

## Purpose

This is a scale model of torx make, with the basic models and a simple api, it uses django rest framework to create a viewable api in the browser.

It is designed as a way to learn the mechanics of torx make.

## Setup

There is a Makefile, it has `make build` and `make start` which should be enough to get you up and running I think.

Please see the Makefile for specifics.

## Usage

There is a web server that starts up and runs on: http://localhost:8000/

## The test

### Description Of Problem

At Elixir we often have to work with third party apis and ingest data into our system, we write bespoke programs that we call `biz_rules` to perform this integration. This test is a scale model of the sort of work we do quite frequently and is quite reflective of what a typical day might look like. Your task will be to write a biz_rule, we have selected some apis and you may choose whichever one you like and write the code in the matching `core/management/commands/<service>` file.

You may need to use the django admin panel and create a service for your chosen api, you will then have to analyse the data from the api, create fields and forms to represent a single object returned from the api in the django admin.

It is important to think carefully how to represent a given object, once you have designed the object representation you will ingest data from the api.

Use the models directly and do not use the `customer-api` route when writing your biz_rule.

### The Services

- https://pokemontcg.io/
- https://scryfall.com/docs/api
- https://developer.marvel.com/
- https://rapidapi.com/omgvamp/api/hearthstone


### Running your biz_rule

Running your code is as simple as `make <service>` where the service is one of:

- mtg
- hearthstone
- pokemon
- marvel
