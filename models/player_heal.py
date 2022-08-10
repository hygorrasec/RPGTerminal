from colorama import Fore, init
from utils.helper import show_message

init()


def player_heal(potions: int) -> int:
    while True:
        heal = input(
            Fore.GREEN + f'\nVocê possue {potions} poções de cura, deseja usar? (S para sim ou N para não): ')
        try:
            if heal.upper() == 'S':
                potions = potions - 1
                return potions
            elif heal.upper() == 'N':
                return potions
            else:
                show_message('Por favor, digite S ou N para continuar.')

        except ValueError as err:
            show_message('Por favor, digite S ou N para continuar.')
