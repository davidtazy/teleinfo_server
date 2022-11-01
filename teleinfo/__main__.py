import logging
from .linky import LinkySerial, Teleinfo
from .influx import Influx, TMDB


def main():

    # config
    serial_port = "/dev/ttyAMA0"
    org = None
    url = None
    log_level = logging.ERROR

    # logger
    logging.basicConfig(
        filename="/var/log/teleinfo/releve.log",
        level=log_level,
        format="%(asctime)s %(message)s",
    )
    # logging.basicConfig( level=log_level, format='%(asctime)s %(message)s')

    logging.info("Teleinfo starting..")

    try:

        # deps
        serial = LinkySerial(serial_port=serial_port)
        teleinfo = Teleinfo(serial)
        influx = Influx(org=org, url=url)

        # main loop
        while True:
            msg = teleinfo.next_msg()
            influx.push(msg)
    except Exception as ex:
        logging.exception(ex)


if __name__ == "__main__":

    main()
