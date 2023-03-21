"""
Command to import data from a JSON file into the ReferralUser models in the database.
"""

from django.core.management.base import BaseCommand, CommandError
from referral_users.models import ReferralUser
from referral_users.utils import *
import json


class Command(BaseCommand):
    """
    Django command to import data from a JSON file into the ReferralUser models in the database.
    """

    help = 'Import data from a JSON file into the database'

    def add_arguments(self, parser):
        """
        Adds command line arguments to the parser.
        """
        parser.add_argument('file_path', type=str,
                            help='Path to the JSON file')

    class ProgressPrinter():
        """
        Progress printer.
        """
        def __init__(self, step_name: str, step_count: int):
            self.step_name = step_name
            self.step_count = step_count
            self.last_progress = -1
            self.cur_step = 0
            
        def print_step_progress(self):
            """
            Print progress updates.
            """
            progress = int(self.cur_step / self.step_count * 100) + 1
            last_progress = self.last_progress
            self.last_progress = progress 
            self.cur_step += 1
            if progress == last_progress:
                return
            progress_str = f"{self.step_name}...: [{'=' * int(progress / 5)}{' ' * (20 - int(progress / 5))}] {progress}%"
            end = '\r'
            if progress == 100:
                end = '\n'
            print(progress_str, end=end)
            
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

        step_count = calculate_data_size(parent)

        # calculate levels
        printer = self.ProgressPrinter("Processing data",step_count)

        users_to_save = []

        def process_node(parent, node):
            """
            Recursively processes each node in the tree, creating ReferralUser objects
            """
            children = []
            this = ReferralUser(
                id=node['id'],
                referrer=parent,
            )
            users_to_save.append(this)
            printer.print_step_progress()
            team_size = len(node['refs'])
            for ref in node['refs']:
                children.append(process_node(this, ref))
                team_size += len(ref['refs'])
            calculate_referrals_level(this, children, team_size)
            return this

        # Iterate over users three to create users and compute their levels
        process_node(None, parent)

        # Iterate over all users to top up balance
        printer = self.ProgressPrinter("Fill balance",step_count)

        for user in users_to_save:
            top_up_120_balance(user)
            printer.print_step_progress()
        
        ReferralUser.objects.bulk_create(users_to_save)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
