#pre-training
#script's args:
# $1: yaml config file path
# $2: env path( ALWAYS IS hparam.env)
# $3: dataset dir
# $4: 

python yaml_to_env.py --yaml-path=$1 --env-path=$2 --data-path=$3
pip install -r requirements.txt --no-cache-dir
echo "Hyperparams loaded"

#training using provided script
python -m kws_streaming.train.model_train_eval --alsologtostderr ds_tc_resnet
echo "Trained"

#uploading to minio
echo "uploading train result to Minio"
python upload_to_minio.py --local-dir="train_res/ds_tc_resnet/non_stream" --bucket-name=model-store --remote-dir=$4