# User Input Madness


## Problem
 - Input Validation is critical for any application
 - As a user, I don't want to restart an app over invalid input
 - As a user, I want to see a clear error message. Why you no work! (insert gif)

## Solution
Can utilize a cyclic approach of:

- Prompt user with some message/question
- Retrieve their input
- Validate their input
- If valid, continue. Otherwise, repeat process

### Loops

The syntax will vary between languages. However, the way they operate remains the same for every. single. language.

#### for Loops

Excellent for when you want something to be done '**n**' times. Want to print '*' 5 times? 10 times? This is the loop for you! 


**Python**:
```python
for x in range(5):
    print('*', end='')

# output --> *****
```

**C#**:
```csharp
for(int i = 0; i < 5; i++) // This line is also the same between C++ and Java!
    Console.Write("*");  // This doesn't require curly brackets because only 1 statement exists in the loop body

/// output --> *****

for(int i = 0; i < 5; i++)
{ // <-- This begins the body / scope
    Console.Write("*");
} // <-- This ends the body / scope
```

#### while Loops

Used when you aren't sure how many times something needs to run. It could be 0... 1.... 1000 times. Game engines are based around while loops! while the player isn't trying to leave / is alive -- keep running the game!

The thing to remember though, is the condition you're checking needs to at some point update -- otherwise you can run into infinite loops!

**Python**:
```python
count = 0
while count < 0:
    count += 1
```

**C#**:
```csharp
int count = 0;
while(count < 10)
    count++; // again, because only 1 statement exists for the loop body
// OR
while(count < 10)
{
    count++;
}
```

There are some keywords to remember with loops!

```yml
continue: This means move to the NEXT cycle / iteration. Stop at whatever line, and go back to the beginning of loop
break: Stop the loop completely. Exit out of the loop and continue with the next statement
```

**Python**:
```python
for item in ["sword", None, "shield"]:
    if item is None:
        continue
    print(item)

print("done")

# output
sword
shield
done
```

```python
for item in ["sword", None, "shield"]:
    if item is None:
        break
    print(item)

print("done")
# output
sword
done
```



----

### Functions
Copying/Pasting code introduces unnecessary complexity and makes it harder to debug/maintain your codebase. If you identify a set of common code... odds are it should be a function!

I would argue that planning your application before ever writing a line of code is important but if you're a newcomer... you won't be able to plan! If you haven't used something, or utilized a function how would you know?!?!?!

Similar to loops, the syntax for creating a function varies however the same building blocks exist!

Below this is what makes up a **method signature**
```yaml
identifier: This behaves like a variable. When referencing this you can invoke / call the method!
return type: This indicates the type of value that will be provided by this method. (void if nothing)
parameter_s: Optional. Can specify the data you want to work with
```

**Python**:
```python
def function_name():
    pass

# call it 
function_name()
```
```yaml
def: This is the python way of saying "I'm DEFINING a function"
function_name: This is the indentifier
(): This means no parameters are needed for this function
return_type: Python hides this... by default the return type is 'None' aka 'void' meaning "I don't return anything"
```

**C#**:
```csharp
void Print(string message)
{
    Console.WriteLine(message);
}

// call it (while passing in a string)
Print("something")
```
```yaml
void: This is the return type
Print: this is the identifier
message: accepts a parameter of type 'string'
```

----

Up until this point we haven't done anything useful with a function. Now let's look into creating functions for capturing user input!

**but we have the 'input' function already**... we'll be using that... don't worry. Also, that only exists for Python! What we'll be going over can be utilized in any language. Plus or minus a few syntax changes....

```md
As a developer I want to capture a specific 'type' of data. So an 'int', 'float', etc
# get user input

- Display a message to user
- Specify the desired type of data the user must provide
- Return the user input in our specified type

while true
    display message / get input
    if provided data is valid
        return data
    print error message indicating invalid data was given
```


Alright, what if we want to provide an optional error message?
```md
while true
    display message / get input
    if provided data is valid
        return data
    print provided error message if given, otherwise default error message
```

Okay... what if... here me out... we want to specify additional conditions this user input must have? Like...
- a number greater than 0
- a value from a list of options
- a number in range of 0 and 10

Well, this concept is known as a 'predicate'... a function which returns a bool (true/false). Of course, this should be optional anddddd perhaps have an optional error message as well!

```md
while true
    display message / get input
    if provided data is valid
        if predicate is given
            if predicate
                return data
            print predicate error message if given, otherwise default predicate error message
            continue
        return data -- because at this point we assume predicate wasn't given
    print provided error message if given, otherwise default error message
```

### Display and select item from list
We can utilize the function we created above to help us out! We will create a new function for this

```md
# select from list
- display title
- display each item from list with an associated number (which is used for selection purposes)
- display prompt to user
- accept an optional error message
- return the appropriate item from given list

--- Example ---
Title goes here
[0] Item 1
[1] Item 2
[2] Item 3

prompt goes here

--- pseudocode ---
if collection is not iterable
    throw an assertion error because we require a list of sorts!

print title

for index ; index < length of collection; index++
    - format string and print
        [{index}]\t{collection[index]}
print new line to give spacing

selection = get_user_input(prompt, int, error message, predicate defining range of 0 and length)
return collection[selection]

```

-----

### Creating a configurable form?

Sometimes you'll get customers who drive you nuts, changing requirements last minute. Or perhaps in your case you might need to add a bit of dynamic user inputs! 

AKA... without modifying your code... your input validation could be modified... stuff can be removed / deleted

When designing a config you just need to think... "What do I need?" JSON is a popular format so we'll use that. Alternatively you could use XML, INI, or even CSV

-- example --
```json
{
    "type": "int",
    "prompt": "Give me a number"
}
```

It's simple, but ideally we want the user to be prompted "Give me a number" and they give us a valid number.

Currently we have the ability to 
- display a prompt/message asking user for something
- specify type of data the user must provide
- provide optional error message when invalid data is given
- provide an optional condition the user's data must meet
- provide an optional conditional error message when predicate isn't met

The danger though, is if we enabled user-defined predicates. Malicious code could be inserted. Ideally we should create a way of defining configurable predicates. Perhaps have pre-existing conditions where these config values plug into

```json
{
    "predicateType": "age"
}
```

Where we have some sort of function that verifies a number 0 <= x <= 130

Or perhaps 
```json
{
    "predicateConfig": {
        "type": "range",
        "min": -10,
        "max": 10
    }
}
```

Where we just defined a predicate where the value must be between -10 and 10

---
Having a config for just 1 type of user input isn't **that** useful though. We may need multiple types of input!

As a result, we'll use a dictionary approach because it makes lookups easier. Just means we'll reference a form by this 'key' name

```json
{
    "inputType": {
        "prompt": "Give me a number ",
        "type": "int",
        "errorMessage": "give me a valid number! What you gave, wasn't that"
    },

    "getAge":{
        "prompt": "How old are you? ",
        "type": "int",
        "errorMessage": "give me a valid number! What you gave, wasn't that",
        "predicate": {
            "type": "age",
            "errorMessage": "Please provide a number > 0"
        }
    },

    "getName": {
        "prompt": "What's your name? ",
        "type": "str"
    },

    "selectItem": {
        "prompt": "Please select an item: ",
        "type": "select"
    }
}
```

```json
{
    "registrationForm": [ 
        { "name": "name", "form": "getName"},
        { "name": "age", "form": "getAge" }
    ]
}
```
