# Configurable User Input

The target of this section is to expose you to configurable pipelines / why configuration files are the bomb diggity! 

The most common use for a config file is for values that can change based on production site. For instance, your database connection string will differ between your local development environment and production. So, it makes sense for putting your connection string(s) in a config! 

Alternatively, you might be familiar with the idea of "modding" videogames. This is accomplished via loading specific config files. Typically, it'll describe the author, description, the various assets needed, etc. Think of it as modifying / changing the behavior of your application without editing a line of code! 

In this section we'll take our relatively basic user-input API and turn it into a configurable pipeline. Worth mentioning that we're currently using a text-based application. The true appreciation for what we're about to do will come when we convert this into a website!

----
# Config Types

A config file is just a structured / formatted file. Some sort of value is associated with a key. The most common serialization type is `JSON`, or JavaScript Object Notation. Second, you'd probably find 
an environment file / environment variable before seeing an INI file, or XML config file.

**JSON**:
```json
{
  "sampleConnectionString": "Data Source=sample.db",
  "retryCount": 3
}
```

**XML**:
```xml
<Config>
    <SampleConnectionString>Data source=sample.db</SampleConnectionString>
    <RetryCount>3</RetryCount>
</Config>
```

**INI**:
```ini
SampleConnectionString = Data Source=sample.db
RetryCount = 3
```

**ENV** (Environment):
```env
SampleConnectionString="Data Source=sample.db"
RetryCount=3
```

----

# Problem

## How on Earth do we come up with a config?
For the purpose of this section we will set the following goals for ourselves. 
   - We need to dynamically create user-forms. Inside a form we need to specify `fields` which a user must fill out

## How do we load/save/modify a config file?
It's actually surprisingly easy to work with JSON in most languages. In C# we have `Newtonsoft`, 
in Python we have the `json` module -- which we get by default without adding any additional libraries!

## What do, or what can I make configurable?
You can make anything configurable. It ultimately boils down to the application requirements, and how extendable / flexible you want things to be.

----

## Where do we begin?

Let's figure out what a user input field is first.

Similar to how a website works, there are various input control such as a textbox, slider, datepicker, etc that a user can interact with to provide data.
Ultimately a field has

- A name / ID associated with it. This makes it easier to track.
- Type of data to expect/validate -- such as a string, number, etc.
- Error message -- for when they provide invalid input. In some cases we could infer an error message based on context.

Like in any scenario, we need to let the user know WHAT we want from them so a message/prompt is an absolute must!

Let's create a user-registration form where we need a username and age. What **could** this look like? Note, this structure is just **my** interpretation. 
From my point of view I would like to create a form where I can define the name/ID for it. Then specify fields that would make up this form in the order it'll
appear to the user.

I'll create a json file called `forms.json` in my project directory.
```json
{
  "user-registration": {
     "fields": {
      "username": {
        "message": "Please provide a valid username.",
        "type": "text",
        "predicate": {
          "maxLength": 25
        }
      },
      "age": {
        "type": "int",
        "message": "How old are you?",
        "predicate": {
          "min": "1",
          "max": "130"
        }
      }
    }
  }
}
```

The above config uses key/value pairs (dictionary). This allows us to basically say the first layer of keys are form names! In this case `user-registration`.

The object (dictionary) associated with a form name tells us some basic info about it. In our case, `fields`. Though in the future if we wanted
to add more info such as a form title, or whatever, we could do so! 

Our fields object (dictionary) contains info about what type of data we want our user to give. Notice... our config is closely aligned with our `get_user_input` function
we have!

| Key | Value                                                                               |
| ---- |-------------------------------------------------------------------------------------|
| message | This represents the text/prompt the user must answer                                |
| type | The type of data we want from the user. For instance, `int`, `str`/`text`, `float`  |
| predicate | Configuration object we can use to specify validation criteria (not requred though) |

`text`/`str` predicate
For text - we can keep it simple by specifying required lengths.

Similarly, we can specify a min/max range for numbers.


How the heck do we translate this into actual code?!? Let's dive in.

---

## Python code!

```python
import json
from util import get_user_input # this is how we can reference our function in the other file!

"""
Whenever you're working with a file, connection, or something related to IO -- it's important
to dispose / close / cleanup the things you use!

In this case, we want to open and read a file. By utilizing the `with` keyword - once we exit the with-scope it'll
automatically clean stuff up for us! No need to manually do stuff!
"""

with open("forms.json", "r") as json_file:   # this starts the with-scope. 
    forms_config = json.load(json_file)        
# at this point the json file is closed
```

