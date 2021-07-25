# Resize and Preserve Aspect Ratio
import cv2


input_RGB_RAW = "PNG/RGB.png"
input_GT_RAW = "PNG/GT.png"

output_RGB_Resized = "PNG/1000x1000/RGB.png"
output_GT_Resized = "PNG/1000x1000/GT.png"


def resizePNG(input, output, scale_percent=20):
    ''' 20% percent of original size
    '''
    img = cv2.imread(input, cv2.IMREAD_UNCHANGED)
    # print('Original Dimensions : ', img.shape)

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    # INTER_NEAREST / INTER_AREA
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_NEAREST)

    # print('Resized Dimensions : ', resized.shape)

    # save image
    status = cv2.imwrite(output, resized)
    # print("Resized Image written to file-system : ", status)
    return status


if __name__ == '__main__':
    # print("Resize the PNG image with OpenCV:")
    resizePNG(input_RGB_RAW, output_RGB_Resized)
    resizePNG(input_GT_RAW, output_GT_Resized)
    # print("Done")
