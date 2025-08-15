# Omezarr Group

Explore different Ome-Zarr implementations for converting and working with large-scale imaging data.

We tested various configurations to convert a multi-page TIFF file into the Ome-Zarr format.

## Installation

### Conda (dask env)

```shell
conda create -n big-imaging-data-tutorial python=3.13 -y
```

```shell
conda activate big-imaging-data-tutorial
```

```shell
pip install "matplotlib" "jupyterlab" "numcodecs==0.15.1" "numpy==2.3.2" "zarr==2.18.7" "pydantic-zarr==0.7.0" "ome-zarr-models==0.1.10" "joblib==1.5.1" "tifffile[zarr]<2025.5.21" "bioio" "bioio-tifffile" "bioio-ome-zarr"
```

```shell
pip install "napari[all]" "napari-ome-zarr"
```

### Pixi

```shell
pixi install -e <env-name>
```

Possible envs are `ngio` `ngff-zarr` `ome-zarr` `stack-to-chunk` `bioio`
