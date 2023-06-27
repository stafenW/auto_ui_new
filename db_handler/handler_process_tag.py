from django.db import IntegrityError

from .models import ProcessTag


def add_new_tag(tag_name, tag_description):
    new_tag = ProcessTag(
        tag_name=tag_name,
        tag_description=tag_description
    )
    try:
        new_tag.save()
    except IntegrityError:
        return False
    return True


def delete_tag(tag_id):
    try:
        ProcessTag.objects.get(id=tag_id).delete()
    except ProcessTag.DoesNotExist:
        return False
    return True


def edit_tag(tag_id, tag_name, tag_description):
    try:
        tag = ProcessTag.objects.get(id=tag_id)
        tag.tag_name = tag_name
        tag.tag_description = tag_description
        tag.save()
        return True
    except (ProcessTag.DoesNotExist, IntegrityError):
        return False


def query_tags():
    return ProcessTag.objects.order_by('tag_name').all()
