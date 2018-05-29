# Tooling

There are various API Elements tools available to interact and parse API
Description Documents.

## [API Description Parsing Service](http://docs.apiblueprintapi.apiary.io/#reference)

API Description Parsing Serice (formerly API Bluerpint API) is a hosted service
that takes API Description documents such as API Blueprint or Swagger 2.0 as
input and returns API Elements.

## JavaScript

### [Fury](https://github.com/apiaryio/fury.js)

Fury is a library for validating and parsing API description documents, Furys
API provides [API Element JS](https://api-elements-js.readthedocs.io/) objects.

### [API Element JS](https://api-elements-js.readthedocs.io/)

The API Elements JS Package provides an interface for querying and interacting
with API Elements. This library can be used in conjunction with Fury to handle
parsing of API Description documents into API Elements.

## Python

### [refract.py](https://github.com/kylef/refract.py)

A Python library for interacting with Refract and API Element in Python.

---

## API Blueprint

The API Blueprint ecosystem heavily uses API Elements under the hood. Although
we would recommend interacting with API Elements using the JavaScript tooling
above as it is generic and not API Blueprint specific.

### [Drafter](https://github.com/apiaryio/drafter)

Drafter is a library for parsing API Blueprint documents and return parse results in API Elements.

### [Drafter JS](https://github.com/apiaryio/drafter-npm)

Drafter JS is a JavaScript interface to Drafter and can be used in Node.JS or natively in a browser.
