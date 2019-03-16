import subclient as sc
import cv2
from keras.models import load_model,model_from_json
import numpy as np
json_file = open('model_out.json','r')
loaded_model_json =json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('model_weights.h5')
print('done loading')
while True:
    
        img = sc.client_thread(1)
        
        print(loaded_model.predict_classes(np.asarray([img]),batch_size = None))
        
        
    
