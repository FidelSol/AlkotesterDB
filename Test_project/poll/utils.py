from django.core.serializers import serialize
import json

def serialize_bootstraptable(queryset):
    json_data = serialize('json', queryset)
    json_final = {"total": queryset.count(), "rows": []}
    data = json.loads(json_data)
    for item in data:
        del item["model"]
        item["fields"].update({"id": item["pk"]})
        item = item["fields"]
        json_final['rows'].append(item)
    return json_final
