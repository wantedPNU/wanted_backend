#divide the video.mp4 into frames at samples
#process the image frame and annotate and save at frames


#main : load the model, divide and save frame, process and annotate and save the frame


#module test : process and annotate가 되는지 모름 save는 잘됨.
#process and annotate잘됨, save도 잘됨
# threshold값 설정을 못건드려봄
# 이제 구현 들어가면 됨.


import os
import cv2
import supervision as sv
# from models.InferenceSettings import InferenceSettings
from tqdm import tqdm
from ultralytics import YOLO,YOLOWorld
import translators as ts
from yolo_world import progress_value

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
   
def initialize_model(inference_setting:InferenceSettings):
    
    # model = YOLOWorld('yolov8x-worldv2.pt')        
    # model = YOLOWorld('model_for_white_shirt.pt')
    model = YOLOWorld('model_jmk_2.pt')
    model.set_classes(inference_setting.classes)
    
    # result = model.predict()
    # first = result[0].boxes
    
    return model

def set_inference(score_threshold: float, frame_interval: int, inference_setting: InferenceSettings):
    """추론 설정 업데이트"""
    inference_setting.update_settings(score_threshold, frame_interval)
    print(f"Updated score_threshold: {inference_setting.score_threshold}")
    print(f"Updated frame_interval: {inference_setting.frame_interval}")

def get_frames_count(video_path, frame_interval):
    """비디오에서 프레임을 간격마다 추출하여 저장하지 않고, 총 이미지 개수를 반환"""
    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    interval = frame_rate * frame_interval

    count = 0
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            count += 1

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    return count  # 총 이미지 개수를 반환

def extract_frames(video_path, frame_interval, file_name):
    """비디오에서 프레임을 간격마다 추출하여 저장"""
    cap = cv2.VideoCapture(video_path)
    print(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    interval = frame_rate * frame_interval
    
    fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=True)

    count = 0
    frame_count = 0

    output_dir = os.path.join(os.getcwd(), "frames")
    os.makedirs(output_dir, exist_ok=True)
    
    while cap.isOpened():        
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

def progress_test():
    update_son = progress_value.get_progress_son() + 1
    progress_value.update_progress_son(update_son)
    updated_value = progress_value.get_progress_value()
    print(updated_value)


def process_and_annotate_image(cnt,input_dir,model,classes,output_dir,inference_setting:InferenceSettings,file_name):
        
    
    results = model.predict(input_dir,conf = inference_setting.score_threshold)
    
    
    image = cv2.imread(input_dir)
    if image is None:
        raise ValueError(f"Failed to load image. Please check the file format and path: {input_dir}")

    detections = results[0].boxes
    
    print(progress_value.get_progress_mom())
    
    # 감지된 객체가 있는 경우에만 저장
    if len(detections) > 0:        
        results[0].save(os.path.join(output_dir, f"{file_name[0:-4]}의 {cnt}번째 프레임 결과.jpg"))
    
    image = cv2.imread(input_dir)
    if image is None:
        raise ValueError(f"Failed to load image. Please check the file format and path: {input_dir}")
           




def run_inference_on_video(video_path, model, inference_setting: InferenceSettings, file_name):
    """비디오에 대해 추론을 실행"""
    # 추출된 프레임 수
    count = extract_frames(video_path, inference_setting.frame_interval, file_name)
    # count = get_frames_count_of_video_file(video_path, inference_setting.frame_interval)
    input_dir = os.path.join(os.getcwd(), "frames")
    output_dir = os.path.join(os.getcwd(), "frames")    
        
    for i in range(count):
        process_and_annotate_image(i, os.path.join(input_dir, f"{file_name[0:-4]}의 {i}번째 프레임.jpg"), model, inference_setting.classes,output_dir, inference_setting, file_name)
        progress_value.increase_progress_son()
        print(progress_value.get_progress_value())

def run_inference(inference_settings: InferenceSettings):
    inference_setting = InferenceSettings()

    model = initialize_model(inference_settings)
    
    # model.set_classes(inference_setting.classes)        
    # model.save("custom_yolov8s.pt")
    # model = YOLOWorld("custom_yolov8s.pt")

    inference_setting.update_settings(score_threshold = inference_settings.score_threshold, frame_interval = inference_settings.frame_interval)
    inference_setting.update_query(inference_settings.classes, True)
    files_and_dirs = os.listdir("./sample_test_backup/")
    file_count = len([f for f in files_and_dirs if os.path.isfile(os.path.join("./sample_test_backup/", f))])
    print(file_count)
    file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join("./sample_test_backup/", f))]
    print(file_names)
        
    model.set_classes(inference_setting.classes)
    # model.save("custom_yolov8s.pt")
    # model = YOLOWorld("custom_yolov8s.pt")
    
    #테스트용 image.jpg run
    # results = model.predict("./test.jpg")
    # results[0].save("./frames/테스트용 image.jpg 결과")
    # output_dir = os.path.join(os.getcwd(), "frames")
    # results[0].save(os.path.join(output_dir, "test 결과.jpg"))
    # results[0].save("./test 결과.jpg")
    total_frame_count = 0
    for file_name in file_names:    
        # 비디오에 대해 추론 실행
        total_frame_count += get_frames_count(os.path.join(os.getcwd(), f"./sample_test_backup/{file_name}"),inference_setting.frame_interval)
    
    progress_value.update_progress_mom(total_frame_count)
    
    
    for file_name in file_names:    
        # 비디오에 대해 추론 실행
        run_inference_on_video(os.path.join(os.getcwd(), f"./sample_test_backup/{file_name}"), model, inference_setting, file_name)
    
# HOME = os.getcwd()
# model = initialize_model()
# os.system("rm -rf ./frames")
# video_file_name = "video.mp4"
# extract_frames(os.path.join(HOME,"./",video_file_name),3,video_file_name)

# BOUNDING_BOX_ANNOTATOR = sv.BoundingBoxAnnotator(thickness=1)
# LABEL_ANNOTATOR = sv.LabelAnnotator(text_thickness=2, text_scale=0.5, text_color=sv.Color.BLACK)

# # output_dir = os.path.join(os.getcwd(), "frames")
# input_dir = "./frames/video의 13번째 프레임.jpg"
# output_dir = os.path.join(HOME,f"frames/image_res.png")

# process_and_annotate_image(model,input_dir,output_dir)
# process_and_annotate_image(os.path.join(output_dir, f"{video_file_name[0:-4]}의 첫번째 프레임.jpg"),model)
# process_and_annotate_image(os.path.join(output_dir, f"{video_file_name[0:-4]}의 첫번째 프레임.jpg"), model,BOUNDING_BOX_ANNOTATOR, LABEL_ANNOTATOR, output_dir, video_file_name)