from .models import ProcessTag


def add_new_tag(tag_name):
    new_tag = ProcessTag(
        tag_name=tag_name
    )
    new_tag.save()
    return new_tag.to_dict()


def delete_tag(tag_id):
    ProcessTag.objects.get(id=tag_id).delete()
    return True


def edit_tag(tag_id, tag_name):
    try:
        tag = ProcessTag.objects.get(id=tag_id)
        tag.tag_name = tag_name
        tag.save()
        return True
    except ProcessTag.DoesNotExist:
        return False


def query_tags():
    return ProcessTag.objects.order_by('name').all()
