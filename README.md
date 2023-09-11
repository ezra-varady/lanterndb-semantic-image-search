# LanternDB Semantic Image Search
This project aims to provide a simple web interface providing CLIP based semantic image search backed by LanternDB

## TL:DR

This project assumes you have a Postgres installation running (locally) with [lanterndb](https://github.com/lanterndata/lanterndb) and [lanterndb_extras](https://github.com/lanterndata/lanterndb_extras) installed. Installation instructions for these extensions can be found in their respective repos. 

I include scripts to download an image dataset to populate the database (on a g4dn.xlarge this takes about an hour). This is totally optional, but to support this I do not allow django to manage the table. As a consequence it expects that the following has already been done
```
CREATE EXTENSION lanterndb;
CREATE EXTENDION lanterndb_extras;
CREATE TABLE IF NOT EXISTS image_table (
	v REAL[],
	location VARCHAR,
	id SERIAL PRIMARY KEY
);
CREATE INDEX semantic_image ON image_table USING hnsw (v dist_cos_ops) WITH (M=5, ef=20, ef_construction=20, dims=512);
```
This should be sufficient to use the app, though you will have to upload images by hand

## Using the project
Once you have the database set up you can run the django app with `python3 manage.py runserver`
TODO: add some images of this

## Loading the Caltech-256 dataset

This is an image dataset that happens to be a convenient size for testing the functionality I'm interested in. To dowload it and insert it into the database run
```
./dl_cal256.sh
python3 load.py
```
With this done lantern is already able to perform semantic image search! Albeit without an interface 

![Demo](images/ascii_cast.gif)
