# Docker covert channel

This repository shows new [Covert channel](https://en.wikipedia.org/wiki/Covert_channel) that i found in Docker environment.

You are more then welcome [watch the video](https://youtu.be/n5sFaDJyeIQ) that show the use of this code.

Hebrew speakers are invited to read the article that will be published soon in [digital whisper](https://www.digitalwhisper.co.il/).

# Using containers to check this :
You are more then welcome to check this by run the commands :

    docker run --network=none -it yehudacorsia/docker-covert-channel-sender

and 

    docker run --network=none -it yehudacorsia/docker-covert-channel-reciver 

in two terminals  and see the magic happen :-)

