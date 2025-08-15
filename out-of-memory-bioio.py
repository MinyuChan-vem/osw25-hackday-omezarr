from bioio import BioImage, plugin_feasibility_report
from pathlib import Path

tiff_image_path = Path.home()/"data/neuron-data/Human_neuron.tif"
assert tiff_image_path.exists()
print(plugin_feasibility_report(tiff_image_path))

tiff_image = BioImage(tiff_image_path)
print(tiff_image.shape)
print(tiff_image.dims.order)
print(tiff_image.metadata)

from bioio_ome_zarr.writers import (
    OmeZarrWriterV2,
    chunk_size_from_memory_target,
    compute_level_shapes,
    compute_level_chunk_sizes_zslice,
    resize,
)
import dask.array as da

# Prepare data and pyramid parameters
tiff_image_shape = (1, 1, 527, 2614, 2344)       # (T,C,Z,Y,X)
# Create a dask array from random uint8 data
import numpy as np
im = tiff_image.get_image_dask_data()
scaling = (1.0, 1.0, 2.0, 2.0, 2.0)
levels = 4

shapes = compute_level_shapes(tiff_image_shape, scaling, levels)
chunks = compute_level_chunk_sizes_zslice(shapes)

print(shapes)
print(chunks)

# Initialize writer
writer = OmeZarrWriterV2()
write_path = Path.home()/"data/neuron_slash.ome.zarr"
writer.init_store(
    output_path=str(write_path),
    shapes=shapes,
    chunk_sizes=chunks,
    dtype=im.dtype,
)

# Write all timepoints at once
writer.write_t_batches_array(im, channels=[], tbatch=4)

# Generate and write metadata
physical_dims = {"c":1.0, "t":1.0, "z":0.29, "y":0.24, "x":0.24}
physical_units = {"x":"micrometer","y":"micrometer","z":"micrometer","t":"minute"}
channel_names = [f"c{i}" for i in range(tiff_image_shape[1])]
channel_colors = [0xFFFFFF for _ in range(tiff_image_shape[1])]
meta = writer.generate_metadata(
    image_name="TEST",
    channel_names=channel_names,
    physical_dims=physical_dims,
    physical_units=physical_units,
    channel_colors=channel_colors,
)
writer.write_metadata(meta)

# for path in write_path.rglob("*"):
#     if path.is_file() and "." in path.name:
#         if path.name not in [".DS_Store", ".zattrs", ".zgroup"]:
#             new_name = path.name.replace(".", "/")
#             new_path = path.parent / new_name
#             path.replace(new_path)

from pathlib import Path
import zarr

path = write_path
assert path.exists()
zarr_group = zarr.open(path, mode="r+")
print(dir(zarr_group))
print(zarr_group.attrs.asdict())