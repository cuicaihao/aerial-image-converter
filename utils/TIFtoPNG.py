from osgeo import gdal

in_rgb_img_path = "RGB/kitsap11.tif"
in_gt_img_path = "GT/kitsap11.tif"

out_rgb_img_path = "PNG/RGB.png"
out_gt_img_path = "PNG/GT.png"


def tif2png(input, output):
    from osgeo import gdal
    driver = gdal.GetDriverByName('PNG')
    ds = gdal.Open(input)
    dst_ds = driver.CreateCopy(output, ds)
    # print(f"Input : {input}")
    # print(f"output: {output}")
    return dst_ds


if __name__ == '__main__':
    # print("Convert tif image to png with gdal:")
    tif2png(in_rgb_img_path, out_rgb_img_path)
    tif2png(in_gt_img_path, out_gt_img_path)
    # print("Done")
