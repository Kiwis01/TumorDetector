# TumorDetector

This application is running on Flask and Python --version = Python 3.12.7
(There should not be compatibility issues)

# Example 
[![Watch the video](https://i.sstatic.net/Vp2cE.png)](https://youtu.be/vt5fpE0bzSY)

# Setup
Please make sure to install the required dependencies 

```
pip install -qr requirements.txt 
```

# Test cases 
Included 7 Images to try out the model, but feel free to use any images at your disposal

```
path = ./static/prediction_examples
```

# Disclaimer
This code utilizes ultralytics yolov5 pretrained model for the training and prediction of brain tumor dataset. This model is still undergoing training, however updates will keep being made so stay tuned for that. Here is a link to check out their repository: https://github.com/ultralytics/yolov5

# Possible Issues
This pretrained model is only compatible for unix type devices (ex. MacOS and Linux/Ubuntu). To view on Windows devices it is needed to retrain the model yourself with my data. This issue is being solved and will be updated next.
