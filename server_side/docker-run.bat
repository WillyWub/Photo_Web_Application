@echo off
REM
REM Windows BATCH script to run docker container
REM
@echo on
docker run -it -u user -w /home/user -v /Users/Wilson/Desktop/CS310/CS310_Final_Project/CS310_Final_Project/server_side:/home/user -p 8080:8080 --rm --env-file ../.env cs310_final_project_server bash
