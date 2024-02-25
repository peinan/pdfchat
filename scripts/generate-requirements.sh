#!/bin/bash

cp requirements.lock requirements.txt
# remove `-e file:.` from requirements.txt because it's not supported by pip-compile
sed -i '' '/-e file:\./d' requirements.txt
git add requirements.txt
