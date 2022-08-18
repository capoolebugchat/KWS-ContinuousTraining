#training phase
python $1 --yaml-path=$2 --env-path=$3 --data-path=$4
pip install -r requirements.txt --no-cache-dir
echo "Hyperparams loaded"

pip install tensorflow==2.7.0
pip install -U numpy
cd components/train
python -m kws_streaming.train.model_train_eval --alsologtostderr ds_tc_resnet
echo "Trained"

#deployment phase
