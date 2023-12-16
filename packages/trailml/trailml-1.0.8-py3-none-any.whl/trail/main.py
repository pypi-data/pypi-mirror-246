import argparse
import traceback

import sentry_sdk

from trail import libconfig
from trail.exception.trail import RemoteTrailException
from trail.userconfig.init import init_environment
from trail.util import uploads
from trail.util.new_experiment import add_new_experiment
from trail.util.upload_artifacts_from_notebook import \
    upload_artifacts_from_notebook


def handle_exception(e: Exception):
    if libconfig.is_development_environment():
        traceback.print_exc()
    else:
        sentry_sdk.capture_exception(e)

    print(e)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Trail CLI')
    parser.add_argument(
        '--upload-folder', '-u',
        required=False,
        help='Upload the specified folder to trail'
    )

    parser.add_argument(
        '--upload-file', '-f',
        required=False,
        help='Upload the specified file to trail'
    )

    parser.add_argument(
        '--upload-notebook-artifact', '-a',
        required=False,
        help='Upload the jupyter notebook to trail and add outputs as artifacts'
    )

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser(
        'init',
        help='Initialize a new trail environment. '
             'This will create a new configuration file in the current directory.'
    )

    subparsers.add_parser(
        'add-new-experiment',
        help='Add a new experiment to trail'
    )

    args = parser.parse_args()

    if args.command == 'init':
        try:
            init_environment()
        except RemoteTrailException as e:
            handle_exception(e)
    elif args.command == 'add-new-experiment':
        try:
            add_new_experiment()
        except RemoteTrailException as e:
            handle_exception(e)
    else:
        if args.upload_file:
            print(f'Uploading file: {args.upload_file}')

            try:
                uploads.upload_file(args.upload_file)
            except RemoteTrailException as e:
                handle_exception(e)
        elif args.upload_folder:
            try:
                uploads.upload_folder(args.upload_folder)
            except RemoteTrailException as e:
                handle_exception(e)
            except FileNotFoundError as e:
                print(e)
        elif args.upload_notebook_artifact:
            print(
                f'Uploading notebook artifact: {args.upload_notebook_artifact}')
            try:
                uploads.upload_file(args.upload_notebook_artifact)
                upload_artifacts_from_notebook(args.upload_notebook_artifact)
            except RemoteTrailException as e:
                handle_exception(e)
        else:
            parser.print_help()


def main():
    parse_arguments()


if __name__ == "__main__":
    main()
