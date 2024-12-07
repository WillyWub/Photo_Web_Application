#!/bin/bash
#
# Linux/Mac BASH script to run docker container
#
docker run -it -u user -w /home/user -v /Users/willi/CS310_Final_Project/client_side:/home/user --network="host" --rm --env-file ../.env cs310_final_project_client bash
