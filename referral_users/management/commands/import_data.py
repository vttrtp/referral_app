"""
Command to import data from a JSON file into the ReferralUser and ReferralLevel models in the database.
"""

from django.core.management.base import BaseCommand, CommandError
from referral_users.models import ReferralUser, ReferralLevel
from referral_users.utils import *
import json


class Command(BaseCommand):
    """
    Django command to import data from a JSON file into the ReferralUser and ReferralLevel models in the database.
    """
    
    help = 'Import data from a JSON file into the database'

    def add_arguments(self, parser):
        """
        Adds command line arguments to the parser.
        """
        parser.add_argument('file_path', type=str,
                            help='Path to the JSON file')

    def handle(self, *args, **options):
        """
        Handles the command.
        """
        file_path = options['file_path']
        print(f"Importing file {file_path}...")
        # Open the JSON file and read the data as parent object

        with open(file_path, 'r') as file:
            parent = json.load(file)

        ReferralUser.objects.all().delete()
        ReferralLevel.objects.all().delete()

        def calculate_data_size(node):
            """
            Recursively calculates the total number of nodes in a given tree.
            """
            size = 0

            def collect_children(node):
                """
                Recursively collects all children of a given node.
                """
                nonlocal size
                size += 1
                for ref in node['refs']:
                    collect_children(ref)
            collect_children(node)
            return size

        count = calculate_data_size(parent)

        def print_progress(step_name, count, cur_step, last_progress):
            """
            Prints progress of the current step.
            """
            progress = int(cur_step / count * 100)
            if progress == last_progress:
                return progress
            progress_str = f"{step_name}...: [{'=' * int(progress / 5)}{' ' * (20 - int(progress / 5))}] {progress}%"
            print(progress_str, end='\r')
            return progress

        # calculate levels
        step_name = "Processing data"
        cur_step = 0
        last_progress = -1

        # Process node
        def process_node(parent, node):
            """
            Recursively processes each node in the tree, creating ReferralUser and ReferralLevel objects as necessary.
            """
            nonlocal cur_step, last_progress

            children = []
            level = ReferralLevel.objects.create()

            this = ReferralUser.objects.create(
                id=node['id'],
                referrer=parent,
                referral_level=level,
            )
            last_progress = print_progress(
                step_name, count, cur_step, last_progress)
            cur_step += 1
            for ref in node['refs']:
                children.append(process_node(this, ref))
            calculate_referrals_level(this)
            this.referral_level.save()
        process_node(None, parent)

        # process_node(None,parent)
        self.stdout.write(self.style.SUCCESS('Data imported successfully                         '))
