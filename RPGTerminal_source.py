# Version 3.0

from json import dump, load
from os import stat
from random import choice, randint, randrange
from time import sleep

from colorama import Fore, init
from passlib.hash import pbkdf2_sha256 as cryp

from models.player_heal import player_heal
from utils.helper import show_message

init()

accounts_file = 'accounts.json'
enemies_file = 'enemies.json'
data_default_player = {
    "username": "",
    "password": "",
    "level": 1,
    "health": 150,
    "healthMax": 150,
    "exp": 0,
    "firstLogin": 1,
    "atkMelee": [5, 10],
    "healthPotion": 1000,
    "backpack": {}
}
data_default_enemy = {
    "name": "Bug",
    "pre1": "no",
    "pre2": "o",
    "pre3": "um",
    "health": 29,
    "healthMax": 29,
    "exp": 18,
    "atkMelee": [0, 23],
    "loot": {
        "Gold Coin": 10,
        "Cherry": 2
    }
}


def start() -> None:
    '''Aqui verifica se o arquivo json existe ou se está vazio. Se não existir ele criar e depois adiciona um conteúdo dentro dele. Se existir e não tiver conteúdo, ele adiciona algo.'''
    while True:
        try:
            if stat(accounts_file).st_size == 0:
                with open(accounts_file, 'w') as arq:
                    arq.write('[]')
                    break
            else:
                break

        except FileNotFoundError as err:
            with open(accounts_file, 'w') as arq:
                arq.write('[]')
                break

    while True:
        try:
            if stat(enemies_file).st_size == 0:
                enemies_list: list = []
                enemies_list.append(data_default_enemy)
                with open(enemies_file, 'w', encoding='utf-8') as enemies_l:
                    dump(enemies_list, enemies_l,
                         indent=4, separators=(',', ': '))
                break
            else:
                break

        except FileNotFoundError as err:
            enemies_list: list = []
            enemies_list.append(data_default_enemy)
            with open(enemies_file, 'w', encoding='utf-8') as enemies_l:
                dump(enemies_list, enemies_l, indent=4, separators=(',', ': '))
            break

    print(
        Fore.MAGENTA + '\nOlá, jogador(a)! Seja bem-vindo(a) ao Delta AVA Game! Estamos iniciando a sua jornada...')
    sleep(3)
    menu()


def menu() -> None:
    # Apenas para ajudar no desenvolvimento.
    print(Fore.BLUE + '\n========INFORMAÇÃO PROVISÓRIA========')
    account_list: list = []
    for account in read_accounts():
        account_list.append(account['username'])
    print(Fore.BLUE +
          f'Total de account(s) registrada(s): {len(account_list)}\nAccount(s): {account_list}')
    print(Fore.BLUE + '=====================================')
    # Apenas para ajudar no desenvolvimento.

    while True:
        print(Fore.YELLOW + '''\nDigite um número de acordo com o que deseja fazer:

    [ 1 ] - Entrar
    [ 2 ] - Criar uma nova conta
    [ 3 ] - Sair
        ''')
        opc: int = input('Escolha uma das opções: ')
        try:
            if int(opc) == 1:
                entrar()
                break
            elif int(opc) == 2:
                registro()
                break
            elif int(opc) == 3:
                show_message('ATÉ A PRÓXIMA!')
                sleep(2)
                break
            else:
                show_message('POR FAVOR, DIGITE A OPÇÃO CORRETA')
                sleep(2)

        except ValueError as err:
            show_message('POR FAVOR, DIGITE A OPÇÃO CORRETA')
            sleep(2)


def entrar() -> None:
    global usuario
    account_ok = 0
    password_ok = 0
    read_accounts()
    show_message('ENTRAR NO JOGO')
    usuario = input(Fore.YELLOW + '\nDigite seu usuário: ')
    senha = input('Digite sua senha: ')

    for account in accounts:
        if usuario.lower() == account['username'].lower():
            account_ok = 1
            if cryp.verify(senha, account['password']):
                password_ok = 1
                break

    if account_ok == 0:
        show_message('NÃO ENCONTRAMOS NENHUMA CONTA COM ESSE REGISTRO')
        sleep(2)
        menu()
    else:
        if password_ok == 0:
            show_message('VOCÊ DIGITOU UMA SENHA ERRADA')
            sleep(2)
            menu()
        else:
            # Verificar se os dados estão ok.
            check_default()
            for account in accounts:
                if usuario.lower() == account['username'].lower():
                    if int(account['firstLogin']) == 1:
                        account['firstLogin'] = 0
                        update_data()
                        show_message(
                            f'OLÁ {usuario.upper()}, SEJA MUITO BEM VINDO(A) AO JOGO!')
                        sleep(2)
                    else:
                        show_message(
                            f'OLÁ {usuario.upper()}, É BOM TE VER POR AQUI NOVAMENTE!')
                        sleep(2)

            game()


