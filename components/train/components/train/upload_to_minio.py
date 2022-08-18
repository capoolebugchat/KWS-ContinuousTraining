### Script in construction, deprecated since its too labourous

import os

model_dir = "non_stream"
model_new_dir = "saved_model"
for root, dirs, files in os.walk(model_dir, topdown=True):
    for name in files:
        print(os.path.join(model_new_dir, name))
    for name in dirs:
        print(os.path.join(model_new_dir, name))
