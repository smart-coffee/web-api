#!/bin/sh

cd docs
mkdir gen
raml2html webservice.raml > gen/index.html
