def max_pil_image_size(pil_images_list: list, based_on_width: bool = True, return_image: bool = False):
    max_width = 0
    max_height = 0
    max_image = None
    for img in pil_images_list:
        width, height = img.size
        if based_on_width:
            if width > max_width:
                max_width = width
                max_height = height
                max_image = img
        else:
            if height > max_height:
                max_width = width
                max_height = height
                max_image = img

    if return_image:
        return max_image
    else:
        return max_width, max_height
