# Resize and Preserve Aspect Ratio
import cv2

input_GT = "PNG/GT.png"
output_GT_invert = "PNG/GT_INV.png"


def invertBW(input, output):
    ''' 20% percent of original size
    '''
    image = cv2.imread(input, 0)
    print('Original Dimensions : ', image.shape)

    # resize image
    invert = cv2.bitwise_not(image)
    print('Resized Dimensions : ', invert.shape)

    # save image
    status = cv2.imwrite(output, invert)
    print("Inverted Image written to file-system : ", status)
    return status


if __name__ == '__main__':
    print("Resize the PNG image with OpenCV:")
    invertBW(input_GT, output_GT_invert)
    print("Done")
