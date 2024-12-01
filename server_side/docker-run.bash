#!/bin/bash
#
# Linux/Mac BASH script to run docker container
#
docker run -it -u user -w /home/user -v /Users/Wilson/Desktop/CS310/project02-server-main:/home/user -p 8080:8080 --rm --env-file ../.env project02-server bash
