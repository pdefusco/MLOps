import tensorflow as tf
import cdsw 
import numpy as np
from json import JSONEncoder
import json

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

model = tf.keras.models.load_model('models/my_model.h5')

@cdsw.model_metrics
def predict(json_input):
  
  request = np.array(json_input["vals"]).reshape(-1,2)
  
  y_pred = model.predict(request)
  
  # Track inputs
  cdsw.track_metric("prediction", 1.*y_pred[0][0])
  
  pred= 1.*y_pred[0][0]
  return pred


predict({
  "vals": [
    1,
    2
  ]
})