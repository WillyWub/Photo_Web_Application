#!/bin/bash
#
# Linux/Mac BASH script to build docker container
#
docker rmi cs310_final_project_client
docker build -t cs310_final_project_client .
