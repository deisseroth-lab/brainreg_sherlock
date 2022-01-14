import argparse
import logging

import dask.array as da
import numpy as np
from dask_image.imread import imread
from scipy.ndimage import zoom
from skimage.transform import resize_local_mean, resize
from tifffile import imwrite


class DownsampleError(Exception):
    pass


def downsample(img, res_in, res_out, algo="brainreg"):
    if len(args.res_in) != 3:
        raise DownsampleError("res_in needs to have 3 values")

    if algo not in {"resize_local_mean", "brainreg"}:
        raise DownsampleError(f"Unknown downsample algorithm: {algo}")

    dtype_in = img.dtype
    shape_in = img.shape

    scale = np.array(res_in) / res_out
    shape_out = np.maximum(np.round(scale * shape_in), 1)
    shape_out = tuple(shape_out.astype(int))

    shape_partial = (1,) + shape_out[1:]

    # The dtype returned by scikit image using preserve_range=True and order=None.
    dtype_partial = np.float64
    if dtype_in == np.float16 or dtype_partial == np.float32:
        dtype_partial = np.float32

    if algo=="resize_local_mean":
        img = da.map_blocks(resize_local_mean,
                            img,
                            dtype=dtype_partial,
                            chunks=shape_partial,
                            meta=np.array((), dtype=dtype_partial),
                            output_shape=shape_partial,
                            preserve_range=True)
    elif algo=="brainreg":
        img = da.map_blocks(resize,
                            img,
                            dtype=dtype_partial,
                            chunks=shape_partial,
                            meta=np.array((), dtype=dtype_partial),
                            output_shape=shape_partial,
                            preserve_range=True,
                            mode="constant",
                            anti_aliasing=True)


    logging.info(f"Downsampling algo={algo} {shape_in} to {shape_out}: xy")
    img = img.compute()

    logging.info(f"Downsampling algo={algo} {shape_in} to {shape_out}: z")

    if algo=="resize_local_mean":
        img = resize_local_mean(img, output_shape=shape_out, preserve_range=True)
    elif algo=="brainreg":
        zoom_scale = shape_out[0] / shape_in[0]
        img = zoom(img, (zoom_scale, 1, 1), order=1)

    return img


if __name__ == '__main__':
    fmt = '%(asctime)s %(name)s:%(lineno)d %(levelname)s - %(message)s'
    logging.basicConfig(format=fmt, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Downsample a 3d dataset')
    parser.add_argument("--dir", help="Directory containing tiff stack to downsample.",
                        required=True)
    parser.add_argument("--res_in", nargs="+", type=float,
                        help="The zyx resolution of the input data in um",
                        required=True)
    parser.add_argument("--res_out", type=int,
                        help="The desired resolution (isotropic) of the output",
                        required=True)
    parser.add_argument("--zmax", type=int,
                        help="Maximum zplane to use.  Useful for testing.")
    parser.add_argument("--algo", choices=["brainreg", "resize_local_mean"],
                        default="brainreg", help="Algorithm for downsampling.")

    args = parser.parse_args()

    if args.algo == "brainreg":
        algo_short = "br"
    elif args.algo == "resize_local_mean":
        algo_short = "rlm"

    pattern_in = f"{args.dir}/*.tif"
    logging.info(f"Input: {pattern_in}")

    img = imread(pattern_in)
    if args.zmax is not None:
        img = img[:args.zmax]

    img = downsample(img, args.res_in, args.res_out, args.algo)

    path_out = f"{args.dir}.{algo_short}.{args.res_out}um.tif"
    logging.info(f"Writing to {path_out}")
    imwrite(path_out, img)

    logging.info(f"Done")
