# biblioteca para alterar as cores dos textos.
from colorama import Fore, init

init()


def show_message(message: str) -> None:
    print(Fore.MAGENTA +
          f'\n|=={len(message) * "="}==|\n|  {message}  |\n|=={len(message) * "="}==|')
