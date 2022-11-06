# stable-diffusion-battle

Battle out who comes up with the best stable diffusion prompts in a 1-on-1! The pictures are updated as real-time as it gets (5-10 seconds). I hosted this a few days, but the cheapest GPU box on AWS was 0.6€/h, which makes it too expensive to host it for a longer time. However, I decided to open source my code so people can host it on their own.

![diffusion.fun](https://pbs.twimg.com/media/FghIVnZWAAA0OUs?format=jpg&name=large)

## Setup

### Server

Simple FastAPI server, used for the interaction with the user, just install the dependencies.txt and run start.sh. Does not need a GPU.

### Worker

The thing that generates the pictures using stable diffusion. Follow the instructions at [https://huggingface.co/runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5) to set up the environment at an machine with GPU, then it should work. If server and worker are on different machines, you might need to setup sshfs and adjust paths, but you will figure out.