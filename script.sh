#!/bin/bash

sudo su postgres
psql
ALTER USER postgres PASSWORD 'postgres';
\q
exit
