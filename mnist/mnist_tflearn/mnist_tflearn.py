import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import tflearn.datasets.mnist as mnist

x_train,y_train ,x_test,y_test =mnist.load_data(one_hot=True)

x_train= x_train.reshape([-1,28,28,1])
x_test= x_test.reshape([-1,28,28,1])

convnet=input_data(shape=[None, 28, 28, 1],name='input')

convnet=conv_2d(convnet,32,2, activation='relu')
convnet=max_pool_2d(convnet, 2)

convnet=conv_2d(convnet,64, 2, activation='relu')
convnet=max_pool_2d(convnet, 2)

#for fully connected layer
convnet=fully_connected(convnet,1024, activation='relu')
convnet=dropout(convnet, 0.8)


#for output layer
convnet=fully_connected(convnet, 10, activation='softmax')
convnet=regression(convnet, optimizer='adam',learning_rate=0.001,loss='categorical_crossentropy',name='targets')

model=tflearn.DNN(convnet)


model.fit({'input': x_train}, {'targets': y_train}, n_epoch=10, validation_set=({'input': x_test}, {'targets': y_test}),
    snapshot_step=500, show_metric=True, run_id='mnist')

model.save('tflearn.model')

print(model.predict([x_test[1]]))
