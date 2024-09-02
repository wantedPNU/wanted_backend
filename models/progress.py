class ProgressValue():
    son: int
    mom: int
    value : float

    def __init__(self, son, mom):
        self.son = son
        self.mom = mom #todo : vulnerable
        self.value = son/mom 
    

    def update_progress_value(self, son: float, mom: int):
        self.value = son/mom        
