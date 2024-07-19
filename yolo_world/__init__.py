import os
import cv2
import supervision as sv
from tqdm import tqdm
from inference.models.yolo_world.yolo_world import YOLOWorld
from googletrans import Translator

# 경로 설정
HOME = os.getcwd()
print(HOME)

# 모델 설정
model = YOLOWorld(model_id="yolo_world/s")

# 번역기 객체 생성
translator = Translator()

# 변환 함수
def translate_to_korean(english_text):
    translation = translator.translate(english_text, src='ko', dest='en')
    return translation.text

classes = [translate_to_korean("노란색 바지를 입은 남자")]
print(translate_to_korean("노란색 바지를 입은 남자"))
model.set_classes(classes)

# 비디오 경로 설정
SOURCE_VIDEO_PATH = os.path.join(HOME, "blue_person.mp4")
TARGET_VIDEO_PATH = os.path.join(HOME, "yellow_result3.mp4")

# 비디오 프레임 생성
frame_generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)
video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)

width, height = video_info.resolution_wh
frame_area = width * height

BOUNDING_BOX_ANNOTATOR = sv.BoundingBoxAnnotator(thickness=1)
LABEL_ANNOTATOR = sv.LabelAnnotator(text_thickness=2, text_scale=0.5, text_color=sv.Color.BLACK)

# 비디오 처리 및 주석 추가
with sv.VideoSink(target_path=TARGET_VIDEO_PATH, video_info=video_info) as sink:
    for frame in tqdm(frame_generator, total=video_info.total_frames):
        results = model.infer(frame, confidence=0.002)
        detections = sv.Detections.from_inference(results).with_nms(threshold=0.1)
        detections = detections[(detections.area / frame_area) < 0.10]

        annotated_frame = frame.copy()
        annotated_frame = BOUNDING_BOX_ANNOTATOR.annotate(annotated_frame, detections)
        annotated_frame = LABEL_ANNOTATOR.annotate(annotated_frame, detections)
        sink.write_frame(annotated_frame)

# 프레임으로 나누기
cap = cv2.VideoCapture(SOURCE_VIDEO_PATH)

# 프레임 간격 설정
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
interval = frame_rate * 3

# 모션 디텍션 설정
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=True)

count = 0
frame_count = 0

output_dir = os.path.join(HOME, "frames")
os.makedirs(output_dir, exist_ok=True)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 설정한 간격마다 프레임을 분석
    if frame_count % interval == 0:
        fgmask = fgbg.apply(frame)
        cv2.imwrite(os.path.join(output_dir, f"{count}.jpg"), frame)
        count += 1

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

print(count)

# 프레임 별로 inference
def process_and_annotate_image(cnt, source_image_path, model, classes, bounding_box_annotator, label_annotator, confidence_threshold=0.2):
    if not os.path.exists(source_image_path):
        raise FileNotFoundError(f"Image file not found: {source_image_path}")

    image = cv2.imread(source_image_path)
    if image is None:
        raise ValueError(f"Failed to load image. Please check the file format and path: {source_image_path}")

    results = model.infer(image, confidence=confidence_threshold)
    detections = sv.Detections.from_inference(results)

    labels = [
        f"{classes[class_id]} {confidence:0.3f}"
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]

    annotated_image = image.copy()
    annotated_image = bounding_box_annotator.annotate(annotated_image, detections)
    annotated_image = label_annotator.annotate(annotated_image, detections, labels=labels)

    cv2.imwrite(os.path.join(output_dir, f"{cnt}_res.jpg"), annotated_image)

for i in range(count):
    process_and_annotate_image(i, os.path.join(output_dir, f"{i}.jpg"), model, classes, BOUNDING_BOX_ANNOTATOR, LABEL_ANNOTATOR)
