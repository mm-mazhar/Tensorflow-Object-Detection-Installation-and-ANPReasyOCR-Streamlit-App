import os
import wget
import tarfile
import shutil
from git import Repo
from git import RemoteProgress
from tqdm import tqdm
from zipfile import ZipFile
import subprocess

class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count = None, message = ''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()

CUSTOM_MODEL_NAME = 'my_ssd_mobnet' 
LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    'APIMODEL_PATH': os.path.join('Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace','annotations'),
    'PROTOC_PATH':os.path.join('Tensorflow','protoc')
    }

files = {
    'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

print("#################### Creating folders ")
for path in paths.values():
    if not os.path.exists(path):
        os.makedirs(path)

print("#################### Download and Unzip Trained Model ")
wget.download("https://onedrive.live.com/download?cid=FAD26F9F698F8EDC&resid=FAD26F9F698F8EDC%214693&authkey=AEQ_9fS_6w44xJE")
# open file
file = tarfile.open('ANPRandEasyOCR_models.tar.gz')
# extracting file
file.extractall()
file.close()

print("#################### Copy Label Map ")
original = os.path.join('.', LABEL_MAP_NAME)
target = os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
shutil.copyfile(original, target)

print("#################### Downloading Tensorflow Models Repo ")
Repo.clone_from("https://github.com/tensorflow/models", paths['APIMODEL_PATH'], progress = CloneProgress())

print("#################### Downloading protobuf-compiler ")
url="https://github.com/protocolbuffers/protobuf/releases/download/v3.19.6/protoc-3.19.6-win64.zip"
wget.download(url)
source = os.path.join('.', 'protoc-3.19.6-win64.zip')
destination = paths['PROTOC_PATH']
shutil.move(source, destination) 
# Unziping
with ZipFile(os.path.join(paths['PROTOC_PATH'], 'protoc-3.19.6-win64.zip'), 'r') as zObject:
    zObject.extractall(path=paths['PROTOC_PATH'])
# Environment Variable
os.environ['PATH'] += os.pathsep + os.path.abspath(os.path.join(paths['PROTOC_PATH'], 'bin'))
print(os.environ['PATH'])

print("#################### Install the Object Detection API ")
cmd = 'cd Tensorflow/models/research && protoc object_detection/protos/*.proto --python_out=. && copy object_detection\\packages\\tf2\\setup.py setup.py && python setup.py build && python setup.py install'
subprocess.run(cmd, shell = True)
cmd = "cd Tensorflow/models/research/slim && pip install -e ."
subprocess.run(cmd, shell = True)


##ideally, this package should get installed when installing the Object Detection API as documented in the Install the Object Detection API section above, 
##however the installation can fail for various reasons and therefore it is simpler to just install the package beforehand, in which case later installation will be skipped.
# print("#################### COCO API installation ")
# cmd = "pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI" 
# subprocess.run(cmd, shell = True)

print("#################### Verifying Insatallation ")
VERIFICATION_SCRIPT = os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection', 'builders', 'model_builder_tf2_test.py')
# Verify Installation
cmd = f"python {VERIFICATION_SCRIPT}"
#print(cmd)
subprocess.run(cmd, shell = True)

#cmd = "pip install streamlit av opencv_python==4.5.5.64 opencv-python-headless==4.5.2.52 easyocr==1.6.2"
#cmd = "pip install streamlit av opencv-python==4.6.0.66"
#cmd = "pip install streamlit av opencv_python==4.5.5.64"
#subprocess.run(cmd, shell = True)

print("__________________ Script END __________________")


