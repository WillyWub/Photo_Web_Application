@echo off
REM
REM Windows BATCH script to build docker container
REM
@echo on
docker rmi cs310_final_project_server
docker build -t cs310_final_project_server .
