# Docker

## Build / Dockerfile

A `dockerfile` defines all the things one has to do in order to get your environment setup. If we wanted to host a python website, we'd have to execute
a series of commands to install all necessary packages, copy source code, and configure stuff. At the end we define an `entrypoint` or the command that runs when the container
starts up. This could be as simple as `python app.py`. Nothing wild is going on here.

When the build process is completed you're left with an image. In laymen terms it is the equivalent of a snapshot for a virtual machine. 

Lets dive into how to build a docker file.

Every dockerfile is built using some sort of `base image`. This is defined using the `FROM` keyword. In our example we'll use the `python` image using version `latest` - which is
actually referred to as a `tag` when working with docker. When a tag is not provided it by default uses the `latest` tag.

```dockerfile
# assumes latest
FROM python

# defined latest tag
FROM python:latest

# using 3.8 tag instead (don't confuse it with version... even though that's technically how this is used) 
FROM python:3.8
```

Anyhow, lets start building our docker file to host our basic flask application! Inside of the `starter` folder create a new file called `dockerfile`. That's it... no extension

```dockerfile
FROM python

# we're informing our build context that 
# this is our current working directory
WORKDIR /app

# we're telling flask that this is the file to use at startup
ENV FLASK_APP app.py

# copies requirements.txt from host into our /app directory as requirements.txt
COPY requirements.txt requirements.txt

# copies our files from host into the workdir of /app
COPY . .

# for our test environment our python app uses 5000 so we'll expose it 
# so we can map it to something else externally
EXPOSE 5000

# python3 -m flask run --host=0.0.0.0
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0" ]
```

Time to build! Open a terminal, navigate to this project directory and use the following

We're going to build our docker image and tag it as `test` and the `.` represents the current working directory will be used for our build context.
So if I was at a path /home/username/sourcecodehere --- when our docker file has `COPY . . ` it will be using `/home/username/sourcecodehere` to pull from.

```bash
docker build -t test .
```

The first time executing this command will take the longest. This is because it has to pull the `python` image from a docker repository, which in our case is dockerhub. Once this 
image is on your machine, future iterations will be significantly faster!

Images are built using `layers` which are basically like little commits. It's a history of changes that have occurred to the image overtime. The admittedly confusing part is
when viewing these layers. It might appear that each layer is 900MB in size, it's not. It's essentially the size of the image at that point in time. 

If I have 3 layers that say something like

| Layer | Size (MB) |
| --- |-----------|
| Layer 1 | 100       |
| Layer 2 | 101       |
| Layer 3 | 200       |

It's not a total of 401MB in size. It's 200MB

## Docker Container

To get a container running you need an image! We'll use the docker image built in the above process. 

Given we know the app is using port 5000 in the container, we need to tell our host how to map this port so we can use it from outside the container!

The `-d` argument indicates we want to `detach` from our container. This is important if we **do not** want docker to consume our terminal! Detaching allows us to continue
using our terminal without having to create a new one. 

The `-p` argument indicates our host port followed by a `:` and the port inside our container. In this case we're mapping the host port `5123` to `5000` in our container.

Furthermore, we're giving our container a custom name of `flask-test-container`. It's worth noting that you should avoid underscores when naming things.... try to stick to URL friendly
formats by using a hyphen to separate things. Lastly, `test` is the name of the image we created in the build step.

```bash
docker run -d -p 5123:5000 --name flask-test-container test
```

Now you should be able to connect to our app via
`http://localhost:5123`

If you want to setup SSL to get https working, we may do a tutorial on that in the future.

### Note:
As your container is running, you might be changing / saving things locally in the container itself. It is imperative that you understand that when the container is shutdown,
you **LOSE** any changes that were made. It resets to whatever the state was at the end of the build-process. 

### Persistence
For a database container you will most likely want to keep things between each run. Well... you need to mount the data directory to your host! Suggest double-checking with your
database of choice as it can vary between MySQL, Mongo, etc.

Mongo containers have their data stored at `/data/db` inside the container. So, to make this persistent we need this folder to get mounted/saved outside the container
onto the host! To do this we utilize `volumes`. You'll probably see a path mapped to path more often than a named-volume being used? In my experience, they're mostly path to path.

If you're utilizing docker on windows, this is where pathing can get a little funky. The host pathing schema is very different from a linux container.  

| Parameter | Description |
| --- | --- |
| -d | detach |
| -p | port mapping |
| -v | indicating the volume to mount |

Linux
```bash
docker run -d -p 27017:27017 -v /home/username/data:/data/db mongo
```

Windows:
```bash
docker volume create mongodata
docker run -d -p 27017:27017 -v mongodata:/data/db mongo
```

If you have **multiple** ports or volumes you have to specify another `-p` or `-v` argument. This is where either creating a script for this becomes useful or just use `docker-compose`!

If we converted this mongo example into a `docker-compose` file

Create a file: `docker-compose.yml`
```yaml
version: "3.3"
services:
  mongodb:
    image: mongo
    container_name: my_mongo_container
    volumes:
      - mongodata:/data/db
    ports:
      - "27017:27017"

volumes:
  mongodata:
```

This also allows you to spool up multiple services at a time! Many apps require a database these days so what you could do is start the database and then your app!

Lets add our test application (even though it doesn't use a database).

```yaml
version: "3.3"
services:
  mongodb:
    image: mongo
    container_name: my_mongo_container
    volumes:
      - mongodata:/data/db
    ports:
      - "27017:27017"
  flask-test-container:
    image: test
    container_name: flask-test-container
    ports:
      - "5123:5000"
    depends_on:
      - mongodb
volumes:
  mongodata:
```

By using the `depends_on` key we can provide 1 or many services which `flask-test-container` needs in order to start! This example will start the `mongodb` container first
and then `flask-test-container`.

If you're using sql-alchemy in python you would require the database to be ready/online. This is one approach to ensuring your DB is online so you can perform the necessary migrations
for your application.
