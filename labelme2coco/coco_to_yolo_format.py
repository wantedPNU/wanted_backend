import json
import os

# 경로 설정
coco_json_path = './output/annotations.json'
output_dir = './labels/'

# COCO 주석 파일 로드
with open(coco_json_path, 'r') as f:
    coco_data = json.load(f)

# 출력 디렉토리 생성
os.makedirs(output_dir, exist_ok=True)

# 라벨 매핑 생성
categories = {cat['id']: cat['name'] for cat in coco_data['categories']}

# 이미지 정보와 크기 정보를 추출
image_info = {img['id']: (img['file_name'], img['width'], img['height']) for img in coco_data['images']}

# 이미지별 YOLO 포맷 주석 파일 생성
for image in coco_data['images']:
    image_id = image['id']
    file_name, img_width, img_height = image_info[image_id]
    annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_id]
    
    # YOLO 주석 파일 생성
    yolo_file = os.path.join(output_dir, file_name.replace('.jpg', '.txt'))
    with open(yolo_file, 'w') as f:
        for ann in annotations:
            category_id = ann['category_id']
            bbox = ann['bbox']
            # COCO bbox를 YOLO 포맷으로 변환
            x_center = bbox[0] + bbox[2] / 2
            y_center = bbox[1] + bbox[3] / 2
            width = bbox[2]
            height = bbox[3]
            x_center /= img_width
            y_center /= img_height
            width /= img_width
            height /= img_height
            # 파일에 기록
            f.write(f"{category_id} {x_center} {y_center} {width} {height}\n")
