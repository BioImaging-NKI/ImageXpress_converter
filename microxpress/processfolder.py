import logging
from pathlib import Path

import numpy as np
from tifffile import TiffFile, imwrite


def processfolder(pth_in, pth_out=None):
    logging.info(f"pth_in = {pth_in}")
    logging.info(f"pth_out = {pth_out}")
    if not pth_in.is_dir():
        logging.error(f'Input path {pth_in} is not a directory')
    if pth_out is None:
        pth_out = Path(pth_in, 'Output')
    tifs = [x for x in pth_in.glob('**\*.tif')]
    if len(tifs) == 0:
        logging.error(f"found {len(tifs)} tiffiles")
    else:
        logging.info(f"found {len(tifs)} tiffiles")

    tifsets = {}
    for tif in tifs:
        tif_ref = TiffFile(tif)
        if tif_ref.metaseries_metadata['Description'] == 'thumbnail image':
            continue
        stage_label = [x.strip() for x in tif_ref.metaseries_metadata['PlaneInfo']['stage-label'].split(sep=':')]
        stage_label = (stage_label[0], stage_label[1])
        timepoint = 1
        if 'Timepoint' in tif_ref.metaseries_metadata['PlaneInfo'].keys():
            timepoint = tif_ref.metaseries_metadata['PlaneInfo']['Timepoint']
        tif_info = {'pth': tif,
                'timepoint': timepoint,
                'image-name': tif_ref.metaseries_metadata['PlaneInfo']['image-name'],
                'spatial-calibration-x': tif_ref.metaseries_metadata['PlaneInfo']['spatial-calibration-x'],
                'spatial-calibration-y': tif_ref.metaseries_metadata['PlaneInfo']['spatial-calibration-y']}
        if stage_label in tifsets.keys():
            tifsets[stage_label].append(tif_info)
        else:
            tifsets[stage_label] = [tif_info]
        tif_ref.close()

    for tifset in tifsets:
        timepoints = list(set([x['timepoint'] for x in tifsets[tifset]]))
        image_names = list(set([x['image-name'] for x in tifsets[tifset]]))
        pixelSizeX = list(set([x['spatial-calibration-x'] for x in tifsets[tifset]]))
        pixelSizeY = list(set([x['spatial-calibration-y'] for x in tifsets[tifset]]))
        if len(pixelSizeX) > 1:
            logging.error('Warning! Pixel sizes of images not equal.')
            continue
        images = [[None] * len(image_names) for _ in range(len(timepoints))]
        for tif in tifsets[tifset]:
            tif_ref = TiffFile(tif['pth'])
            # stage_position_x = tif_ref.metaseries_metadata['PlaneInfo']['stage-position-x']
            # stage_position_y = tif_ref.metaseries_metadata['PlaneInfo']['stage-position-y']
            idx_t = timepoints.index(timepoint)
            idx_c = image_names.index(tif_ref.metaseries_metadata['PlaneInfo']['image-name'])
            images[idx_t][idx_c] = tif_ref.pages[0].asarray()
        data = np.stack(images)
        filename = f"{' '.join(tifset)}.tif"
        outpath = Path(pth_out, filename)
        outpath.parent.mkdir(exist_ok=True)
        logging.info(f"Saving to: {outpath}")
        metadata = {
            'axes': 'TCYX',
            'unit': 'um',
            'Channel': {'Name': [image_names[0], image_names[1]]},
            'PhysicalSizeXUnit': 'um',
            'PhysicalSizeYUnit': 'um'
        }
        imwrite(
            outpath,
            data,
            imagej=True,
            resolution=(1 / pixelSizeX[0], 1 / pixelSizeY[0]),
            metadata=metadata
        )