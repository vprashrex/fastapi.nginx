import cv2
import numpy as np
import onnxruntime
from PIL import Image

class BGRemove:

    def resize_long(self,im, long_size=224, interpolation=cv2.INTER_LINEAR):
        value = max(im.shape[0], im.shape[1])
        scale = float(long_size) / float(value)
        resized_width = int(round(im.shape[1] * scale))
        resized_height = int(round(im.shape[0] * scale))

        im = cv2.resize(im, (resized_width, resized_height),
                        interpolation=interpolation)
        return im

    def process_original_im(self,im):
        im_h,im_w = im.shape[:2]
        if max(im_h,im_w) < 1024 or min(im_h,im_w):
            if im_w >= im_h:
                im_rh = 1024
                im_rw = int(im_w/im_h * 1024)
            elif im_w < im_h:
                im_rw = 1024
                im_rh = int(im_h/im_w * 1024)
        else:
            im_rh = im_h
            im_rw = im_w
        
        im = cv2.resize(im,(im_rw,im_rh),cv2.INTER_AREA)
        return im
    
    def preprocess(self, im):
        self.original_im = self.process_original_im(im)
        self.height,self.width = self.original_im.shape[:2]
        im = self.resize_long(im,768)
        im = cv2.resize(im,(512,512), interpolation=cv2.INTER_LINEAR)
        im = (im-127.5)/127.5
        im = np.transpose(im)
        im = np.swapaxes(im, 1, 2)
        im = np.expand_dims(im, axis=0).astype('float32')
        return im

    def postprocess(self,mask_data):
        mask_data = (np.squeeze(mask_data[0]))
        matte = np.dstack([mask_data]*4)
        rgba_img = cv2.cvtColor(self.original_im,cv2.COLOR_RGB2RGBA)
        bg_s = np.full(rgba_img.shape,(0,0,0,0),dtype=np.uint8)
        matte = cv2.resize(matte,(self.width,self.height),cv2.INTER_AREA)
        res = matte * rgba_img + (1-matte) * bg_s
        return res

    def image(self,im):        
        im = self.preprocess(im)
        session = onnxruntime.InferenceSession('pic_ai.onnx', None)
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        result = session.run([output_name], {input_name: im})
        result = self.postprocess(result)
        return result


if __name__ == '__main__':
    r = BGRemove()
    im = cv2.imread('1.jpg')
    #im = Image.open('1.jpg')
    res = r.image(im)
    cv2.imwrite('result.png',res)