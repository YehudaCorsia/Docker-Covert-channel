

# Docker covert channel

This repository shows new [Covert channel](https://en.wikipedia.org/wiki/Covert_channel) vulnerability that I found in Docker environment.

You can check this  [video](https://youtu.be/Zh4gNfVhnl8) that shows my exploitation of this vulnerability.

some screenshots:

![Scrren shot 1](https://github.com/YehudaCorsia/Docker-Covert-channel/blob/master/docs/Screenshots/From%20Fedora/Screenshot%201.png)

![Scrren shot 2](https://github.com/YehudaCorsia/Docker-Covert-channel/blob/master/docs/Screenshots/From%20Fedora/Screenshot%202.png)

Hebrew speakers are welcome to read my article that was published in [digital whisper](https://www.digitalwhisper.co.il/files/Zines/0x69/DW105-2-CovertDocker.pdf).

# Using this project :

 
**You can use my images, by running these commands from two terminals.**

    docker run --network=none -it yehudacorsia/docker-covert-channel-sender
and 

    docker run --network=none -it yehudacorsia/docker-covert-channel-receiver 
    
**or build it by yourself from [here](https://github.com/YehudaCorsia/Docker-Covert-channel/tree/master/src/Dockerfiles)**.

**or just create two containers and run the [scripts](https://github.com/YehudaCorsia/Docker-Covert-channel/tree/master/src).**
