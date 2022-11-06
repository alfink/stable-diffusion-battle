import torch
import time
import requests
from torch import autocast
from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"
#model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16", use_auth_token=True)
pipe = pipe.to(device)

def dummy(images, **kwargs):
    return images, False
pipe.safety_checker = dummy

def generate(prompts, filenames, seed=31337):

    generator = torch.Generator("cuda").manual_seed(seed)

    with autocast("cuda"):
        images = pipe(prompts, height=512, width=512, num_inference_steps=25, guidance_scale=6, generator=generator).images
        
    for i in range(len(images)):
        images[i].save(filenames[i])

last_prompts = {"0": "", "1": ""}
while True:

    data = requests.get("http://localhost:8080/status").json()
    print(data)
    if data["started"]:
        prompts = []
        files = []
        for i in range(len(data["players"])):
            if str(i) in last_prompts and last_prompts[str(i)] != data["players"][i]["prompt"]:
                prompts.append(data["players"][i]["prompt"])
                files.append(f"../server/static/{i}.png")
                last_prompts[str(i)] =  data["players"][i]["prompt"]
        if prompts:
            generate(prompts, files)
            requests.post("http://localhost:8080/notify")
        else:
            time.sleep(1)
    else:
        time.sleep(5)