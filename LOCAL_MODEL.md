# Running AI Town with Local Models
With the increased prevalence of open-source models, the following project has been modified to support local LLMs via Ollama's API endpoints. This includes various functionality such as completion, chat, and embedding generation. There are, however, additional Ollama API endpoints that can be leveraged in the future. 

## Hardware/Software Requirements
Hardware and software requirements for both client-side simulation and LLM server are listed below
- Client-side simulation
  - Python version 3.9.12 as listed in README.md
  - Python packages as listed in requirements.txt
- LLM Server running Ollama
  - Ollama supports Linux, MacOS, and Windows (preview)
  - Recommended hardware for LLM server can be found [here](https://github.com/open-webui/open-webui/discussions/736)
  - If CUDA-enabled GPU is available, a more recent version of CUDA is recommended (e.g. 11.0 - 12.0)

## Installing Ollama
To host LLMs on a local machine, you will need to install Ollama on the machine and start the Ollama server

### Step 1. Installing Ollama
Ollama can be found at https://ollama.ai/ with Linux and MacOS currently supported (Windows version in preview). In a Linux environment, Ollama can be installed via the following command.
```
$ curl https://ollama.ai/install.sh | sh
```
If sudo access is unavailable, Ollama can be installed locally by downloading the self-contained binary.
```
$ curl -L https://ollama.ai/download/ollama-linux-amd64 -o <directory-of-your-choice>/ollama
$ chmod +x <directory-of-your-choice>/ollama
```

### Step 2. Running Ollama Server
The Ollama server will host an API used to generate responses and modify models. The API can be found at https://github.com/ollama/ollama/blob/main/docs/api.md. To start the server on a specific port and IP, run the following command with the environment variable ```OLLAMA_HOST```.
```
$ OLLAMA_HOST=0.0.0.0:8888 ollama serve
```
The above example starts the server on port 8888 listening to requests from all IP addresses.

### Step 3. Download a Model
To download a model, first make sure the Ollama server is running. Then use the ```pull``` request to download an available model from https://ollama.ai/library. 
```
$ OLLAMA_HOST=0.0.0.0:8888 ollama pull mistral:latest
```
Here, we're pulling the ```mistral:latest``` model. Other models can be imported and configured using a Modelfile as specified here - https://github.com/ollama/ollama/blob/main/docs/import.md.

Additional documentation can be found at https://github.com/ollama/ollama/tree/main/docs.

## Project Setup
Running the project with local LLMs and on a remote server will require additional setup steps. 

### Step 1. Download / Clone this Fork of Generative Agents Repository
Be sure to clone this repository as it contains the commits that enable local LLMs.
```
$ git clone https://github.com/peizhiliu168/generative_agents.git 
```

### Step 2. Create a new Python Virtual Environment
Here we're using Python Virtual Environments with pip. I have not tested with conda but you can try. First, create a virtual environment.
```
$ python -m venv my-venv
```
This creates a virtual environment called ```my-venv```. There should be a new directory named ```my-venv```. To activate the environment, use ```source```.
```
$ source <path-to-my-venv>/bin/activate
```

### Step 3. Install Dependencies
The list of dependencies can be found in ```<project-directory>/requirements.txt```. Use pip to install the required dependencies.
```
$ pip install -r <project-directory>/requirements.txt
```
Depending on Python and pip versions, you might encounter dependency issues during installation. In those cases, manually install the conflicting packages and remove the corresponding version requirements in ```requirements.txt```.

### Step 4. Create ```utils.py``` File
To configure the project, add a file named ```utils.py``` under the ```reverie/backend_server``` directory. A sample file is shown below.
```
# Local / OpenAI Models
use_local_model = True # Use Ollama or OpenAI API

# Local model configuration
local_model_host = "" # Ollama host e.g. "0.0.0.0:8888"
local_model_name = "" # model name from Ollama e.g. "mistral:latest"

# Copy and paste your OpenAI API Key
openai_api_key = ""
# Put your name
key_owner = ""

maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

collision_block_id = "32125"

# Verbose 
debug = True
```
Notice Notice the three additional configuration variables use_local_model, local_model_host, and local_model_name. Set these accordingly based on the Ollama server hostname, port, and model to run.

### Step 5. Create New Folders
To avoid errors during simulation, create the following ```movement``` folders in the project.
```
$ mkdir environment/frontend_server/storage/base_the_ville_isabella_maria_klaus/movement 
$ mkdir environment/frontend_server/storage/base_the_ville_n25/movement
```

### Step 6. Allow Hosts in Frontend
If the frontend of the simulation is hosted on a remote machine, the frontend should be modified to allow access from a local browser. This required modification to the ```ALLOWED_HOSTS``` in the Django project.

In ```environment/frontend_server/frontend_server_settings/base.py``` as well as ```environment/frontend_server/frontend_server/settings/local.py```, modify the ```ALLOWED_HOSTS``` variable as such.
```
...
DEBUG = True

ALLOWED_HOSTS = ["your-host-name"]
...
```
After these steps, the simulation should be ready to run.

## Running the Simulation
Running the simulation follows similarly as in the [README.md](https://github.com/peizhiliu168/generative_agents/blob/main/README.md). It's important to realize that responses generated by local models might be of poorer quality and can have issues in response parsing.

### Step 1. Starting the Frontend
To start the frontend server on a specific IP and port (e.g. ```0.0.0.0:8000```) run the following command from ```environments/frontend_server```.
```
$ python manage.py runserver 0.0.0.0:8000
```
You can now go to ```http://your-host-name:your-port``` on a web browser to confirm the frontend has started.

### Step 2. Starting the Backend
To start the backend simulator, under directory ```reverie/backend_server``` run 
```
$ python reverie.py
```
You will then be prompted to ```Enter the name of the forked simulation: ```. You can choose different base simulations for example ```base_the_ville_isabella_maria_klaus``` or ```base_the_ville_n25```. 

```
$ Enter the name of the forked simulation: base_the_ville_isabella_maria_klaus
```

You will then be prompted to ```Enter the name of the new simulation: ```. Give it a name of your choice, making sure you have not chosen that name before.

```
$ Enter the name of the new simulation: demo-000
```

You will now be able to see the base simulation in the front end at the following URL ```http://your-host-name:your-port/simulator_home```. **Keep this window open and in the foreground throughout the entire duration of the simulation.** Otherwise, the simulation will stop.

Finally, you will be prompted to ```Enter option: ``` to run various commands allowed by the backend. to run the simulation, use the ```run``` command followed by the number of steps. 
```
$ Enter option: run 10000
```
Each step corresponds to 10 seconds in the simulation. Thus, 10,000 steps is a bit over a day.

### Step 3. Saving and Finishing the Simulation
To save the simulation, use the ```save``` command.
```
$ Enter option: save
```
To save and finish the simulation, use the ```fin``` command.
```
$ Enter option: fin
```
Additional commands and information can be found in the [README.md](https://github.com/peizhiliu168/generative_agents/blob/main/README.md).

## Potential Issues
As mentioned, there are several potential issues when running the simulation.

1. For the simulation to progress, the simulation page in your browser should be active (the simulation might stop if you have the tab opened in the background) 
2. Local models might generate poor-quality responses, resulting in errors during response parsing. In the case of the error, the backend will continue running, asking to ```Enter option:``` again. You can use the ```run``` command to retry again for better responses.
