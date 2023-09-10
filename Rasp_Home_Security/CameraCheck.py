import cv2

def check_camera(index):
    '''Try to open the camera at the given index. 
       Return True if successful, otherwise return False.'''
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return False
    cap.release()
    return True

def available_cameras(max_index=10):
    '''Check and return available camera indices up to max_index.'''
    return [i for i in range(max_index) if check_camera(i)]

cams = available_cameras()
print(f"Available camera indices: {cams}")
