# Tensorflow Object Detection Installation and ANPReasyOCR Streamlit-App

- `git clone "https://github.com/mazqoty/Tensorflow-Object-Detection-Installation-and-ANPReasyOCR-Streamlit-App.git"`
- `conda create -n envobjdetection pip python=3.9` or `python -m venv envobjdetection`
- `conda activate envobjdetection` or `.\envobjdetection\Scripts\activate` for Windows `source envobjdetection/bin/activate` for Linux
-  Optional `conda install -n envobjdetection ipykernel --update-deps --force-reinstall` or `python3 -m ipykernel install --user --name=envobjdetection`
- `pip install -r win_tfod1_requirements.txt` for Windows
- RUN
    For Windows `python ./objdetection_installation.py`
    For Linux `bash ./objdetection_installation.sh`
- Error handling: Please use this tutorial: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html
    - During 'Install the Object Detection API',  if `no module error` is occured then just find the relevent `pip install <module name>` command and run it
    - To speed up, comment out lines of code as shown in the figure below and run it again
        <table style="width:100%">
            <tr>
                <td><img src="https://i.imgur.com/AZYIThD.jpg" width="200px" height=100px/></td>
            </tr>
        </table>
- Finally, After Verification step following result must be seen otherwise installation is messed up preferable something wrong with pycocotools.
    <table style="width:100%">
        <tr>
            <td><img src="https://i.imgur.com/uRsX4Q7.jpg" width="200px" height=50px/></td>
        </tr>
    </table>
- RUN `streamlit run app.py`

- Other useful commands
- `conda env list`
- `conda env remove -n ENV_NAME`
- `conda list`
- `python.exe -m pip install -r win_tfod1_requirements.txt --user`


