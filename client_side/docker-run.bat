@echo off
REM
REM Windows BATCH script to run docker container
REM
@echo on
docker run -it -u user -w /home/user -v /Users/Wilson/Desktop/CS310/CS310_Final_Project/CS310_Final_Project/client_side:/home/user --network="host" --rm --env-file ../.env cs310_final_project_client bash
