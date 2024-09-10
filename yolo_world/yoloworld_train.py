from ultralytics import YOLOWorld

# Load a pretrained YOLOv8s-worldv2 model
# model = YOLOWorld("./yolo_world/pre_trained_model/yolov8s-worldv2.pt")
model = YOLOWorld('../yolo_world/model_jmk_2.pt')


# Train the model on the COCO8 example dataset for 100 epochs
results = model.train(data="../custom_coco.yaml", epochs=60, imgsz=640)

# Run inference with the YOLOv8n model on the 'bus.jpg' image
# results = model("path/to/bus.jpg")
model.save('./third_train_3_from_model_jmk_and_pic2.pt')