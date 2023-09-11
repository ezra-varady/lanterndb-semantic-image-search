#!/bin/bash

wget https://data.caltech.edu/records/nyy15-4j048/files/256_ObjectCategories.tar?download=1 -O 256.tar
tar xf 256.tar
rm -rf 256_ObjectCategories/056.dog/greg/
rm 256_ObjectCategories/198.spider/RENAME2
rm 256.tar
