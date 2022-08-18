#build training image
train_image_name=capoolebugchat/kws-training
train_image_tag=v0.1.0
train_full_image_name=${train_image_name}:${train_image_tag}

cd "$(dirname "$0")" 
docker build -t "${train_full_image_name}" .
docker push "$train_full_image_name"

# Output the strict image name, which contains the sha256 image digest
docker inspect --format="{{index .RepoDigests 0}}" "${train_full_image_name}"