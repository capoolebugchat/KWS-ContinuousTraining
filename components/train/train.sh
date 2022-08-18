#pre-training 
python yaml_to_env.py --yaml-path=$2 --env-path=$3 --data-path=$4
pip install -r requirements.txt --no-cache-dir
echo "Hyperparams loaded"

#training using provided script
python -m kws_streaming.train.model_train_eval --alsologtostderr ds_tc_resnet
echo "Trained"

#uploading to minio


