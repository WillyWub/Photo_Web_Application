@echo off
REM
REM Windows BATCH script to run docker container
REM
@echo on
docker run -it -u user -w /home/user -v C:/Users/willi/CS310_Final_Project/server_side:/home/user -p 8080:8080 --rm --env-file ../.env cs310_final_project_server bash