def registro() -> None:
    while True:
        show_message('REGISTRO')
        check = 0

        read_accounts()

        usuario: str = input(Fore.YELLOW + '\nDigite seu usuário: ')
        senha: str = input('Digite sua senha: ')

        if usuario != '':
            if senha != '':
                for account in accounts:
                    if usuario.lower() == account['username'].lower():
                        show_message(
                            'ATENÇÃO! Usuário já registrado. Tente outro nome.')
                        sleep(2)
                        check = 1

                if check == 0:
                    data_default_player['username'] = usuario
                    data_default_player['password'] = cryp.hash(
                        senha, rounds=200000, salt_size=16)
                    accounts.append(data_default_player)
                    update_data()
                    show_message('REGISTRO REALIZADO COM SUCESSO!')
                    sleep(2)
                    menu()
                    break
                else:
                    menu()
                    break
            else:
                show_message('POR FAVOR, DIGITE UMA SENHA VÁLIDA')
                sleep(2)
                menu()
                break
        else:
            show_message('POR FAVOR, DIGITE UM USUÁRIO VÁLIDO')
            sleep(2)
            menu()
            break


def game() -> None:
    while True:
        show_message('ESCOLHA O QUE DESEJA FAZER:')
        print(Fore.YELLOW + '''
    1 - Status
    2 - Procurar batalha
    3 - Sair
        ''')
        opc: int = input('Escolha uma das opções: ')
        try:
            if int(opc) == 1:
                status_player()
                sleep(2)
            elif int(opc) == 2:
                search_battle()
                break
            elif int(opc) == 3:
                menu()
                break
            else:
                show_message('POR FAVOR, DIGITE A OPÇÃO CORRETA')
                sleep(2)

        except ValueError as err:
            show_message('POR FAVOR, DIGITE A OPÇÃO CORRETA')
            sleep(2)


def status_player() -> None:
    show_message('STATUS DO SEU PERSONAGEM')
    print('')

    read_accounts()
    for account in accounts:
        if usuario.lower() == account['username'].lower():
            for k, v in account.items():
                print(Fore.GREEN + f'{k}: {v}')
            break


def search_battle() -> None:
    global enemy

    for account in accounts:
        if usuario.lower() == account['username'].lower():
            player_health = int(account['health'])
            if player_health > 0:
                enemy = choice(read_enemies())

                show_message(
                    f'VOCÊ ENCONTROU {enemy["pre3"].upper()} {enemy["name"].upper()} COM {enemy["health"]} DE VIDA!')
                sleep(1)

                while True:
                    fight: str = input(
                        Fore.RED + '\nDeseja continuar com esta batalha? (S para sim ou N para não): ')
                    try:
                        if fight.upper() == 'S':
                            battle()
                            break
                        elif fight.upper() == 'N':
                            game()
                            break
                        else:
                            show_message(
                                'Por favor, digite S ou N para continuar.')
                            sleep(2)

                    except ValueError as err:
                        show_message(
                            'Por favor, digite S ou N para continuar.')
                        sleep(2)
            else:
                show_message(
                    'Seu personagem está morto mas você ainda pode se curar.')
                sleep(1)
                player_healthPotion = int(account['healthPotion'])
                player_healthMax = int(account['healthMax'])
                if player_healthPotion > 0:
                    potion_now = player_heal(player_healthPotion)
                    if potion_now != player_healthPotion:
                        account['health'] = player_healthMax
                        account['healthPotion'] = potion_now
                        update_data()
                        show_message(
                            f'Sua vida foi restaurada e voltou a ter {player_healthMax} de vida!')
                        sleep(1)
                        game()
                    else:
                        show_message(
                            'Para continuar batalhando, cure seu personagem.')
                        sleep(2)
                        game()
                else:
                    show_message(
                        'Você não tem mais poções de cura e seu personagem está morto.')
                    sleep(2)
                    game()


