import shutil
from pathlib import Path

import pytest
from geokoord.koordinates.exports import validate_export
from requests.exceptions import HTTPError


@pytest.fixture
def linz_exports(linz):
    """Return the exports."""
    return linz.get_exports()


@pytest.fixture
def lris_exports(lris):
    """Return the exports."""
    return lris.get_exports()


@pytest.fixture
def linz_single_export(linz_exports):
    """Return a single export."""
    return linz_exports[0]


@pytest.fixture
def single_export_id(linz_single_export):
    """Return a single export ID."""
    return linz_single_export["id"]


def test_linz_exports_instance(linz_exports):
    """Test if the exports instance is a list."""
    assert isinstance(linz_exports, list)


def test_lris_exports_instance(lris_exports):
    """Test if the exports instance is a list."""
    assert isinstance(lris_exports, list)


def test_exports_structure(linz_exports):
    """Test the structure of each export in the exports list."""
    assert isinstance(linz_exports[0], dict)
    assert "id" in linz_exports[0].keys()
    assert "name" in linz_exports[0].keys()
    assert "created_at" in linz_exports[0].keys()
    assert "created_via" in linz_exports[0].keys()
    assert "state" in linz_exports[0].keys()
    assert "url" in linz_exports[0].keys()
    assert "download_url" in linz_exports[0].keys()


def test_export_instance(linz_single_export):
    """Test if the export instance is a dictionary."""
    assert isinstance(linz_single_export, dict)


def test_export_structure(linz_single_export):
    """Test the structure of the export dictionary."""
    assert "id" in linz_single_export.keys()
    assert "name" in linz_single_export.keys()
    assert "created_at" in linz_single_export.keys()
    assert "created_via" in linz_single_export.keys()
    assert "state" in linz_single_export.keys()
    assert "url" in linz_single_export.keys()
    assert "download_url" in linz_single_export.keys()


def test_invalid_export_id(linz):
    """Test if an invalid export ID raises a ValueError."""
    with pytest.raises(HTTPError):
        linz.get_export(0)


def test_valid_export(linz, vector_id, export_extent):
    """Test if a valid export returns True."""
    url = f"https://{linz.domain}/services/api/v{linz.api_version}/exports/"
    data = {
        "crs": linz.crs,
        "items": [
            {
                "item": f"https://{linz.domain}/services/api/v{linz.api_version}/layers/{vector_id}/",
            }
        ],
        "delivery": {"method": "download"},
        "extent": export_extent,
        "formats": {"vector": "application/x-ogc-gpkg"},
    }
    export_request = validate_export(url, linz._headers, data)
    assert isinstance(export_request, dict)


def test_invalid_layer(linz, export_extent):
    """Test if an invalid export raises a ValueError."""
    fake_layer_id = 50768000
    url = f"https://{linz.domain}/services/api/v{linz.api_version}/exports/"
    data = {
        "crs": linz.crs,
        "items": [
            {
                "item": f"https://{linz.domain}/services/api/v{linz.api_version}/layers/{fake_layer_id}/",
            }
        ],
        "delivery": {"method": "download"},
        "extent": export_extent,
        "formats": {"vector": "application/x-ogc-gpkg"},
    }
    with pytest.raises(HTTPError):
        validate_export(url, linz._headers, data)


def test_over_size_limit(linz):
    """Test if an export over the size limit returns False."""
    large_raster_id = 110757
    url = f"https://{linz.domain}/services/api/v{linz.api_version}/exports/"
    data = {
        "crs": linz.crs,
        "items": [
            {
                "item": f"https://{linz.domain}/services/api/v{linz.api_version}/layers/{large_raster_id}/",
            }
        ],
        "delivery": {"method": "download"},
        "formats": {"grid": "image/tiff;subtype=geotiff"},
    }
    with pytest.raises(ValueError):
        validate_export(url, linz._headers, data)


def test_download_layer(linz, raster_id):
    """Test if a layer can be downloaded."""
    linz.download_dir = Path("tests/data/test-download-layer")
    linz.download_dir.mkdir(parents=True, exist_ok=True)
    download_path = linz.download_layer(layer_id=raster_id)
    shutil.rmtree(linz.download_dir)
    assert isinstance(download_path, Path)


def test_export_batch(linz, vector_id, raster_id, export_extent):
    """Test if a batch export can be downloaded."""
    linz.extent = export_extent
    linz.create_export(layer_id=vector_id, format="vector", batch=True)
    linz.create_export(layer_id=raster_id, format="grid", batch=True)

    assert isinstance(linz.export_queue, list)
    assert len(linz.export_queue) == 2
    assert isinstance(linz.export_queue[0], dict)


def test_batch_collect(linz, vector_id, raster_id, export_extent):
    """Test if a batch export can be downloaded."""
    linz.download_dir = Path("tests/data/test-download-layer")
    linz.download_dir.mkdir(parents=True, exist_ok=True)
    linz.extent = export_extent
    linz.create_export(layer_id=vector_id, format="vector", batch=True)
    linz.create_export(layer_id=raster_id, format="grid", batch=True)
    linz.collect()
    shutil.rmtree(linz.download_dir)
    assert len(linz.export_queue) == 0


def test_partial_batch(linz, raster_id, export_extent):
    """Test if a batch export can be downloaded."""
    linz.extent = export_extent
    layers_to_download = [50768000, raster_id]
    for layer_id in layers_to_download:
        try:
            linz.create_export(layer_id=layer_id, batch=True)
        except HTTPError:
            pass

    assert isinstance(linz.export_queue, list)
    assert len(linz.export_queue) == 1
    assert isinstance(linz.export_queue[0], dict)
