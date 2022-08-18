import argparse
from ast import arg
from pathlib import Path
import yaml
import logging

# Function doing the actual work (Outputs first N lines from a text file)
def yaml_to_env(yaml_file, env_file, data_path):
    
    hyperparams = yaml.safe_load(yaml_file)
    hyperparams['data_path'] = data_path
    logging.info("Loading hyperparams:")
    print("Loading hyperparams:")
    for key in hyperparams:
        logging.info(f"{key} = {hyperparams[key]}")
        print(f"{key} = {hyperparams[key]}")
        if isinstance(hyperparams[key], str):
            env_file.write(f"{key} = '{hyperparams[key]}'\n")
        else: env_file.write(f"{key} = {hyperparams[key]}\n")

parser = argparse.ArgumentParser(description='None')

parser.add_argument('--yaml-path', type=str,
    help='Path of the yaml file.')
parser.add_argument('--env-path', type=str,
    help='Path of the dotenv file where hyperparams should be written.')
parser.add_argument('--data-path', type=str,
    help='Path of the dataset.')
args = parser.parse_args()

yaml_f = open(args.yaml_path,'r')
env_f = open(args.env_path,'w')
yaml_to_env(yaml_f, env_f, args.data_path)
yaml_f.close()
env_f.close()

