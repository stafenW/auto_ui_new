from .models import TagRelation, ProcessTag, Process


def add_relate(tag_id, process_id):
    new_relate = TagRelation(
        tag_id=ProcessTag(id=tag_id),
        process_id=Process(id=process_id)
    )
    new_relate.save()
    return True


def add_relates(tag_ids: list, process_id):
    for tag_id in tag_ids:
        add_relate(tag_id, process_id)
    return True


def del_relate(process_id):
    TagRelation.objects.filter(process_id=process_id).delete()
    return True


def update_relation(process_id, tag_ids):
    del_relate(process_id)
    add_relates(tag_ids, process_id)
    return True


def query_process_id_list_from_tag(tag_ids):
    processes = TagRelation.objects.filter(tag_id__in=tag_ids).values_list('process_id', flat=True)
    return list(processes)


def query_tag_of_process(process_id):
    return TagRelation.objects.filter(process_id=process_id)


def query_tags_of_processes_to_dict(process_ids):
    tag_relations = TagRelation.objects.filter(process_id__in=process_ids)
    tag_dict = {}

    for tag_relation in tag_relations:
        process_id = tag_relation.process_id_id
        if process_id not in tag_dict:
            tag_dict[process_id] = []
        tag_dict[process_id].append(tag_relation.to_dict())
    return tag_dict