def battle() -> None:
    enemy_dead = 0
    player_dead = 0
    # ADAPTAR SORTEIO PARA QUEM ATACA PRIMEIRO
    # POR ENQUANTO O PLAYER ESTÁ COMEÇANDO O ATAQUE
    # turn = ['enemy', 'player']
    # if turn[randrange(len(turn))] == 'player':
    while int(enemy['health']) > 0:
        read_accounts()
        for account in accounts:
            if usuario.lower() == account['username'].lower():

                player_health = int(account['health'])
                player_healthMax = int(account['healthMax'])
                player_exp = int(account['exp'])
                player_dmg = randint(
                    int(account['atkMelee'][0]), int(account['atkMelee'][1]))
                player_healthPotion = int(account['healthPotion'])
                enemy_health = int(enemy['health'])
                enemy_new_health = enemy_health - player_dmg
                enemy_exp = int(enemy['exp'])
                enemy_dmg = randint(
                    int(enemy['atkMelee'][0]), int(enemy['atkMelee'][1]))

                print(
                    Fore.CYAN + f'\n============================================================')
                if player_dead == 0:
                    if enemy_new_health <= 0:
                        enemy_new_health = 0
                        print(
                            Fore.CYAN + f'Seu último dano {enemy["pre1"]} {enemy["name"]} foi {player_dmg} e você {enemy["pre2"]} matou!')
                        sleep(1)
                        print(
                            Fore.CYAN + f'VOCÊ GANHOU {enemy_exp} DE EXPERIÊNCIA E SUA VIDA FOI RESTAURADA.')
                        sleep(2)
                        account['health'] = player_healthMax
                        account['exp'] = player_exp + enemy_exp
                        enemy_dead = 1
                        sleep(1)

                    elif player_dead == 0:
                        print(
                            Fore.CYAN + f'Seu dano {enemy["pre1"]} {enemy["name"]} foi {player_dmg} e {enemy["pre2"]} deixou com {enemy_new_health} de vida.')
                        enemy['health'] = enemy_new_health
                        sleep(1)

                if enemy_dead == 0:
                    if player_dead == 0:
                        player_new_health = player_health - enemy_dmg
                        account['health'] = player_new_health
                        if enemy_dmg > 0:
                            print(
                                Fore.CYAN + f'{enemy["pre2"].upper()} {enemy["name"]} te deu um dano de {enemy_dmg}.')
                            sleep(1)
                            if player_new_health <= 0:
                                account['health'] = 0
                                print(Fore.CYAN + 'Você morreu!')
                                sleep(2)
                                player_dead = 1
                            else:
                                print(
                                    Fore.CYAN + f'Sua vida era {player_health} e passou a ser {player_new_health}.')
                                sleep(1)
                                if player_healthPotion > 0:
                                    potion_now = player_heal(
                                        player_healthPotion)
                                    if potion_now != player_healthPotion:
                                        account['health'] = player_healthMax
                                        account['healthPotion'] = potion_now
                                        show_message(
                                            f'Sua vida foi restaurada e voltou a ter {player_healthMax} de vida!')
                                        sleep(1)

                        else:
                            print(
                                Fore.CYAN + f'{enemy["pre2"].upper()} {enemy["name"]} errou o ataque em você.')
                            sleep(1)
                print(
                    Fore.CYAN + f'============================================================')

                update_data()

        if enemy_dead == 1 or player_dead == 1:
            game()
            break


def update_data() -> None:
    with open(accounts_file, 'w', encoding='utf-8') as acc:
        dump(accounts, acc, indent=4, separators=(',', ': '))


def read_accounts() -> list:
    global accounts
    with open(accounts_file, encoding='utf-8') as acc:
        accounts = load(acc)

    return accounts


def read_enemies() -> list:
    global enemies
    with open(enemies_file, encoding='utf-8') as en:
        enemies = load(en)

    return enemies


def check_default() -> None:
    cache = 0
    read_accounts()

    for k, v in data_default_player.items():
        for account in accounts:
            if usuario.lower() == account['username'].lower():
                if k not in account.keys():
                    account[k] = v
                    print(Fore.GREEN +
                          f'A chave "{k}" com o valor "{v}" foi adicionado.')
                    cache = 1

    if cache:
        update_data()
        show_message('Dados Default foram atualizados.')
        sleep(1)


if __name__ == '__main__':
    start()
