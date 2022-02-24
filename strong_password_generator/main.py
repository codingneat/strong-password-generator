
import click
from strong_password_generator.generate_strong_password import generate_strong_password
from strong_password_generator.db import add_password, get_passwords


def validate_characters_len(ctx, param, value):
    if value < 9:
        raise click.BadParameter('number of characters must be equal to 10 or greater')
    return value


@click.command()
@click.option('--site', '-s', required=True, help='site url')
@click.option('--length', '-l', default=15, type=int, callback=validate_characters_len, help='length of password')
def generate(site, length):
    password = generate_strong_password(length)
    add_password(site, password)

    print(password)


@click.command()
@click.option('--site', '-s',  required=True, help='site url')
def history(site):
    passwords = get_passwords(site)

    for password, date in passwords:
        print(f'Passsword: {password}   ---   Added: {date.strftime("%m/%d/%Y %H:%M:%S")}')
