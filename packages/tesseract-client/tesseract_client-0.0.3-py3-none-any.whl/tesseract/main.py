import os
import argparse
import getpass
import keyring
import configparser
from pathlib import Path
from loguru import logger

from watchdog.observers.polling import PollingObserver as Observer

from tesseract.settings import API_URL
from tesseract.db_manager import DBManager
from tesseract.services import Services
from tesseract.monitoring import FileChangeHandler
from tesseract.api_manager import APIManager


class NotLoggedInError(Exception):
    def __init__(self):
        super().__init__("You are not logged in. Please run 'tesseract login'")


def create_db_path_if_not_exists(db_path: str) -> None:
    """ Create the full path to the database file if it doesn't exist"""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created database path: {db_path}")


def create_index_folder_if_not_exists(index_folder_path: str) -> None:
    """ Create the full path to the index folder if it doesn't exist"""
    index_folder_path = Path(index_folder_path)
    index_folder_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created index folder path: {index_folder_path}")


def run(indexed_folder: str, db_path: str, api_url: str):
    """ Start the monitoring process """
    username, password = get_credentials()

    db_path = os.path.expanduser(db_path)
    indexed_folder = os.path.expanduser(indexed_folder)

    api_urls = API_URL(base=api_url)

    create_index_folder_if_not_exists(indexed_folder)
    create_db_path_if_not_exists(db_path)

    with DBManager(db_path) as db_manager:
        api_manager = APIManager(
            username=username,
            password=password,
            api_urls=api_urls
        )
        # chunk_size = api_manager.get_chunk_size()
        chunk_size = 1000
        services = Services(
            api_manager=api_manager,
            db_manager=db_manager,
            indexed_folder=indexed_folder,
            chunk_size=chunk_size
        )
        event_handler = FileChangeHandler(services)

        # Check for changes that were made while offline
        services.check_for_offline_changes()

        # Pull updates from the server
        services.pull()

        # Start monitoring the folder for changes
        observer = Observer()
        observer.schedule(
            event_handler,
            path=indexed_folder,
            recursive=True
        )
        observer.start()
        logger.info(f"Monitoring folder {indexed_folder} for updates...")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
            logger.info("Monitoring stopped due to KeyboardInterrupt")

        observer.join()


def login(username: str = None, password: str = None):
    """ Store the username and password in the config file and keyring """
    if username is None:
        username = input('Username: ')
    if password is None:
        password = getpass.getpass('Password: ')
    config = configparser.ConfigParser()
    config.read('config.ini')
    config['CREDENTIALS'] = {'username': username}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    keyring.set_password('tesseract', username, password)


def get_default_settings() -> dict:
    """ Get the default settings from the config file"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']


def get_credentials() -> tuple[str, str]:
    """ Get the username and password from the config file and keyring """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        username = config['CREDENTIALS']['username']
        password = keyring.get_password('tesseract', username)
        return username, password
    except KeyError:
        raise NotLoggedInError


def exclude_add(folders: list[str]):
    # Add your logic here to add folders to the exclude list
    print(f"Added {', '.join(folders)} to the exclude list")


def exclude_remove(folders: list[str]):
    # Add your logic here to remove folders from the exclude list
    print(f"Removed {', '.join(folders)} from the exclude list")


def main():
    defaults = get_default_settings()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # Login
    login_parser = subparsers.add_parser('login')
    login_parser.add_argument(
        '--username',
        '-u',
        help='Username to use for authentication',
        type=str
    )
    login_parser.add_argument(
        '--password',
        '-p',
        help='Password to use for authentication',
        type=str
    )

    # Run
    run_parser = subparsers.add_parser('run')
    run_parser.add_argument(
        '--path',
        help='Folder to index',
        type=str,
        default=defaults['index_path']
    )
    run_parser.add_argument(
        '--db',
        help='Path to database file',
        type=str,
        default=defaults['db_path']
    )
    run_parser.add_argument(
        '--api_url',
        help='URL of the API',
        type=str,
        default=defaults['api_url']
    )

    # Exclude
    exclude_parser = subparsers.add_parser('exclude')
    subsubparser = exclude_parser.add_subparsers(dest='exclude_command')

    # Exclude add
    exclude_add_parser = subsubparser.add_parser('add')
    exclude_add_parser.add_argument(
        'FOLDER',
        help='Folder to exclude',
        type=str,
        nargs='+'
    )

    # Exclude remove
    exclude_remove_parser = subsubparser.add_parser('remove')
    exclude_remove_parser.add_argument(
        'FOLDER',
        help='Folder to remove from excluded folders',
        type=str,
        nargs='+'
    )

    args = parser.parse_args()

    if args.command == 'login':
        login(args.username, args.password)
    elif args.command == 'run':
        run(args.path, args.db, args.api_url)
    elif args.command == 'exclude':
        if args.exclude_command == 'add':
            exclude_add(args.FOLDER)
        else:
            exclude_remove(args.FOLDER)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
