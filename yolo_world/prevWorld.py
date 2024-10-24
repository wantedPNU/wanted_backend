import os
import cv2
import supervision as sv
from tqdm import tqdm
from inference.models.yolo_world.yolo_world import YOLOWorld
import translators as ts

class InferenceSettings:
    def __init__(self, score_threshold: float = 0.1, frame_interval: int = 3):
        self.score_threshold = score_threshold
        self.frame_interval = frame_interval
        self.file_id = ""
        self.classes = ['init']

    def update_settings(self, score_threshold: float, frame_interval: int):
        self.score_threshold = score_threshold
        self.frame_interval = frame_interval

    def update_file_id(self, file_id: str):
        self.file_id = file_id

    def update_query(self, queries, flag):
        if flag:
            translated_queries = [f"person wearing {ts.translate_text(query)}" for query in queries]
        else:
            translated_queries = [f"{ts.translate_text(query)}" for query in queries]
            
        self.classes = translated_queries
        print(f"추가된 쿼리: {self.classes}")

    def get_settings(self):
        return {
            "score_threshold": self.score_threshold,
            "frame_interval": self.frame_interval
        }
    
def initialize_model(inference_settings, model_id="yolo_world/x"):
    """모델을 초기화하고, 추론 설정의 클래스와 연결"""
    model = YOLOWorld(model_id=model_id)
    model.set_classes(inference_settings.classes)
    return model

def extract_frames(video_path, frame_interval, file_name):
    """비디오에서 프레임을 간격마다 추출하여 저장"""
    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    interval = frame_rate * frame_interval

    fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=True)

    count = 0
    frame_count = 0

    output_dir = os.path.join(os.getcwd(), "frames")
    os.makedirs(output_dir, exist_ok=True)

    while cap.isOpened():
        # print(frame_rate)
        # print(frame_count)
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            fgmask = fgbg.apply(frame)
            cv2.imwrite(os.path.join(output_dir,  f"{file_name[0:-4]}의 {count}번째 프레임.jpg"), frame)
            count += 1

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    return count

def process_and_annotate_image(cnt, source_image_path, model, classes, bounding_box_annotator, label_annotator, output_dir, inference_setting: InferenceSettings, file_name):
    """이미지에 대해 추론을 수행하고 주석을 추가"""
    if not os.path.exists(source_image_path):
        raise FileNotFoundError(f"Image file not found: {source_image_path}")

    image = cv2.imread(source_image_path)
    if image is None:
        raise ValueError(f"Failed to load image. Please check the file format and path: {source_image_path}")

    results = model.infer(image, confidence=inference_setting.score_threshold)
    detections = sv.Detections.from_inference(results)

    if len(detections) > 0:
        labels = [
            f"{classes[class_id]} {confidence:0.3f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence)
        ]

        annotated_image = image.copy()
        annotated_image = bounding_box_annotator.annotate(annotated_image, detections)
        annotated_image = label_annotator.annotate(annotated_image, detections, labels=labels)
        print(classes)
        print(inference_setting.score_threshold)
        print(inference_setting.frame_interval)
        cv2.imwrite(os.path.join(output_dir, f"{file_name[0:-4]}의 {cnt}번째 프레임 결과.jpg"), annotated_image)

def run_inference_on_video(video_path, model, inference_setting: InferenceSettings, file_name):
    """비디오에 대해 추론을 실행"""
    # 추출된 프레임 수
    count = extract_frames(video_path, inference_setting.frame_interval, file_name)

    # 주석 추가 도구 설정
    BOUNDING_BOX_ANNOTATOR = sv.BoundingBoxAnnotator(thickness=1)
    LABEL_ANNOTATOR = sv.LabelAnnotator(text_thickness=2, text_scale=0.5, text_color=sv.Color.BLACK)

    output_dir = os.path.join(os.getcwd(), "frames")
    for i in range(count):
        process_and_annotate_image(i, os.path.join(output_dir, f"{file_name[0:-4]}의 {i}번째 프레임.jpg"), model, inference_setting.classes, BOUNDING_BOX_ANNOTATOR, LABEL_ANNOTATOR, output_dir, inference_setting, file_name)
        print(i)

def set_inference(score_threshold: float, frame_interval: int, inference_setting: InferenceSettings):
    """추론 설정 업데이트"""
    inference_setting.update_settings(score_threshold, frame_interval)
    print(f"Updated score_threshold: {inference_setting.score_threshold}")
    print(f"Updated frame_interval: {inference_setting.frame_interval}")

