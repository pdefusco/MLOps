import tensorflow as tf
import cdsw, numpy

model = load_model('my_model.h5')

@cdsw.model_metrics
def predict(json):
  
  y_pred = model.predict(json)
  
  # Track inputs
  cdsw.track_metric("prediction", y_pred)
  
  return {"data": dict(json), "prediction": y_pred}

