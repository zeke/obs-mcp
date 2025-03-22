#!/usr/bin/env python3

from typing import Any, Dict, List, Optional
import mcp

from .client import obs_client

@mcp.tool()
async def get_source_active(source_name: str) -> bool:
    """
    Gets the active status of a source.
    
    Args:
        source_name: Name of the source to get the active status of
    
    Returns:
        Whether the source is active
    """
    response = await obs_client.send_request("GetSourceActive", {"sourceName": source_name})
    return response.get("sourceActive", False)

@mcp.tool()
async def get_source_screenshot(source_name: str, image_format: str = "png", 
                               image_width: int = 0, image_height: int = 0, 
                               image_compression_quality: int = -1) -> str:
    """
    Gets a Base64-encoded screenshot of a source.
    
    Args:
        source_name: Name of the source to get a screenshot of
        image_format: Image format (png, jpeg, bmp, tga, gif)
        image_width: Screenshot width (0 = source width)
        image_height: Screenshot height (0 = source height)
        image_compression_quality: Compression quality (1-100, -1 = default)
    
    Returns:
        Base64-encoded screenshot image
    """
    payload = {
        "sourceName": source_name,
        "imageFormat": image_format
    }
    
    if image_width > 0:
        payload["imageWidth"] = image_width
    
    if image_height > 0:
        payload["imageHeight"] = image_height
    
    if image_compression_quality >= 0:
        payload["imageCompressionQuality"] = image_compression_quality
    
    response = await obs_client.send_request("GetSourceScreenshot", payload)
    return response.get("imageData", "")

@mcp.tool()
async def save_source_screenshot(source_name: str, file_path: str, image_format: str = "png", 
                                image_width: int = 0, image_height: int = 0, 
                                image_compression_quality: int = -1) -> str:
    """
    Saves a screenshot of a source to a file.
    
    Args:
        source_name: Name of the source to get a screenshot of
        file_path: Path to save the screenshot to
        image_format: Image format (png, jpeg, bmp, tga, gif)
        image_width: Screenshot width (0 = source width)
        image_height: Screenshot height (0 = source height)
        image_compression_quality: Compression quality (1-100, -1 = default)
    
    Returns:
        Path to the saved screenshot
    """
    payload = {
        "sourceName": source_name,
        "imageFormat": image_format,
        "imageFilePath": file_path
    }
    
    if image_width > 0:
        payload["imageWidth"] = image_width
    
    if image_height > 0:
        payload["imageHeight"] = image_height
    
    if image_compression_quality >= 0:
        payload["imageCompressionQuality"] = image_compression_quality
    
    response = await obs_client.send_request("SaveSourceScreenshot", payload)
    return response.get("imageData", "")

@mcp.tool()
async def get_source_filter_list(source_name: str) -> Dict[str, Any]:
    """
    Gets a list of filters on a source.
    
    Args:
        source_name: Name of the source to get the filters of
    
    Returns:
        Dict with filters array (each with name, kind, index, settings)
    """
    return await obs_client.send_request("GetSourceFilterList", {"sourceName": source_name})

@mcp.tool()
async def get_source_filter_default_settings(filter_kind: str) -> Dict[str, Any]:
    """
    Gets the default settings for a filter kind.
    
    Args:
        filter_kind: Filter type to get the default settings for
    
    Returns:
        Dict with default filter settings
    """
    return await obs_client.send_request("GetSourceFilterDefaultSettings", {"filterKind": filter_kind})

@mcp.tool()
async def create_source_filter(source_name: str, filter_name: str, filter_kind: str, 
                              filter_settings: Optional[Dict[str, Any]] = None) -> None:
    """
    Creates a new filter on a source.
    
    Args:
        source_name: Name of the source to add the filter to
        filter_name: Name for the new filter
        filter_kind: Type of filter to add
        filter_settings: Settings object to initialize the filter with
    """
    payload = {
        "sourceName": source_name,
        "filterName": filter_name,
        "filterKind": filter_kind
    }
    
    if filter_settings:
        payload["filterSettings"] = filter_settings
    
    await obs_client.send_request("CreateSourceFilter", payload)

@mcp.tool()
async def remove_source_filter(source_name: str, filter_name: str) -> None:
    """
    Removes a filter from a source.
    
    Args:
        source_name: Name of the source to remove the filter from
        filter_name: Name of the filter to remove
    """
    await obs_client.send_request("RemoveSourceFilter", {
        "sourceName": source_name,
        "filterName": filter_name
    })

@mcp.tool()
async def set_source_filter_name(source_name: str, filter_name: str, new_filter_name: str) -> None:
    """
    Sets the name of a source filter (rename).
    
    Args:
        source_name: Name of the source the filter is on
        filter_name: Current name of the filter
        new_filter_name: New name for the filter
    """
    await obs_client.send_request("SetSourceFilterName", {
        "sourceName": source_name,
        "filterName": filter_name,
        "newFilterName": new_filter_name
    })

@mcp.tool()
async def get_source_filter(source_name: str, filter_name: str) -> Dict[str, Any]:
    """
    Gets information about a source filter.
    
    Args:
        source_name: Name of the source
        filter_name: Name of the filter
    
    Returns:
        Dict with filter information (enabled, index, kind, settings)
    """
    return await obs_client.send_request("GetSourceFilter", {
        "sourceName": source_name,
        "filterName": filter_name
    })

@mcp.tool()
async def set_source_filter_index(source_name: str, filter_name: str, filter_index: int) -> None:
    """
    Sets the index position of a filter on a source.
    
    Args:
        source_name: Name of the source the filter is on
        filter_name: Name of the filter
        filter_index: New index position of the filter
    """
    await obs_client.send_request("SetSourceFilterIndex", {
        "sourceName": source_name,
        "filterName": filter_name,
        "filterIndex": filter_index
    })

@mcp.tool()
async def set_source_filter_settings(source_name: str, filter_name: str, 
                                    filter_settings: Dict[str, Any], overlay: bool = True) -> None:
    """
    Sets the settings of a source filter.
    
    Args:
        source_name: Name of the source the filter is on
        filter_name: Name of the filter to set the settings of
        filter_settings: Object of settings to apply
        overlay: True to overlay with existing settings, false to reset
    """
    await obs_client.send_request("SetSourceFilterSettings", {
        "sourceName": source_name,
        "filterName": filter_name,
        "filterSettings": filter_settings,
        "overlay": overlay
    })

@mcp.tool()
async def set_source_filter_enabled(source_name: str, filter_name: str, filter_enabled: bool) -> None:
    """
    Sets the enable state of a source filter.
    
    Args:
        source_name: Name of the source the filter is on
        filter_name: Name of the filter
        filter_enabled: New enable state of the filter
    """
    await obs_client.send_request("SetSourceFilterEnabled", {
        "sourceName": source_name,
        "filterName": filter_name,
        "filterEnabled": filter_enabled
    })