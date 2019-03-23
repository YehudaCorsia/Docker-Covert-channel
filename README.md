
# Docker covert channel

This repository shows new [Covert channel](https://en.wikipedia.org/wiki/Covert_channel) that i found in Docker environment.

You are more then welcome [watch the video](https://youtu.be/n5sFaDJyeIQ) that show the use of this code.

Hebrew speakers are invited to read the article that will be published soon in [digital whisper](https://www.digitalwhisper.co.il/).

# Ways to check this :

 
**You can use images that i build, by running this commands from two terminals.**

    docker run --network=none -it yehudacorsia/docker-covert-channel-sender

and 

    docker run --network=none -it yehudacorsia/docker-covert-channel-reciver 
    
**or build this by yourself from [here](https://github.com/YehudaCorsia/Docker-Covert-channel/tree/master/src/Dockerfiles)**.

**or just create two containers and run the scripts from [here]**(https://github.com/YehudaCorsia/Docker-Covert-channel/tree/master/src).