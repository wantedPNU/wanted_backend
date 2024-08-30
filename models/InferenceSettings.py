
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