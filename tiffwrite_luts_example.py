import numpy as np
import tifffile

# Create a random test image
im_3frame = np.random.randint(0, 255, size=(3, 150, 250), dtype=np.uint8)
# Intensity value range
val_range = np.arange(256, dtype=np.uint8)
# Gray LUT
lut_gray = np.stack([val_range, val_range, val_range])
# Red LUT
lut_red = np.zeros((3, 256), dtype=np.uint8)
lut_red[0, :] = val_range
# Green LUT
lut_green = np.zeros((3, 256), dtype=np.uint8)
lut_green[1, :] = val_range
# Create ijmetadata kwarg
ijmeta = {'LUTs': [lut_gray, lut_red, lut_green]}
# Save image
tifffile.imwrite(
    'C:\Temp\test.tif',
    im_rgb,
    imagej=True,
    metadata={'mode': 'composite'},
    ijmetadata=ijmeta,
)