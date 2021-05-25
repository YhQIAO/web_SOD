import torch
from torchvision import transforms
from torch.autograd import Variable

from matplotlib import pyplot as plt
import numpy as np

from skimage import transform
from skimage import io
from PIL import Image

from model import U2NETP

import os

def Rescale(image ,output_size=320):
    h, w = image.shape[:2]
    if isinstance(output_size, int):
        if h > w:
            new_h, new_w = output_size * h / w, output_size
        else:
            new_h, new_w = output_size, output_size * w / h
    else:
        new_h, new_w = output_size
    new_h, new_w = int(new_h), int(new_w)
    img = transform.resize(image, (output_size, output_size), mode='constant')
    return img


def ToTensor(image):
    tmpImg = np.zeros((image.shape[0], image.shape[1], 3))
    image = image / np.max(image) # 先归一化
    if image.shape[2] == 1:
        tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
        tmpImg[:, :, 1] = (image[:, :, 0] - 0.485) / 0.229
        tmpImg[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
    else:
        tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
        tmpImg[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
        tmpImg[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225
    tmpImg = tmpImg.transpose((2, 0, 1))
    return torch.from_numpy(tmpImg)

def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d-mi)/(ma-mi)
    return dn


def inference_and_save_mask(image_name):
    model_path = './saved_models/u2netp.pth'
    net = U2NETP(3, 1)
    net.load_state_dict(torch.load(model_path, map_location='cpu'))
    net.eval()

    IMAGE_PATH = 'static/images/'
    test_image_name = image_name
    test_image = io.imread(os.path.join(IMAGE_PATH, test_image_name))
    test_image_shape = test_image.shape

    resized_image = Rescale(test_image, 320)
    image_tensor = ToTensor(resized_image)
    inputs_test = image_tensor.unsqueeze(0)
    inputs_test = inputs_test.type(torch.FloatTensor)

    if torch.cuda.is_available():
        inputs_test = Variable(inputs_test.cuda())
    else:
        inputs_test = Variable(inputs_test)

    d1,d2,d3,d4,d5,d6,d7= net(inputs_test)
    pred = d1[:,0,:,:]
    pred = normPRED(pred)

    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray(predict_np * 255).convert('RGB')
    im = im.resize((test_image_shape[1],test_image_shape[0]),
                   resample=Image.BILINEAR)
    mask_name = image_name.split('/')[-1].split('.')[0]
    im.save('static/masks/' + mask_name + '.png')  # 保存mask

    # todo 保存object
    mask = Image.fromarray(predict_np)
    mask = mask.resize((test_image_shape[1],test_image_shape[0]),
                   resample=Image.BILINEAR)

    test_image[:,:,0] = (test_image[:,:,0].astype(float)*mask).astype(int)
    test_image[:, :, 1] = (test_image[:, :, 1].astype(float) * mask).astype(int)
    test_image[:, :, 2] = (test_image[:, :, 2].astype(float) * mask).astype(int)

    io.imsave('static/objects/' + mask_name + '.png', test_image)