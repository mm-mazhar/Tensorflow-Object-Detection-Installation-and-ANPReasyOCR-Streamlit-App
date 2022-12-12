#!/bin/bash -e

PROJECT_FOLDER=$PWD
echo $PROJECT_FOLDER

echo "#################### Download and Unzip Trained Model "
wget --no-check-certificate "https://onedrive.live.com/download?cid=FAD26F9F698F8EDC&resid=FAD26F9F698F8EDC%214693&authkey=AEQ_9fS_6w44xJE"
mv './download?cid=FAD26F9F698F8EDC&resid=FAD26F9F698F8EDC!4693&authkey=AEQ_9fS_6w44xJE' './ANPRandEasyOCR_models.tar.gz'
TRAINED_MODEL='./ANPRandEasyOCR_models.tar.gz'
tar -zxvf $TRAINED_MODEL

echo "#################### Creating folders "
# #Array of folders to make
dir_array=(
'./Tensorflow/models'
'./Tensorflow/protoc/'
'./Tensorflow/workspace/annotations'
)

echo "##### Looping through dir_array and creating folders #####"
for d in "${dir_array[@]}";do
    if [ -d $d ];then
        echo "##### $d Folder already exists"
    else
        echo "##### Making Folder $d"
        mkdir -p $d
    fi
done

echo "#################### Copy Label Map "
cp label_map.pbtxt Tensorflow/workspace/annotations/

echo "#################### Downloading Tensorflow Models Repo "
git clone https://github.com/tensorflow/models './Tensorflow/models'

echo "#################### Downloading protobuf-compiler "
url="https://github.com/protocolbuffers/protobuf/releases/download/v3.19.6/protoc-3.19.6-linux-x86_64.zip"
wget -w 10 "$url"
echo "##### Moving protobuf-compiler"
mv './protoc-3.19.6-linux-x86_64.zip' './Tensorflow/protoc/'
echo "##### Unziping protobuf-compiler"
cd './Tensorflow/protoc/' && unzip 'protoc-3.19.6-linux-x86_64.zip'
cd ../../
echo "## Protoc Path ##"
PROTOC_PATH=$PWD/Tensorflow/protoc/bin
echo $PROTOC_PATH
PATH="$PROTOC_PATH:$PATH"
#sudo apt-get install protobuf-compiler

echo "#################### Protobuf Installation/Compilation "
cd Tensorflow/models/research && protoc object_detection/protos/*.proto --python_out=.  
cd ../../../
# export PYTHONPATH=$PYTHONPATH:pwd:pwd/slim

echo "##### Install the Object Detection API #####"
cd Tensorflow/models/research
cp object_detection/packages/tf2/setup.py .
python3 -m pip install .
cd ../../../

##ideally, this package should get installed when installing the Object Detection API as documented in the Install the Object Detection API section above, 
##however the installation can fail for various reasons and therefore it is simpler to just install the package beforehand, in which case later installation will be skipped.
#echo "#################### COCO API installation "
#mkdir -p './cocoapi'
#git clone https://github.com/cocodataset/cocoapi.git
#cd './cocoapi/PythonAPI'
#make
#echo $PWD
#cp -r pycocotools/. $PROJECT_FOLDER'/Tensorflow/models/research/'
#cd ../../

echo "#################### Verifying Insatallation "
VERIFICATION_SCRIPT='./Tensorflow/models/research/object_detection/builders/model_builder_tf2_test.py'
python3 $VERIFICATION_SCRIPT

echo "##### Installing Requirements.txt #####"
pip install -r linux_tfod1_requirements.txt

echo "__________________ Script END __________________"
