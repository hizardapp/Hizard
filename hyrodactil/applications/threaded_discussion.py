from collections import defaultdict


def group(messages,
          level=0,
          parent_pk=None,
          messages_by_parent=None,
          threaded=None):

    if not messages_by_parent:
        messages_by_parent = defaultdict(list)
        for message in messages:
            messages_by_parent[message.parent_id].append(message)

    if not threaded:
        threaded = []

    for node in messages_by_parent[parent_pk]:
        threaded.append((level, node))
        group(messages, level+1, node.pk, messages_by_parent, threaded)

    return threaded
