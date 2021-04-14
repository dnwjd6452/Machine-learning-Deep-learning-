from tensorflow.keras import *
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
import os

a = 0
b = 0
c = 0
result = 0
s = ""


def build_model(input_shape=(220, 200, 3)):
    pretrained = applications.VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    pretrained.trainable = False
    x = layers.Flatten()(pretrained.output)
    x = layers.Dense(2048, activation='relu')(x)
    x = layers.Dense(1024, activation='relu')(x)
    x = layers.Dense(3, activation='softmax')(x)
    model = models.Model(inputs=pretrained.input, outputs=x)
    model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(lr=1e-8), metrics=['acc'])
    model.summary()
    return model

def names_to_image(names):
    imgs = Image.open(names[0])
    newsize = (int(imgs.size[0] / 20), int(imgs.size[1] / 20))
    return list(map(lambda name: np.array(Image.open(name).resize(newsize).rotate(0)), names))


def get_image_names(base):
    return lambda x: list(map(lambda y: base + x + '/' + y, os.listdir(f'{base}{x}')))


def with_labels(image, label):
    return list(zip(image, [label] * len(image)))


def load_data(data_dir='./cnn/'):
    name_left, name_right, name_middle = tuple(map(get_image_names(data_dir), ['left', 'right', 'middle']))
    image_left, image_right, image_middle = tuple(map(names_to_image, [name_left, name_right, name_middle]))
    image_left, image_right, image_middle = with_labels(image_left, [1, 0, 0]), with_labels(image_right,
                                                                                            [0, 0, 1]), with_labels(
        image_middle, [0, 1, 0])
    image_all = image_left + image_right + image_middle
    random.seed(1234)
    random.shuffle(image_all)
    x = list(map(lambda x: x[0], image_all))
    y = list(map(lambda x: x[1], image_all))
    split = int(len(x) * 0.8)
    train_x = np.array(x[:split])
    train_y = np.array(y[:split])
    test_x = np.array(x[split:])
    test_y = np.array(y[split:])
    return train_x, train_y, test_x, test_y


data_directory = './cnn/'
train_x, train_y, test_x, test_y = load_data(data_directory)

load = False  # True 일시 가장 최근 모델 가져옴
train = True  # True 일시 트레이닝
if load:
    model_name = sorted(os.listdir("./models"))[-1]
model = models.load_model("./models/" + model_name) if (
        load and os.path.exists("./models/" + model_name)) else build_model(train_x.shape[1:])
model_path = "./models/" + '{epoch:02d}-{val_loss:.4f}.hdf5'
cb_checkpoint = callbacks.ModelCheckpoint(filepath=model_path, monitor='val_loss',
                                          verbose=1, save_best_only=False)

epochs = 100
batch_size = 32
if train:
    history = model.fit(x=train_x, y=train_y, validation_data=(test_x, test_y), batch_size=batch_size, epochs=epochs,
                        callbacks=[cb_checkpoint])

    y_vloss = history.history['val_loss']
    y_loss = history.history['loss']

    x_len = np.arange(len(y_loss))
    plt.plot(x_len, y_vloss, marker='.', c='red', label="Validation-set Loss")
    plt.plot(x_len, y_loss, marker='.', c='blue', label="Train-set Loss")

    plt.legend(loc='upper right')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('loss')

    y_vloss = history.history['val_acc']
    y_loss = history.history['acc']

    x_len = np.arange(len(y_loss))
    plt.plot(x_len, y_vloss, marker='.', c='red', label="Validation-set acc")
    plt.plot(x_len, y_loss, marker='.', c='blue', label="Train-set acc")

    plt.legend(loc='upper right')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('acc')

def test(image_path):
    model = models.load_model("./models/" + sorted(os.listdir("./models"))[-1])  # 모델로드
    label2string = {(1, 0, 0): 'right', (0, 0, 1): 'left', (0, 1, 0): 'middle'}  # 레이블을 스트링 형태로
    image = Image.open(image_path)
    image = image.resize((int(image.size[0] / 20), int(image.size[1] / 20)))
    image_array = np.expand_dims(np.array(image).astype(np.float32), axis=0)
    raw_pred = model.predict(image_array).squeeze()
    pred = [1 if x == max(raw_pred) else 0 for x in raw_pred]
    # plt.title(f"prediction:{label2string[tuple(pred)]}")
    # plt.imshow(np.array(image))
    # plt.savefig(f"./pred.png")

    print(label2string[tuple(pred)])
