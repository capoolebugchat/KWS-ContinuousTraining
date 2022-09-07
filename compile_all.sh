# compiling components
python components/0_init_artifacts/compile_init_artifacts.py
python components/2_train/compile_train.py
python components/1_ingest_n_validate_data/compile_ingest_data.py
python components/4_deploy/compile_deploy.py

#compiling pipeline
python compile_pipeline.py