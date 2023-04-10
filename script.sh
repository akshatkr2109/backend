#!/bin/bash

sudo -u postgres psql -U postgres -d postgres -c "ALTER USER postgres PASSWORD 'postgres';"
