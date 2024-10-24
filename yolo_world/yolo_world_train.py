from ultralytics import YOLOWorld

# Load a pretrained YOLOv8s-worldv2 model
model = YOLOWorld("./yolo_world/yolov8s-worldv2.pt")
# model = YOLOWorld('../yolo_world/third_train_b-4_from_jmk2.pt')

results = model.train(data="../data.yaml", epochs=200, imgsz=640)

# Run inference with the YOLOv8n model on the 'bus.jpg' image
model.save('./_10th_final_report_result4_1_epoch200.pt')

