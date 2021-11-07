import tensorflow as tf
import cdsw, numpy

model = tf.keras.models.load_model('models/my_model.h5')

@cdsw.model_metrics
def predict(json):
  
  request = np.array(jsonin["vals"]).reshape(-1,2)
  
  y_pred = model.predict(request)
  
  # Track inputs
  cdsw.track_metric("prediction", y_pred)
  
  return {"data": dict(json), "prediction": y_pred}

