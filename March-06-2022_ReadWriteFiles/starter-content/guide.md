# How to read files
Every language / framework has some way to work with files. In python we have the `open` function! 

Lets take this example.txt file and learn how to read from it!

**Example.txt**:
```txt
Sword
Shield
Health Potion
```

In every language it is **imperative** to clean up after yourself. If you open a file you **need** to close it when you're done! 
This goes with **any** IO operation.

One way to open a file, which I commonly see
```python
file = open("example.txt")
contents = file.readlines()
```

This is bad! The file doesn't get closed! We could either (1) manually close it or (2) use the `with` operator!

**manually close**:
```python
file.close()
```

The `with` operator will automatically dispose/cleanup things once we're `out of scope`. 
**with operator**:
```python
with open("example.txt") as file:
    # anything at this indentation level
    # or to the right would be considered 'in scope'
    contents = file.readlines()
# the file is automatically closed for us at this point!
```

Loading the entirety of a file into memory could be problematic for larger files. Heck, if you're on a device with little RAM you need to use
as **little** as possible! In this scenario you'll want to read line-by-line.

```python
with open("example.txt") as file:
    while True:
        current_line = file.readline()

        # if we reached the end (because current_line will be None) - exit loop
        if not current_line:
            break
        
        print(current_line.strip()) # we need to strip this line otherwise we'll get the special characters such as newline (\n).
```

# How to write to files

The `open` function we learned above has a few options available to us. We can specify a second argument which defines the behavior / accessibility of said file. In regard to writing we'll be looking at 3 different flags.

| Flag | Description                                                                |
| ---- |----------------------------------------------------------------------------|
| "x" | Will create file. Throws error if the file already exists                  |
| "a" | Append to file, creates file if it doesn't exist                           |
| "w" | Write. Creates file if it doesn't exist. This WILL overwrite existing file |

Create file
```python
with open("test.txt", "x") as file:
    file.write("\n".join(["shield", "bow", "health potion"]))
```

Contents of `test.txt` after
```md
shield
bow
health potion
```

Append file
```python
with open("test.txt", "a") as file:
    file.write("\n".join(["boots", "helmet"]))
```

Contents of `test.txt` after
```md
shield
bow
health potion
boots
helmet
```

Write to file
```python
with open("test.txt", "w") as file:
    file.write("oops")
```

Contents of `test.txt` after
```md
oops
```
----
# Algorithms! + Yield
Ever find yourself creating these massive functions? Separating areas of responsibility can help improve readability. In some cases we might find ourselves going over the SAME content MULTIPLE TIMES. For obvious reasons this is not ideal. 

To many people, if I have a list of 10 items they'll say it's not a problem. Well, technically no it's not that big of a problem. However, it's not a mindset you want to fall into. What happens when that SAME list becomes 1000 items? 10,000 items? Meanwhile you had an algorithm which goes through this `list` 5 times?

Let's look at this. If my algorithm for some reason goes through a list 5 times... for whatever reason. It is 5n meaning 5 times the size of the list.

| Size of list | Number of times |
|--------------|-----------------|
| 10           |  50 |
| 100 | 500 |
| 1000 | 5000 |
| 5000 | 25000 |

Computers are fast yes... but when we start getting up to the millions we're wasting precious resources!

## Yield
Lets take a CSV file. Some individuals might consume the entire file, lets say 1000 lines and THEN go over it again to parse it and do something with this data. Effectively making it at least 2n in terms of complexity. Maybe more. One way we can introduce separation of concerns and maintain our performance is by using the `yield` operator.
This operator basically says "at this point in time I will return this item to the caller". Rather than talk about it lets show it in action

**example.csv**
```md
shield,10
bow,5
arrows,100
```

```python
def ingest_market(filepath: str) -> list:
    with open(filepath) as file:
        while True:
            current_line = file.readline()

            # end of file
            if not current_line:
                break
                
            yield current_line.strip().split(',')

for item in ingest_market("example.csv", "r"):
    print(f"We have {item[1]} of {item[0]} in stock!")
```

We get the benefit of sanitizing and reading data in one method while actually consuming it and doing something with in another! All without going over the SAME content again and again!!!!!!!!! Awesome isn't it?