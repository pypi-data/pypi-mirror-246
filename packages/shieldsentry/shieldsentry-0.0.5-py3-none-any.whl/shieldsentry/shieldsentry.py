import os
import json
import re

class ShieldSentry:
    def __init__(self, specification="specifications.json"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        specifications_path = os.path.join(current_dir, specification)
        with open(specifications_path, 'r') as file:
            self.specification = json.load(file)

        # Initialize access control settings
        self.roles = self.specifications["accessControl"]["roles"]
        self.permissions = self.specifications["accessControl"]["permissions"]

    def validate(self, input_type, value):
        rules = self.specification['inputTypes'][input_type]
        # Implementing basic validation logic
        if 'maxLength' in rules and len(value) > rules['maxLength']:
            return False
        if 'regex' in rules and not re.match(rules['regex'], value):
            return False
        if input_type == 'numeric':
            if (value < rules['min']) or (value > rules['max']):
                return False
        return True

    def html_escape(self, value):
        escape_chars = self.specification['sanitization']['HTML']['escapeCharacters']
        for char, escaped_char in escape_chars.items():
            value = value.replace(char, escaped_char)
        return value

    def sql_escape(self, value):
        escape_chars = self.specification['sanitization']['SQL']['escapeCharacters']
        for char, escaped_char in escape_chars.items():
            value = value.replace(char, escaped_char)
        return value

    def sanitize(self, context, value):
        if context == 'HTML':
            return self.html_escape(value)
        elif context == 'SQL':
            return self.sql_escape(value)
        else:
            # Default or unknown context: return value as is
            return value

    def handle_error(self, error_type):
        error = self.specification['errors'][error_type]
        print(f"Error {error['code']}: {error['message']}")

    def has_permission(self, user_role, action):
        """
        Check if a user role has permission to perform an action.
        """
        if user_role not in self.roles:
            return False

        allowed_actions = self.permissions.get(user_role, [])
        if "all" in allowed_actions or action in allowed_actions:
            return True

        return False