import os
import subprocess
import numpy as np
import PIL.Image
import cv2
import supervision as sv
import torch
from mmengine.config import Config
from mmengine.dataset import Compose
from mmengine.runner import Runner
from mmengine.runner.amp import autocast
from mmyolo.registry import RUNNERS
from torchvision.ops import nms


# Clone the repository
repo_url = "https://github.com/AILab-CVC/YOLO-World"
if not os.path.exists('YOLO-World'):
    subprocess.run(["git", "clone", "--recursive", repo_url], check=True)

os.chdir('YOLO-World')

# Install dependencies
def install_dependencies():
    if 'COLAB_GPU' in os.environ:
        subprocess.run(["pip", "install", "torch==2.1.2", "torchvision==0.16.2", "torchaudio==2.1.2", "--index-url", "https://download.pytorch.org/whl/cu121"], check=True)
        subprocess.run(["pip", "install", "requests==2.28.2", "tqdm==4.65.0", "rich==13.4.2"], check=True)
        subprocess.run(["mim", "install", "mmengine>=0.7.0"], check=True)
    else:
        subprocess.run(["pip", "install", "torch", "wheel", "requests==2.28.2", "tqdm==4.65.0", "rich==13.4.2"], check=True)

# subprocess.run(["pip", "install", "-e", "."], check=True)

# Download pretrained weights and images
def download_files():
    if not os.path.exists("pretrained_weights"):
        os.makedirs("pretrained_weights")
    
    urls = [
        "https://huggingface.co/wondervictor/YOLO-World/resolve/main/yolo_world_v2_l_obj365v1_goldg_pretrain_1280ft-9babe3f6.pth",
        "https://media.roboflow.com/notebooks/examples/dog.jpeg"
    ]
    
    for url in urls:
        subprocess.run(["wget", "-P", "pretrained_weights/", url], check=True)

download_files()

# Load model configurations and run inference
cfg = Config.fromfile(
    "configs/pretrain/yolo_world_v2_l_vlpan_bn_2e-3_100e_4x8gpus_obj365v1_goldg_train_1280ft_lvis_minival.py"
)
print("bb")
cfg.work_dir = "."
cfg.load_from = "pretrained_weights/yolo_world_v2_l_obj365v1_goldg_pretrain_1280ft-9babe3f6.pth"
runner = Runner.from_cfg(cfg)
runner.call_hook("before_run")
runner.load_or_resume()
pipeline = cfg.test_dataloader.dataset.pipeline
runner.pipeline = Compose(pipeline)

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
mask_annotator = sv.MaskAnnotator()

class_names = ("person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, "
               "traffic light, fire hydrant, stop sign, parking meter, bench, bird, "
               "cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, "
               "backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, "
               "sports ball, kite, baseball bat, baseball glove, skateboard, "
               "surfboard, tennis racket, bottle, wine glass, cup, fork, knife, "
               "spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, "
               "hot dog, pizza, donut, cake, chair, couch, potted plant, bed, "
               "dining table, toilet, tv, laptop, mouse, remote, keyboard, "
               "cell phone, microwave, oven, toaster, sink, refrigerator, book, "
               "clock, vase, scissors, teddy bear, hair drier, toothbrush")

class_names2 = ("dog, eye, tongue, ear, leash")

def run_image(
        runner,
        input_image,
        max_num_boxes=100,
        score_thr=0.05,
        nms_thr=0.5,
        output_image="output.png",
):
    output_dir = "runs/detect"
    print("aa")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_image_path = os.path.join(output_dir, output_image)
    texts = [[t.strip()] for t in class_names.split(",")] + [[" "]]
    data_info = runner.pipeline(dict(img_id=0, img_path=input_image, texts=texts))

    data_batch = dict(
        inputs=data_info["inputs"].unsqueeze(0),
        data_samples=[data_info["data_samples"]],
    )

    with autocast(enabled=False), torch.no_grad():
        output = runner.model.test_step(data_batch)[0]
        runner.model.class_names = texts
        pred_instances = output.pred_instances

    # nms
    keep_idxs = nms(pred_instances.bboxes, pred_instances.scores, iou_threshold=nms_thr)
    pred_instances = pred_instances[keep_idxs]
    pred_instances = pred_instances[pred_instances.scores.float() > score_thr]

    if len(pred_instances.scores) > max_num_boxes:
        indices = pred_instances.scores.float().topk(max_num_boxes)[1]
        pred_instances = pred_instances[indices]
    output.pred_instances = pred_instances

    # predictions
    pred_instances = pred_instances.cpu().numpy()

    if 'masks' in pred_instances:
        masks = pred_instances['masks']
    else:
        masks = None

    detections = sv.Detections(
        xyxy=pred_instances['bboxes'],
        class_id=pred_instances['labels'],
        confidence=pred_instances['scores']
    )

img = run_image(runner, "dog.jpeg")
sv.plot_image(img)
