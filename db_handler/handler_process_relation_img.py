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
    return Image.objects.get(process_id).values_list('image')


def query_thumbnail_path(process_id):
    return Image.objects.get(process_id).values_list('thumbnail')
