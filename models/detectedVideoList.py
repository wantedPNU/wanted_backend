class DetectedVideoList():    
    def __init__(self):
        self.frame_videos = {}  # frame을 key로, video를 value로 저장

    def reset_videos(self):
        self.frame_videos= {}

    def add_video(self, video_name: str, frame_name: str):
        """Adds a detected frame as the key and video name as the value."""
        self.frame_videos[frame_name] = video_name

    def get_video(self, frame_name):
        """Returns the video name associated with the frame name."""
        return self.frame_videos.get(frame_name, None)

    def get_all_frames(self):
        """Returns all frame names."""
        return list(self.frame_videos.keys())

    def get_all_videos(self):
        """Returns all video names."""
        return list(self.frame_videos.values())
