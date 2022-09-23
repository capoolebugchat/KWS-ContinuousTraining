# Keyword-spotting-train

Training code for keyword-spotting repository

## Setup
```
pip install -r requirements.txt --no-cache-dir
```

## Training steps:

Configure hyper parameters in `hparams.env`:
- `wanted_words`: labels of each class
- `data_path`: path of the training dataset
- `train_res`: directory to store logs and checkpoints
- `split_data`: 1 to use autosplit, 0 if the data is already structured as below:
```
train_dataset >
  training >
    word_1 >
      audio_0.wav
      audio_1.wav
    word_n >
      audio_2.wav
      audio_3.wav
  validation >
    word_1 >
      audio_6.wav
      audio_7.wav
    word_n >
      audio_8.wav
      audio_9.wav
  testing >
    word_1 >
      audio_12.wav
      audio_13.wav
    word_n >
      audio_14.wav
      audio_15.wav
  _background_noise_ >
    audio_18.wav
```

Run

```
python -m kws_streaming.train.model_train_eval --alsologtostderr ds_tc_resnet
```

# Train using docker
## Docker with CPU
```
cd keyword-spotting-train
```
Build docker image:
```
docker build -f Dockerfile-train-cpu -t kws-training-cpu:latest .
```
Start the docker container:
```
docker run --net host --restart always -itd -v $PWD:/workspace/keyword-spotting-train --name kws-training-cpu  kws-training-cpu:latest
```
Execute into the container and start training:
```
docker exec -it kws-training-cpu bash

python -m kws_streaming.train.model_train_eval --alsologtostderr ds_tc_resnet
```
## Docker with GPU
```
cd keyword-spotting-train
```
Build docker image:
```
docker build -f Dockerfile-train-gpu -t kws-training-gpu:latest .
```
Start the docker container:
```
docker run --net host --gpus all --restart always -itd -v $PWD:/workspace/keyword-spotting-train --name kws-training-gpu  kws-training-gpu:latest
```
Execute into the container and start training:
```
docker exec -it kws-training-gpu bash

python -m kws_streaming.train.model_train_eval --alsologtostderr ds_tc_resnet
```