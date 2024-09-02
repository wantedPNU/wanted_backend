class ProgressValue():
    son: int
    mom: int
    value : float

    def __init__(self, son, mom):
        self.son = son
        self.mom = mom #todo : vulnerable
        self.value = son/mom 
    
    def get_progress_value(self):
        return self.value
    
    def get_progress_son(self):
        return self.son
    
    def increase_progress_son(self):
        self.son += 1
        self.value = self.son/self.mom

    def get_progress_mom(self):
        return self.mom
    

    def update_progress_mom(self, mom: float):
        self.mom = mom
        self.value = self.son/mom

    def update_progress_son(self, son: float):
        self.son = son      
        self.value = son/self.mom

    # def update_progress_value(self, son: float, mom: int):
    #     self.value = son/mom        
