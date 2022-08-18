python $1 --yaml-path=$2 --env-path=$3 --data-path=$4
pip install -r requirements.txt --no-cache-dir
echo "Hyperparams loaded"

python components/train/kws_streaming/train/model_train_eval.py --alsologtostderr ds_tc_resnet
echo "Trained"