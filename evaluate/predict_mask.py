import os
from glob import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from segment_anything import sam_evimg_model_registry,SamAutomaticMaskGenerator
from segment_anything.utils.mask_postprocess import *
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
device = "cuda"


dataset = "RGBE_SEG"
encoder_checkpoint =".../checkpoints/rgbe_encoder.pth"
decoder_checkpoint =".../pretrained/sam_vit_b.pth"
model_type = "vit_b"


sam = sam_evimg_model_registry[model_type](input_signal="evimg",
                                           encoder_checkpoint=encoder_checkpoint,
                                           decoder_checkpoint=decoder_checkpoint)
sam.to(device=device)
mask_generator = SamAutomaticMaskGenerator(sam,
                                           points_per_side=64,
                                           pred_iou_thresh=0.75,
                                           stability_score_thresh=0.75,
                                           crop_n_layers=0,
                                           crop_nms_thresh= 0.7,
                                           crop_n_points_downscale_factor=1,
                                           min_mask_region_area=900,
                                           output_mode = "binary_mask",)

evimg_path = "..."
save_path = "..."
evimg = cv2.imread(evimg_path)
evimg = cv2.cvtColor(evimg, cv2.COLOR_BGR2RGB)
masks = mask_generator.generate(evimg)
masks = remove_small_mask(masks)
masks = remove_repeat_mask(masks)
mask_image = obtain_mask_image(masks) * 255
mask_image = mask_image.astype(np.uint8)
cv2.imwrite(save_path, mask_image)s
