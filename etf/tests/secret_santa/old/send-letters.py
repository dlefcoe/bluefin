import argparse
import random
import re

import config
from santa import Santa


class SecretSantaError(Exception):
    pass


def is_santa_list_compatible(santas_lst):
    for k in range(len(santas_lst)):
        a = k % len(santas_lst)
        b = (k + 1) % len(santas_lst)

        santa, recipient = santas_lst[a].name, santas_lst[b].name

        if santa in config.incompatibles and \
                recipient in config.incompatibles[santa]:
            return False

    return True


def send_letter(santa, dry_run):
    message = config.letter.get_email_message(santa)

    with open(config.record_file, 'a') as f:
        f.write(message)
        f.write('*' * 80 + '\n')

    if dry_run:
        print(santa)
    else:
        config.letter.send(santa)


def set_recipients(santas):

    for k in range(len(santas) - 1):
        santas[k].recipient = santas[k+1]

    santas[-1].recipient = santas[0]


def parse_arguments():
    parser = argparse.ArgumentParser(
              description='Auto-send Secret Santa letters!')

    parser.add_argument('--official',
        dest='official',
        action='store_true',
        help='Actually send email (and not dump to output)')

    parser.add_argument('--test-email',
        dest='test_email',
        action='store_true',
        help='Send a test email to check configuration')

    return parser.parse_args()


def check_emails(santas):
    email_regex = r'[^@\s]+@[a-zA-Z0-9\-]+(\.[a-zA-Z0-9]+)+$'

    for santa in santas:
        if not re.match(email_regex, santa.email):
            raise SecretSantaError(
                    f'{santa.name} has an invalid email: {santa.email}')


def check_compatibilities(santas):
    santa_names = tuple(map(lambda s: s.name, santas))

    for name in config.incompatibles:
        if name not in santa_names:
            raise SecretSantaError(
                    f'Unknown santa in incompatible list: {name}. ' \
                     'Please check spelling')

        for incompatible_recipient in config.incompatibles[name]:
            if incompatible_recipient not in santa_names:
                raise SecretSantaError(
                        f'Unknown incompatible recipient for {name}: ' \
                        f'{incompatible_recipient}. Please check spelling.')


        if not isinstance(config.incompatibles[name], tuple):
            raise SecretSantaError(
                    f'The incompatible list for {name} must be a tuple')

        num_incompatible_recipients = len(config.incompatibles[name])
        num_possible_recipients = len(santas) - 1 - num_incompatible_recipients

        if num_possible_recipients == 0:
            raise SecretSantaError(
                    f'{name} has no option for a recipient! Check the ' \
                    '\'incompatibles\' list in the configuration file.')


def secret_santa(args):
    santas = config.santas

    check_emails(santas)
    check_compatibilities(santas)

    # Clear contents of the file
    open(config.record_file, 'w').close()
    
    while True:
        random.shuffle(santas)

        if is_santa_list_compatible(santas):
            break

    set_recipients(santas)

    dry_run = not args.official

    for k in sorted(santas):
        send_letter(k, dry_run)

    print('\nFinished!\n')
    print('Mail record saved to: {}'.format(config.record_file))


def send_test_email():
    test_santa = Santa('Test Santa', config.smtp_user)
    test_recipient = Santa('Test Recipient', 'test@example.com')
    test_santa.recipient = test_recipient
    config.letter.send(test_santa)


def main():
    args = parse_arguments()

    if args.test_email:
        send_test_email()
    else:
        secret_santa(args)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Uh oh, something failed: {}'.format(e))