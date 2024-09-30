import sys
import logging

from app import create_app

app = create_app()
logger = logging.getLogger(__name__)

def config_logging(file_name: str, console_level: int=logging.INFO, file_level: int=logging.DEBUG):
    file_handler = logging.FileHandler(file_name, mode='a', encoding="utf8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s.%(lineno)d %(name)s:\t%(message)s'
        ))
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s %(levelname)s] %(message)s',
        datefmt="%Y/%m/%d %H:%M:%S"
        ))
    console_handler.setLevel(console_level)

    logging.basicConfig(
        level=min(console_level, file_level),
        handlers=[file_handler, console_handler],
        )
    

if '__main__' == __name__:
    config_logging('app.log', logging.WARNING, logging.DEBUG)
    app.run(debug=True)