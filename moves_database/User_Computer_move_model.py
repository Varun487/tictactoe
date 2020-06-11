import keras
import pandas as pd
import numpy as np

# Loading the training data
X = pd.read_csv('moves_data/Training_set_User_Computer_Move_encoding.csv')
X = X.loc[:, 'User_Move_1_encoding_1':'User_Move_4_encoding_9']
# print(X.loc[:, 'User_Move_1_encoding_1':'User_Move_4_encoding_9'])

# Loading training data
y = pd.read_csv('moves_data/Training_set_User_Computer_Move_encoding.csv')
y = y.loc[:, 'Computer_Response_encoding_1':'Computer_Response_encoding_9']
# print(y.loc[:, 'Computer_Response_encoding_1':'Computer_Response_encoding_9'])

# Building the model
inputs = keras.Input(shape=(57,))
x = keras.layers.Dense(100, activation='relu')(inputs)
x = keras.layers.Dense(100, activation='relu')(x)
outputs = keras.layers.Dense(9, activation='softmax')(x)

# compiling and training the model
model = keras.Model(inputs, outputs)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=70, batch_size=30)

# evaluating the model on the training data, as there is no test or dev set
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

# serialize model to YAML
model_yaml = model.to_yaml()
with open("User_Computer_move_model_weights.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
# serialize weights to HDF5
model.save_weights("User_Computer_move_model_weights.h5")
print("Saved model to disk")

# load YAML and create model
yaml_file = open('User_Computer_move_model_weights.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = keras.models.model_from_yaml(loaded_model_yaml)

# load weights into new model
loaded_model.load_weights("User_Computer_move_model_weights.h5")
print("Loaded model from disk")

loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

_, accuracy = loaded_model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

# running for a single input
Xnew = np.array([[1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]])
ynew = model.predict(Xnew)
ynew = list(map(lambda num: int(round(num)), ynew[0]))

# 0	 0	0	0	1	0	0	0	0
# show the inputs and predicted outputs
print("X={}\nPredicted={}".format(Xnew, ynew))
