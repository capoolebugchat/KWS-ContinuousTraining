# compiling components
python -m components.0_init_artifacts.compile_init_artifacts
python -m components.1_ingest_n_validate_data.compile_ingest_data
python -m components.2_train.compile_train
python -m components.4_deploy.compile_deploy

#compiling pipeline
python compile_pipeline.py