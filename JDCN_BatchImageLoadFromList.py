import random
import os
import torch
import numpy as np
from PIL import Image, ImageSequence


def pilToImage(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


def extract_file_names(file_paths):
    """
    Extract file names without extensions from a list of file paths.

    Parameters:
    - file_paths: A list of file paths.

    Returns:
    - A list of file names without extensions.
    """
    file_names = []

    for file_path in file_paths:
        base_name, _ = os.path.splitext(os.path.basename(file_path))
        file_names.append(base_name)

    return file_names


def load_images(image_paths):
    """
    Load a list of images using the provided code for reading.

    Parameters:
    - image_paths: A list of file paths for the images.

    Returns:
    - A list of loaded images.
    """
    loaded_images = []

    for image_path in image_paths:
        try:
            img = Image.open(image_path)
            image = img.convert("RGB")
            loaded_images.append(pilToImage(image))
        except Exception as e:
            # Catching exceptions to ensure the code doesn't stop in the middle
            print(f"Error loading image from '{image_path}': {e}")

    return loaded_images


def get_batch_from_list(input_list, batch_size, page_number, direction):
    """
    Get a batch of elements from a list based on the batch size, page number, and direction.

    Parameters:
    - input_list: The input list to extract batches from.
    - batch_size: The size of each batch.
    - page_number: The page number to retrieve (1-indexed).
    - direction: "TOPTOBOTTOM", "BOTTOMTOTOP", or "RANDOM".

    Returns:
    - A list containing the elements of the specified batch.
    """
    try:
        # Validate the direction parameter
        valid_directions = {"TOPTOBOTTOM", "BOTTOMTOTOP", "RANDOM"}
        if direction not in valid_directions:
            raise ValueError(f"Direction must be one of {valid_directions}.")

        # Ensure input_list is not empty
        if not input_list:
            raise ValueError("Input list is empty.")

        # Calculate the starting index for the specified page
        start_index = (page_number - 1) * batch_size

        # Check for out-of-range conditions
        if start_index < 0 or start_index >= len(input_list):
            raise ValueError("Start index is out of range.")

        # Define a dictionary to map directions to extraction functions
        direction_actions = {
            "TOPTOBOTTOM": lambda start, size: input_list[start:start + size],
            "BOTTOMTOTOP": lambda start, size: input_list[-start - size:-start][::-1],
            "RANDOM": lambda start, size: random.sample(input_list, size)
        }

        # Extract the batch based on the direction
        batch_extraction = direction_actions[direction]
        batch = batch_extraction(start_index, batch_size)

        return batch

    except ValueError as ve:
        print(f"Error in get_batch_from_list: {ve}")
        return []

# Example usage:
# input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# batch_size = 3
# page_number = 2
# direction = "RANDOM"
# result = get_batch_from_list(input_list, batch_size, page_number, direction)
# print(result)


class JDCN_BatchImageLoadFromList:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "PathList": ("STRING", {"forceInput": True}),
                "Index": ("INT", {"default": 1, "min": 1, "max": 9999}),
                "BatchSize": ("INT", {"default": 5, "min": 0, "max": 9999}),
                "BatchDirection": (["TOPTOBOTTOM", "BOTTOMTOTOP", "RANDOM"],),
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "INT")
    RETURN_NAMES = ("Images", "ImageNames", "ImagePaths", "Index")
    FUNCTION = "doit"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True, True, True, False)
    CATEGORY = "🔵 JDCN 🔵"    

    def doit(self, PathList, Index, BatchSize, BatchDirection):
        paths = get_batch_from_list(PathList, BatchSize[0], Index[0], BatchDirection[0])
        names = extract_file_names(paths)
        images = load_images(paths)
        # print(PathList,Index,BatchSize,BatchDirection)
        return (images, names, paths, Index)
        # return ([],[],[],0)


N_CLASS_MAPPINGS = {
    "JDCN_BatchImageLoadFromList": JDCN_BatchImageLoadFromList,
}

N_DISPLAY_NAME_MAPPINGS = {
    "JDCN_BatchImageLoadFromList": "JDCN_BatchImageLoadFromList",
}
