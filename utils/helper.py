# biblioteca para alterar as cores dos textos.
from colorama import Fore, init

init()


def show_message(message: str, size: int = 0) -> None:
    '''A mensagem fica colorida.'''
    print(Fore.MAGENTA +
          f'\n|=={(len(message)-size) * "="}==|\n|  {message}  |\n|=={(len(message)-size) * "="}==|')


def health_bar(hp: int, hpMax: int) -> str:
    '''Cria uma barra de vida no console.'''
    x = ''
    hpx = hpMax / 10
    new_hp_calc = hpx
    count = 0
    for i in range(10):
        if hp >= hpMax:
            x += 'x'
        elif hp >= new_hp_calc:
            x += 'x'
            new_hp_calc += hpx
        else:
            if count == 0:
                x += 'x'
            else:
                x += '-'

        count += 1

    return x
