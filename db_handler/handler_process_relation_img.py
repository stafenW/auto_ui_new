from .models import Image, Process


def add_process_description_img(new_process_id, image_data):
    new_image = Image(
        process=Process(id=new_process_id),
        image=image_data,
    )
    new_image.save()
    return True


def del_process_description_img(process_id):
    Image.objects.filter(process_id=process_id).delete()
    return True


def update_process_description_img(process_id, image_data):
    del_process_description_img(process_id)
    add_process_description_img(process_id, image_data)
    return True


def query_img_path(process_id):
    try:
        return Image.objects.get(process=process_id).image.url
    except Image.DoesNotExist:
        return False


def query_thumbnail_path(process_id):
    try:
        return Image.objects.get(process=process_id).thumbnail.url
    except Image.DoesNotExist:
        return False


def query_pic_path(process_id):
    try:
        pic = Image.objects.get(process=process_id)
        return pic.image.url, pic.thumbnail.url
    except Image.DoesNotExist:
        return False, False


def query_pic_paths_to_dict(process_ids):
    pic_paths = {}

    images = Image.objects.filter(process__in=process_ids)
    for image in images:
        try:
            pic_paths[image.process_id] = (image.image.url, image.thumbnail.url)
        except ValueError:
            pic_paths[image.process_id] = (image.image.url, '')

    return pic_paths
