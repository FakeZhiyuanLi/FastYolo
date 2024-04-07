from PIL import Image
import imgaug as ia
import imgaug.augmenters as iaa
import pybboxes
import numpy as np
import sys
import os

def YOLOtoVOC(boundingBox):
    converted = list(pybboxes.convert_bbox(boundingBox[1:5], from_type="yolo", to_type="voc", image_size=(640, 640)))
    return [boundingBox[0], converted[0], converted[1], converted[2], converted[3]]

def VOCtoYOLO(boundingBox):
    converted = list(pybboxes.convert_bbox(boundingBox[1:5], from_type="voc", to_type="yolo", image_size=(640, 640)))
    return [boundingBox[0], converted[0], converted[1], converted[2], converted[3]]

# seq = iaa.Sequential([
#     iaa.Multiply((1.2, 1.5)), # change brightness, doesn't affect BBs
#     iaa.Affine(
#         translate_px={"x": 40, "y": 60},
#         scale=(0.5, 0.7)
#     ) # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
# ])
# https://imgaug.readthedocs.io/en/latest/source/examples_basics.html
seq = iaa.Sequential([
    iaa.Fliplr(0.5), # horizontal flips
    iaa.Crop(percent=(0, 0.1)), # random crops
    # Small gaussian blur with random sigma between 0 and 0.5.
    # But we only blur about 50% of all images.
    iaa.Sometimes(
        0.5,
        iaa.GaussianBlur(sigma=(0, 0.5))
    ),
    # Strengthen or weaken the contrast in each image.
    iaa.LinearContrast((0.75, 1.5)),
    # Add gaussian noise.
    # For 50% of all images, we sample the noise once per pixel.
    # For the other 50% of all images, we sample the noise per pixel AND
    # channel. This can change the color (not only brightness) of the
    # pixels.
    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
    # Make some images brighter and some darker.
    # In 20% of all cases, we sample the multiplier once per channel,
    # which can end up changing the color of the images.
    iaa.Multiply((0.8, 1.2), per_channel=0.2),
    # Apply affine transformations to each image.
    # Scale/zoom them, translate/move them, rotate them and shear them.
    iaa.Affine(
        scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
        translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
        rotate=(-25, 25),
        shear=(-8, 8)
    )
], random_order=True)

def aug(pilImages, boundingBoxes, epochs):
    count = 0
    for j in range(epochs):
        classes = []
        tempImages = []
        for image in pilImages:
            tempImages.append(np.array(image))
        images = np.array(tempImages)
        boxes = []
        for box2d in boundingBoxes:
            tempBoxes = []
            for box in box2d:
                tempBoxes.append(YOLOtoVOC(box))
                classes.append(box[0])
            boxes.append(tempBoxes)
        for idx, image in enumerate(images):
            currBoxes = []
            for box in boxes[idx]:
                currBoxes.append(ia.BoundingBox(box[1], box[2], box[3], box[4], label=box[0]))
            bbs = ia.BoundingBoxesOnImage(currBoxes, shape=image.shape)

            image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
            labelOutputs = []
            for box in bbs_aug:
                yoloConvert = VOCtoYOLO([box.label, box.x1, box.y1, box.x2, box.y2])
                labelOutputs.append(yoloConvert)
            imageOutput = Image.fromarray(image_aug)

            if j <= epochs/2:
                imageOutput.save(f'/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1/edited/train/images/{count}.jpg')
                with open(f'/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1/edited/train/labels/{count}.txt', "w") as out:
                    for output in labelOutputs:
                        out.write(f"{output[0]} {output[1]} {output[2]} {output[3]} {output[4]} \n")
                count += 1
            else:
                imageOutput.save(f'/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1/edited/val/images/{count}.jpg')
                with open(f'/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1/edited/val/labels/{count}.txt', "w") as out:
                    for output in labelOutputs:
                        out.write(f"{output[0]} {output[1]} {output[2]} {output[3]} {output[4]} \n")
                count += 1

if __name__ == "__main__":
    print(YOLOtoVOC([0, 0.18515625, 0.2109375, 0.1296875, 0.175]))
    print(VOCtoYOLO([0, 77, 79, 160, 191]))