def run_inference(inference_settings: InferenceSettings):
    inference_setting = InferenceSettings()

    model = initialize_model(inference_settings)

    inference_setting.update_settings(score_threshold = inference_settings.score_threshold, frame_interval = inference_settings.frame_interval)
    inference_setting.update_query(inference_settings.classes, True)
    files_and_dirs = os.listdir("./samples/")
    file_count = len([f for f in files_and_dirs if os.path.isfile(os.path.join("./samples/", f))])
    print(file_count)
    file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join("./samples/", f))]
    print(file_names)
    for file_name in file_names:
        # 비디오에 대해 추론 실행
        run_inference_on_video(os.path.join(os.getcwd(), f"./samples/{file_name}"), model, inference_setting, file_name)
    
    # 비디오에 대해 추론 실행
        # run_inference_on_video(os.path.join(os.getcwd(), "./input_video.mp4"), model, inference_setting)



'''
# 경로 설정
HOME = os.getcwd()
print(HOME)

# 모델 설정
model = YOLOWorld(model_id="yolo_world/s")

# threshold 및 interval 설정
# inference_settings = InferenceSettings()
model.set_classes(inference_settings.classes)

# 비디오 경로 설정
# 이 비디오 경로를 inpue_video.mp4로 하면 될듯?? 
SOURCE_VIDEO_PATH = os.path.join(HOME, "./input_video.mp4")
# TARGET_VIDEO_PATH = os.path.join(HOME, "blue_result.mp4")

# # 비디오 프레임 생성
# frame_generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)
# video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)

# width, height = video_info.resolution_wh
# frame_area = width * height

BOUNDING_BOX_ANNOTATOR = sv.BoundingBoxAnnotator(thickness=1)
LABEL_ANNOTATOR = sv.LabelAnnotator(text_thickness=2, text_scale=0.5, text_color=sv.Color.BLACK)

# # 비디오 처리 및 주석 추가
# with sv.VideoSink(target_path=TARGET_VIDEO_PATH, video_info=video_info) as sink:
#     for frame in tqdm(frame_generator, total=video_info.total_frames):
#         results = model.infer(frame, confidence=0.2)
#         detections = sv.Detections.from_inference(results)
#         detections = detections[(detections.area / frame_area) < 0.10]

#         annotated_frame = frame.copy()
#         annotated_frame = BOUNDING_BOX_ANNOTATOR.annotate(annotated_frame, detections)
#         annotated_frame = LABEL_ANNOTATOR.annotate(annotated_frame, detections)
#         sink.write_frame(annotated_frame)

# 프레임으로 나누기
cap = cv2.VideoCapture(SOURCE_VIDEO_PATH)

# 프레임 간격 설정
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
interval = frame_rate * inference_settings.frame_interval

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
def process_and_annotate_image(cnt, source_image_path, model, classes, bounding_box_annotator, label_annotator):
    if not os.path.exists(source_image_path):
        raise FileNotFoundError(f"Image file not found: {source_image_path}")

    image = cv2.imread(source_image_path)
    if image is None:
        raise ValueError(f"Failed to load image. Please check the file format and path: {source_image_path}")

    results = model.infer(image, confidence=inference_settings.score_threshold)
    detections = sv.Detections.from_inference(results)

    labels = [
        f"{classes[class_id]} {confidence:0.3f}"
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]

    annotated_image = image.copy()
    annotated_image = bounding_box_annotator.annotate(annotated_image, detections)
    annotated_image = label_annotator.annotate(annotated_image, detections, labels=labels)
    print(classes)
    cv2.imwrite(os.path.join(output_dir, f"{cnt}_res.jpg"), annotated_image)
print(inference_settings.classes)
for i in range(count):
    process_and_annotate_image(i, os.path.join(output_dir, f"{i}.jpg"), model, inference_settings.classes, BOUNDING_BOX_ANNOTATOR, LABEL_ANNOTATOR)

def set_inference(score_threshold: float, frame_interval: int):
    inference_settings.update_settings(score_threshold, frame_interval)
    print(inference_settings.score_threshold)
    print(inference_settings.frame_interval)

def add_query(query: list[str]):
    inference_settings.update_query(query) '''