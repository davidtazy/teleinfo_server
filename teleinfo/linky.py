from abc import ABC, abstractmethod
import logging
import time
import serial


class Linky(ABC):
    @abstractmethod
    def next_line(self) -> bytes:
        pass


class LinkySerial(Linky):
    def __init__(self, serial_port: str) -> None:
        super().__init__()
        logging.info(f"connecting to {serial_port} ...")
        self.serial = serial.Serial(
            port=serial_port,
            baudrate=1200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS,
            timeout=1,
        )

        logging.info(f"synchronize  to {serial_port} ...")
        # boucle pour partir sur un début de trame
        line = self.serial.readline()
        while b"\x02" not in line:  # recherche du caractère de début de trame
            line = self.serial.readline()
        logging.info(f"...synchronized  to {serial_port} ")

    def __del__(self):
        self.serial.close()

    def next_line(self) -> bytes:
        line = self.serial.readline()
        logging.debug("line received:")
        logging.debug(line)
        return line


class Teleinfo:
    def __init__(self, linky: Linky) -> None:
        self.linky = linky

    def next_msg(self):

        trame = {}
        finish = False
        while not finish:
            line = self.linky.next_line()
            finish, trame = decode_line(line, trame)
        return trame


def decode_line(line: bytes, trame):

    INT_MESURE_KEYS = [
        "BASE",
        "IMAX",
        "HCHC",
        "IINST",
        "PAPP",
        "ISOUSC",
        "ADCO",
        "HCHP",
        "BBRHCJB",
        "BBRHPJB",
        "BBRHCJW",
        "BBRHPJW",
        "BBRHCJR",
        "BBRHPJR",
    ]

    line_str = line.decode("utf-8")

    try:
        # separation sur espace /!\ attention le caractere de controle 0x32 est un espace aussi
        [key, val, *_] = line_str.split(" ")

        # supprimer les retours charriot et saut de ligne puis selectionne le caractere
        # de controle en partant de la fin
        checksum = (line_str.replace("\x03\x02", ""))[-3:-2]

        if verif_checksum(f"{key} {val}", checksum):
            # creation du champ pour la trame en cours avec cast des valeurs de mesure en "integer"
            trame[key] = int(val) if key in INT_MESURE_KEYS else val

        if (
            b"\x03" in line
        ):  # si caractère de fin dans la ligne, on insère la trame dans influx

            if "ADCO" in trame:
                del trame["ADCO"]  # adresse du compteur : confidentiel!
            time_measure = time.time()
            trame["timestamp"] = int(time_measure)
            logging.debug("trame read:")
            logging.debug(trame)

            return True, trame
    except Exception as e:
        logging.error("Exception : %s" % e, exc_info=True)
        logging.error("%s %s" % (key, val))
        return True, trame

    return False, trame


def verif_checksum(data, checksum):
    data_unicode = 0
    for caractere in data:
        data_unicode += ord(caractere)
    sum_unicode = (data_unicode & 63) + 32
    return checksum == chr(sum_unicode)
