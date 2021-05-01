
import os
import sys
absolute_path=os.path.dirname(os.path.abspath(__file__))
absolute_model_path=os.path.dirname(os.path.abspath(__file__))
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
