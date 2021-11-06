import pandas as pd
import tensorflow as tf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from helpers import plot_decision_boundary


spark = SparkSession\
    .builder\
    .appName("PythonSQL")\
    .config("spark.hadoop.fs.s3a.s3guard.ddb.region","us-east-2")\
    .config("spark.yarn.access.hadoopFileSystems","s3a://gd01-uat2/")\
    .getOrCreate()

sparkDF = spark.sql("SELECT * FROM DEFAULT.circles")

df = sparkDF.toPandas()

# Split data into train and test sets
X_train, y_train = df[:800], df[:800] # 80% of the data for the training set
X_test, y_test = df[800:], df[800:] # 20% of the data for the test set

model = tf.keras.models.load_model('models/my_model.h5')

# Fit the model
history = model.fit(X_train, y_train, epochs=25)

# Evaluate our model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Model loss on the test set: {loss}")
print(f"Model accuracy on the test set: {100*accuracy:.2f}%")

# Plot the decision boundaries for the training and test sets
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Train")
helpers.plot_decision_boundary(model, X=X_train, y=y_train)
plt.subplot(1, 2, 2)
plt.title("Test")
helpers.splot_decision_boundary(model, X=X_test, y=y_test)
plt.show()

# You can access the information in the history variable using the .history attribute
pd.DataFrame(history.history)

# Plot the loss curves
pd.DataFrame(history.history).plot()
plt.title("Model training curves")


#model.save('my_model.h5')

