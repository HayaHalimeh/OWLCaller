
import numpy as np
import requests
import shutil 
import matplotlib
import matplotlib as plt #import pyplot
#print("Switched to:", matplotlib.get_backend())
plt.use('Qt5Agg')


    

def request_save_image(img_url,img_out_path):
    """
    Requests images from img_url and saves image in img_out_path
    """
    response = requests.get(img_url, stream=True)
    
    with open(img_out_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    del response

def request_save_image_wiki(img_url,img_out_path):
    """
    Requests images from img_url from Wikipedia and saves image in img_out_path
    """

    headers = {
        'User-Agent': 'My User Agent 1.0'
    }
        
    response = requests.get(img_url, stream=True)
    with open(img_out_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    del response

def show_image(img_path):
    """
    Takes a path to an image and display it in RGB
    """
    import cv2
    print(img_path)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    plt.pyplot.imshow(cv2.cvtColor(np.array(img, dtype=np.uint8), cv2.COLOR_BGR2RGB))





