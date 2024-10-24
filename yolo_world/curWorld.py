import os
import cv2
from ultralytics import YOLOWorld
import translators as ts
from yolo_world import progress_value,detected_video_list
import heapq
import torch

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
        
    model = YOLOWorld('yolo_world/model.pt') #this        
    model.set_classes(inference_setting.classes)
        
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

async def extract_frames(video_path, frame_interval, file_name):
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

async def process_and_annotate_image(cnt,input_dir,model,classes,output_dir,inference_setting:InferenceSettings,file_name, resultQ):
            
    results = model.predict(input_dir,conf = inference_setting.score_threshold)    
    
    image = cv2.imread(input_dir)
    if image is None:
        raise ValueError(f"Failed to load image. Please check the file format and path: {input_dir}")

    detections = results[0].boxes
    
    print("진행율 : " , progress_value.get_progress_value())
            
    # 감지된 객체가 있는 경우에만 저장
    if len(detections) > 0:      
        print("라벨 id: " , detections.cls)  
        print("라벨 conf : " , detections.conf)
        max_conf = torch.max(detections.conf)
        heapq.heappush(resultQ, (-max_conf, results[0], cnt, file_name))
        
        # @todo 
        # case (입력 쿼리가 detections에서 모두 일치한다(있다). -> 저장)
        # case (입력 쿼리가 detection에서 하나만 일치한다(있다) -> 저장)
        # case (입력 쿼리가 detection에서 일치 하지 않는다. -> 저장 x or zip 파일로는 제공)
        # results[0].save(os.path.join(output_dir, f"{file_name[0:-4]}의 {cnt}번째 프레임 결과.jpg"))
        # @todo
        # 발견된 동영상의 제목을 위치 정보를 가져와서 저장
        # 위치 정보를 map api를 이용해서 표시. 
        # 위치 정보 주변 가게, 경찰서 전화번호 list up.
    
    image = cv2.imread(input_dir)
    if image is None:
        raise ValueError(f"Failed to load image. Please check the file format and path: {input_dir}")
           




async def run_inference_on_video(video_path, model, inference_setting: InferenceSettings, file_name, resultQ):
    """비디오에 대해 추론을 실행"""
    # 추출된 프레임 수
    count = await extract_frames(video_path, inference_setting.frame_interval, file_name)
    # count = get_frames_count_of_video_file(video_path, inference_setting.frame_interval)
    input_dir = os.path.join(os.getcwd(), "frames")
    output_dir = os.path.join(os.getcwd(), "frames")    
    # count = 2
    for i in range(count):
        await process_and_annotate_image(i, os.path.join(input_dir, f"{file_name[0:-4]}의 {i}번째 프레임.jpg"), model, inference_setting.classes,output_dir, inference_setting, file_name, resultQ)
        progress_value.increase_progress_son()
        # print(progress_value.get_progress_value())

async def run_inference(inference_settings: InferenceSettings):
    inference_setting = InferenceSettings()

    model = initialize_model(inference_settings)      

    inference_setting.update_settings(score_threshold = inference_settings.score_threshold, frame_interval = inference_settings.frame_interval)
    inference_setting.update_query(inference_settings.classes, True)
    
    # dir_name = "sample_test_backup"
    files_and_dirs = os.listdir("./yolo_world/input_video/")
    file_count = len([f for f in files_and_dirs if os.path.isfile(os.path.join("./yolo_world/input_video/", f))])
    print(file_count)
    file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join("./yolo_world/input_video/", f))]
    print(file_names)
        
    model.set_classes(inference_setting.classes)    

    print("setted intiial model")
    detected_video_list.reset_videos()
        
    total_frame_count = 0
    for file_name in file_names:    
        # 비디오에 대해 추론 실행
        total_frame_count += get_frames_count(os.path.join(os.getcwd(), f"./yolo_world/input_video/{file_name}"),inference_setting.frame_interval)
    
    progress_value.update_progress_mom(total_frame_count)
    
    resultQ = []
    for file_name in file_names:    
        # 비디오에 대해 추론 실행        
        print(detected_video_list.get_all_videos())
        await run_inference_on_video(os.path.join(os.getcwd(), f"./yolo_world/input_video/{file_name}"), model, inference_setting, file_name, resultQ)

    score_rank = 0
    while resultQ:
    # 가장 높은 confidence 값을 가진 results[0]을 꺼냄
        max_conf, result, frame_cnt, result_name = heapq.heappop(resultQ)
        score_rank += 1
        print(score_rank)

        result.save(os.path.join(os.path.join(os.getcwd(), "frames"), f"{result_name[0:-4]}의 {frame_cnt}번째 프레임 결과{score_rank}.jpg"))
        detected_video_list.add_video(result_name,f"{result_name[0:-4]}의 {frame_cnt}번째 프레임 결과{score_rank}.jpg")