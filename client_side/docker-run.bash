#!/bin/bash
#
# Linux/Mac BASH script to run docker container
#
docker run -it -u user -w /home/user -v /Users/Wilson/Desktop/CS310/project02-client-main:/home/user --network="host" --rm --env-file ../.env project02-client bash
