
import os
import requests
from zipfile import ZipFile
from tqdm import tqdm
import argparse

def download_url(url, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get('content-length', 0))
    filename = os.path.join(dir, url.split('/')[-1])

    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=file_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

def extract_zip(file_path, extract_to):
    with ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main(dataset_path):
    images_path = os.path.join(dataset_path, 'images')
    labels_url = 'https://github.com/ultralytics/yolov5/releases/download/v1.0/coco2017labels.zip'
    data_urls = [
        'http://images.cocodataset.org/zips/train2017.zip',
        'http://images.cocodataset.org/zips/val2017.zip',
        'http://images.cocodataset.org/zips/test2017.zip'
    ]

    # Download and extract labels
    download_url(labels_url, dataset_path)
    extract_zip(os.path.join(dataset_path, 'coco2017labels.zip'), dataset_path)

    # Download and extract images
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    for url in data_urls:
        zip_name = url.split('/')[-1]
        zip_path = os.path.join(images_path, zip_name)
        download_url(url, images_path)
        extract_zip(zip_path, images_path)
        os.remove(zip_path)  # Clean up zip file after extraction

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and extract COCO dataset.')

    main("./coco2017_dataset")

