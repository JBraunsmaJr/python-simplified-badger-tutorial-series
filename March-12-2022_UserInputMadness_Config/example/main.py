import json
from util import get_user_input

with open("forms.json", "r") as json_file:
    forms_config = json.load(json_file)


def get_control_type(text: str) -> type:
    if text in ["text", "str"]:
        return str
    if text in ["integer", "int"]:
        return int
    if text in ["decimal", "float"]:
        return float
    raise NotImplementedError(f"Unimplemented type mapping for '{text}'")


def parse_field(field_config: dict()) -> dict:
    query: dict = dict()
    field_type = get_control_type(field_config["type"])

    query["expect"] = field_type
    query["message"] = field_config["message"] + " "
    query["error_message"] = field_config.get("errorMessage",None)

    if "predicate" in field_config:
        condition = field_config["predicate"]

        if field_type == str:
            has_min = "minLength" in condition
            has_max = "maxLength" in condition

            if has_min and has_max:
                pred_min = int(condition["minLength"])
                pred_max = int(condition["maxLength"])
                query["predicate_error_message"] = f"Must be at least {pred_min} to {pred_max} characters in length"
                query["predicate"] = lambda x: pred_min <= len(x) <= pred_max
            elif has_min:
                pred_min = int(condition["minLength"])
                query["predicate"] = lambda x: len(x) >= pred_min
                query["predicate_error_message"] = f"Must be at least {pred_min} characters in length"
            elif has_max:
                pred_max = int(condition["maxLength"])
                query["predicate"] = lambda x: len(x) <= pred_max
                query["predicate_error_message"] = f"Cannot exceed {pred_max} characters in length"
        elif field_type == int or field_type == float:
            has_min = "min" in condition
            has_max = "max" in condition

            if has_min and has_max:
                pred_min = field_type(condition["min"])
                pred_max = field_type(condition["max"])
                query["predicate_error_message"] = f"Expected a value between {pred_min} and {pred_max}"
                query["predicate"] = lambda x: pred_min <= x <= pred_max

            elif has_min:
                pred_min = field_type(condition["min"])
                query["predicate_error_message"] = f"Expected a value greater than or equal to {pred_min}"
                query["predicate"] = lambda x: x >= pred_min

            elif has_max:
                pred_max = field_type(condition["max"])
                query["predicate"] = lambda x: x <= pred_max
                query["predicate_error_message"] = f"Expected a value less than or equal to {pred_max}"
    return query


user_registration_form = forms_config["user-registration"]
user_data: dict = dict()

for field_name, field_config in user_registration_form["fields"].items():
    user_data[field_name] = get_user_input(**parse_field(field_config))

sample = {
    "something": "ts"
}
print(user_data)
