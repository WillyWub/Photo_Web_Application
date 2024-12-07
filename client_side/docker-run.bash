#!/bin/bash
#
# Linux/Mac BASH script to run docker container
#
docker run -it -u user -w /home/user -v /Users/ayang/Desktop/NU_Fall_2024/CS_310/cs310_finalproject/client_side:/home/user --network="host" --rm --env-file ../.env cs310_final_project_client bash
