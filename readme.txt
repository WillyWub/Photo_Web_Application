* Note, these instructions only work for Unix systems


To setup the server and client, follow these steps:


Navigate to the /client_side folder


1. Open the docker-run.bash file
2. In the line of code: 


docker run -it -u user -w /home/user -v /Users/ayang/Desktop/NU_Fall_2024/CS_310/cs310_finalproject/client_side:/home/user --network="host" --rm --env-file ../.env cs310_final_project_client bash


3. modify the first part of the file path '/Users/ayang/Desktop/NU_Fall_2024/CS_310/cs310_finalproject/client_side' to be the file directory you are currently in on your own system


Navigate to the /server_side folder


1. Open the docker-run.bash file
2. In the line of code: 


docker run -it -u user -w /home/user -v /Users/ayang/Desktop/NU_Fall_2024/CS_310/cs310_finalproject/server_side:/home/user -p 8080:8080 --rm --env-file ../.env cs310_final_project_server bash


3. modify the first part of the file path '/Users/ayang/Desktop/NU_Fall_2024/CS_310/cs310_finalproject/server_side' to be the file directory you are currently in on your own system


Navigate to the /client_side folder


Run these commands in terminal:
1. chmod 755 *.bash
2. ./docker-build.bash
3. ./docker-run.bash


Navigate to the /server_side folder


Run these commands in terminal:
1. chmod 755 *.bash
2. ./docker-build.bash
3. ./docker-run.bash


To run the server and client, follow these steps:


Navigate to the /server_side folder


Run this command in terminal:
1. node app.js


Navigate to the /client_side folder


Run this command in terminal:
1. python3 main.py