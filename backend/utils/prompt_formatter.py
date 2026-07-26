import json


def to_json(data):

    # Pydantic Model
    if hasattr(data, "model_dump"):

        return json.dumps(
            data.model_dump(
                exclude_none=True
            ),
            indent=2,
            ensure_ascii=False
        )

    # List of Pydantic Models
    if isinstance(data, list):

        return json.dumps(
            [
                item.model_dump(exclude_none=True)
                if hasattr(item, "model_dump")
                else item
                for item in data
            ],
            indent=2,
            ensure_ascii=False
        )

    # Normal Python object
    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )