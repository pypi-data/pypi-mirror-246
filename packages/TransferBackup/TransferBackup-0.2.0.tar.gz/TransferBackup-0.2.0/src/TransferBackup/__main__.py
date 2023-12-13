from TransferBackup import main
from argparse import ArgumentParser


def transfer_backup():
    parser = ArgumentParser(
        prog='Transfer Backup',
        usage='TransferBackup',
        description='Transferring Backup to git folder.',
        epilog='Still under development'
    )

    parser.add_argument('-rm', '--remove_config', action='store_true',
                        help='Remove existing configuration file.')

    args = parser.parse_args()

    kwargs = {items[0]: items[1] for items in args._get_kwargs()}
    try:
        main(**kwargs)
    except KeyboardInterrupt:
        print('Terminating.')

