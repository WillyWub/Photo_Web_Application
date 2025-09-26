This project will have 3 functions

1. We use OpenAI’s ChatGPT API to give a summary of an image previously stored in the S3 bucket. The summary will be saved in a .txt file and will be downloaded on the user’s personal computer.

2. We use OpenAI’s ChatGPT API to implement a simple trivia game. When the user chooses to play the game, we wil call ChatGPT's API to return a unique trivia question that can be answered in one word. The user will then input their answer into the Python client, and we will again use the API to check if the answer is correct or incorrect then return that result to the client.

3. We will ask the user to input the assetid of an image that was stored previously into the S3 bucket. We will apply convolution to this image with a filter of choice that the user will choose. The filters they can choose include smoothing (reduces noise and smooths image), edge detection (highlights edges by detecting sharp intensity changes), and sharpening (enhances edges and fine details). The resulting image after the filter has been applied will be added to the S3 bucket.