Now to create a function that will help us map the textual representation of our 'type' value to the actual 'python' type such as `str`, `float`, `int`.
```python
def get_type(text: str) -> type:
    if text in ["text", "str"]: # this is one way for us to allow 'aliases' for our types!
        return str
    if text in ["integer", "int"]:
        return int
    if text in ["decimal", "float"]:
        return float
    raise NotImplementedError(f"Unimplemented type mapping for '{text}'")
```

Now comes the more... difficult part. The validation!!! We need to break down the config values per field, so lets create the function for that!

I know some of you are probably curious what's about to happen. Why am I using a dictionary?!?! -- We're going to leverage the splat operator (** -- two asterisks)... not entirely
sure if that's the official word for it but it basically converts a dictionary into a format of `key=value` making it ideal for passing arguments! 


I know.. this is a lot of code but after playing around with it - it's quite fun to play around with!
```python
def parse_field(field_config: dict()) -> dict:
    """
    Converts a dictionary (config) for a field and returns the appropriate
    query in the form of a dictionary!
    """
    query: dict = dict()
    field_type = get_type(field_config["type"])
    
    """
    Please note the keys we are using in our dictionary 'query'
    These keys match the parameter names that are used in `get_user_input`!!!
    This will be important later when we utilize the splat operator for 
    slapping all of these values into that function!!! >:D
    """
    
    query["message"] = field_config["message"]
    query["error_message"] = field_config.get("errorMessage", None) # this means if errorMessage doesn't exist -- default with the value `None`
    query["expect"] = field_type
        
    if "predicate" in field_config:
        predicate_config = field_config["predicate"]
            
        if field_type == str:
            """
            For now, we'll only support the ability for min/max length on a string
            """
            has_min = "minLength" in predicate_config
            has_max = "maxLength" in predicate_config
            
            """
            If you're wondering WHY we're parsing the length values it's because
            a user may/may not provide the number as a string or as a number
            """
            
            if has_min and has_max:
                pred_min = int(predicate_config["minLength"])
                pred_max = int(predicate_config["maxLength"])
                query["predicate_error_message"] = f"Must be at least {pred_min} to {pred_max} characters in length!"
                query["predicate"] = lambda x: pred_min <= len(x) <= pred_max
            elif has_min:
                pred_min = int(predicate_config["minLength"])
                query["predicate"] = lambda x: len(x) >= pred_min
                query["predicate_error_message"] = f"Must be at least {pred_min} characters in length"
            elif has_max:
                pred_max = int(predicate_config["maxLength"])
                query["predicate"] = lambda x: len(x) <= pred_max
                query["predicate_error_message"] = f"Cannot exceed {pred_max} characters in length"
        elif field_type == int or field_type == float:
            """
            Support min/max or range
            """
            
            # these two values are to avoid recalculating the same thing over and over
            # we just want to know if "min" or "max" were defined in our dictionary!
            has_min = "min" in predicate_config
            has_max = "max" in predicate_config
                                    
            # if both values are given then we need to dynamically establish the range
            if has_min and has_max:
                pred_min = field_type(predicate_config["min"])
                pred_max = field_type(predicate_config["max"])            
                query["predicate_error_message"] = f"Expected a value between {pred_min} and {pred_max}"
                query["predicate"] = lambda x: pred_min <= x <= pred_max
                
            # if only minimum is provided
            elif has_min:
                pred_min = field_type(predicate_config["min"])
                query["predicate_error_message"] = f"Expected a value greater than or equal to {pred_min}"
                query["predicate"] = lambda x: x >= pred_min
                
            # if only the maximum is provided
            elif has_max:
                pred_max = field_type(predicate_config["max"])
                query["predicate"] = lambda x: x <= pred_max                
                query["predicate_error_message"] = f"Expected a value less than or equal to {pred_max}"
    
    return query
```


Now we just need to present a form to the user! For this example we'll manually specify 
which form to use

```python
user_registration_form = forms_config["user-registration"]

# this will be used to store the info our user gives us!
user_data: dict = dict()

# key/value pair
for field_name, field_config in user_registration_form["fields"].items():
    """
    The dictionary that gets returned from `parse_field` is going to
    be splatted into the `get_user_input` method!
    
    What this means.... it converts the dictionary into
    
    key=value,key=value,key=value.
    
    The way you can specify parameter name equals something, that's what this is doing
    
    get_user_input(message="something",error_message="nope")
    
    is the same thing as
    
    sample_dict = { "message": "something", "error_message": "nope"}
    get_user_input(**sample_dict)
    """
    user_data[field_name] = get_user_input(**parse_field(field_config))

# for now we'll just output everything...
# you can do whatever you want with this data
print(user_data)
```