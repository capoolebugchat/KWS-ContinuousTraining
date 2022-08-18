import argparse
from ast import arg
from pathlib import Path
import yaml

# Function doing the actual work (Outputs first N lines from a text file)
def yaml_to_env(yaml_file, env_file):
    
    hyperparams = yaml.safe_load(yaml_file)    
    for item,key in enumerate(hyperparams, 0):
        env_file.write(f"{key} = {item}\n")

parser = argparse.ArgumentParser(description='None')

parser.add_argument('--yaml-path', type=str,
    help='Path of the yaml file.')
parser.add_argument('--env-path', type=str,
    help='Path of the dotenv file where hyperparams should be written.')
args = parser.parse_args()

yaml_f = open(args.yaml_path,'r')
env_f = open(args.env_path,'w')
yaml_to_env(yaml_f, env_f)
yaml_f.close()
env_f.close()
