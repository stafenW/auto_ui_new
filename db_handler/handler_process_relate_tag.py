from .models import TagRelation


def add_relate(tag_id, process_id):
    new_relate = TagRelation(
        tag_id=tag_id,
        process_id=process_id
    )
    new_relate.save()
    return True


def add_relates(tag_ids: list, process_id):
    for tag_id in tag_ids:
        add_relate(tag_id, process_id)
    return True


def del_relate(process_id):
    TagRelation.objects.filter(id=process_id).delete()
    return True


def update_relation(process_id, tag_ids):
    del_relate(process_id)
    add_relates(tag_ids, process_id)
    return True


def query_process_id_list_from_tag(tag_ids):
    processes = TagRelation.objects.filter(tag_ids__in=tag_ids).values_list('process_id', flat=True)
    return list(processes)


def query_tag_of_process(process_id):
    return TagRelation.objects.filter(process_id=process_id)
