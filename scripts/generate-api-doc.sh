#!/bin/sh

cd docs
DIRECTORY="gen"
if [ ! -d "$DIRECTORY" ]; then
	mkdir "$DIRECTORY"
fi
raml2html webservice.raml > "$DIRECTORY/index.html"
