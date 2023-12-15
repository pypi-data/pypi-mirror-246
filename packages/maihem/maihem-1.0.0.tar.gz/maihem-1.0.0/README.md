# maihem

## Introduction
The **maihem** python package allows you to generate synthetic text data for training and evaluating your LLMs.

## Getting Started
### Installation
To install the API, run the following command:
```
pip install maihem
```
### Obtaining your maihem API key
Get a free API key by subscribing to our product here: [www.maihem.ai](https://maihem.ai).

### Setting API key
Before using the maihem package, you need to set your maihem API key as an environment variable. You can add it to your local bash script, or directly in your python code.

#### In local bash script
For Linux, open the *.bashrc* file in your home directory (for MacOs *.bash_profile*) and add the following line
```
export MAIHEM_API_KEY = '<your_maihem_api_key>'
```

Run the following command in the terminal to apply the changes

For Linux
```
source ~/.bashrc
```

For Mac
```
source ~/.bash_profile
```

#### In python code
```
import os

os.environ['MAIHEM_API_KEY'] = '<your_maihem_api_key>'
```

## Generate synthetic data

### Persona prompts

See [run_examply.py](./run_example.py) for an example python script for persona prompt generation. The example code is also below

```
import os
import maihem as mh

os.environ['MAIHEM_API_KEY'] = 'a923c14d881247a7bad58b93d9595494'

# Parameter dictionary for persona
persona = {
    'intent': "credit card got blocked",
    'mood': "angry",
    'age': "30-40",
    'gender': "male",
    'ethnicity': "white",
    'disability': "none",
    'income': "high",
    'education': "college degree",
    'marital_status': "married",
    'children': "2",
    'employment': "employed",
    'housing': "rent",
    'occupation': "banker",
    'location': "New York",
    'sector_name': "retail banking",
    'customer_name': "John Doe",
  }

# Create data generator object
dg = mh.DataGenerator()

# Generate list of prompts for defined persona
data = dg.generate_prompts(persona, model_temperature=0.8, n_calls=3, n_prompts_per_call=2)
print(data)
```


