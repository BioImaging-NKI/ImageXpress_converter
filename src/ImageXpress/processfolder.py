import json
import logging
import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import numpy as np
from tifffile import TiffFile, imwrite, RESUNIT


# custom json encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        if isinstance(obj, datetime.datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def processfolder(pth_in, pth_out=None):
    logging.info(f"pth_in = {pth_in}")
    logging.info(f"pth_out = {pth_out}")
    if not pth_in.is_dir():
        logging.error(f"Input path {pth_in} is not a directory")
    if pth_out is None:
        pth_out = Path(pth_in, "Output")
    tifs = [x for x in pth_in.glob(r"**\*.tif")]
    if len(tifs) == 0:
        logging.error(f"found {len(tifs)} tiffiles")
    else:
        logging.info(f"found {len(tifs)} tiffiles")

    tifsets = {}
    for tif in tifs:
        tif_ref = TiffFile(tif)
        if tif_ref.metaseries_metadata["Description"] == "thumbnail image":
            continue
        stage_label = [
            x.strip()
            for x in tif_ref.metaseries_metadata["PlaneInfo"]["stage-label"].split(
                sep=":"
            )
        ]
        stage_label = (stage_label[0], stage_label[1])
        if "Camera Error" in tif_ref.metaseries_metadata["PlaneInfo"].keys():
            error_val = tif_ref.metaseries_metadata["PlaneInfo"]["Camera Error"]
            logging.info(
                f"StageLabel {stage_label} had a Camera Error: {error_val}. Skipping."
            )
            continue
        timepoint = 1
        if "Timepoint" in tif_ref.metaseries_metadata["PlaneInfo"].keys():
            timepoint = tif_ref.metaseries_metadata["PlaneInfo"]["Timepoint"]
        tif_info = {
            "pth": tif,
            "timepoint": timepoint,
            "image-name": tif_ref.metaseries_metadata["PlaneInfo"]["image-name"],
            "spatial-calibration-x": tif_ref.metaseries_metadata["PlaneInfo"][
                "spatial-calibration-x"
            ],
            "spatial-calibration-y": tif_ref.metaseries_metadata["PlaneInfo"][
                "spatial-calibration-y"
            ],
            "metadata": {
                "Info": json.dumps(tif_ref.metaseries_metadata, cls=CustomJSONEncoder)
            },
        }
        if stage_label in tifsets.keys():
            tifsets[stage_label].append(tif_info)
        else:
            tifsets[stage_label] = [tif_info]
        tif_ref.close()

    for tifset in tifsets:
        logging.critical(f"Running {tifset} with {len(tifsets[tifset])} files")
        timepoints = list(set([x["timepoint"] for x in tifsets[tifset]]))
        image_names = list(set([x["image-name"] for x in tifsets[tifset]]))
        image_names.sort()
        pixelSizeX = list(set([x["spatial-calibration-x"] for x in tifsets[tifset]]))
        pixelSizeY = list(set([x["spatial-calibration-y"] for x in tifsets[tifset]]))
        if len(pixelSizeX) > 1:
            logging.error("Warning! Pixel sizes of images not equal.")
            continue
        images = [[None] * len(image_names) for _ in range(len(timepoints))]
        metadata = None
        for tif in tifsets[tifset]:
            tif_ref = TiffFile(tif["pth"])
            # stage_position_x = tif_ref.metaseries_metadata['PlaneInfo']['stage-position-x']
            # stage_position_y = tif_ref.metaseries_metadata['PlaneInfo']['stage-position-y']
            idx_t = timepoints.index(tif["timepoint"])
            idx_c = image_names.index(tif["image-name"])
            logging.info(f"Found file {tif['pth'].stem} ; t = {idx_t} ; c = {idx_c}")
            images[idx_t][idx_c] = tif_ref.pages[0].asarray()
            metadata = tif["metadata"]
        # to do: add ImageJ metadata, including pixel size and z-spacing
        data = np.stack(images)
        filename = f"{' '.join(tifset)}.tif"
        outpath = Path(pth_out, filename)
        outpath.parent.mkdir(exist_ok=True)
        logging.info(f"Saving to: {outpath}")
        imwrite(
            outpath,
            data,
            imagej=True,
            resolution=(1 / pixelSizeX[0], 1 / pixelSizeY[0]),
            resolutionunit=RESUNIT.MICROMETER,
            metadata=metadata,
        )
