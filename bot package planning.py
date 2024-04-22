# Loose functions

def timenow():
    """copy from an older project"""


# Userbase class, for dicts of users arranged by userid

class Userbase:
    def __init__(self):
        """search for file
        make a new file if it doesn't exist'
        save its data to self.data if it does
        create a snapshot of its structure to be saved as self.structure, which is remade whenever anything changes
        self.filename is the name of the json file
        self.name is the name of the userbase"""

    def user(self, display_name=None, nickname=None, user_id=None):
        """Search for a user's data within the userbase using any of the above identifiers. Returns error if none are
        given. Returns user entry in the script"""

    def get_userid(self, display_name=None, nickname=None):
        """Search for a user's data within the userbase using any of the above identifiers, and use that to find the
        user's userid to be used in other functions"""

    def add_user(self, user_object):
        """Add the user to the userbase using the default format initial format"""

    def edit_user_data(self, userid, new_value, field, subfield=None, subsubfield=None, subsubsubfield=None):
        """Replace the value in the field with a new one. Can also be used to add to a list or dict if given
        a location that does not exist yet"""

    def remove_user_data(self, userid, field, subfield=None, subsubfield=None, subsubsubfield=None):
        """Remove the list element or dict key from the user data"""

    def get_from_all_users(self, field, subfield=None, subsubfield=None, subsubsubfield=None):
        """Get the desired information from all users and return it as a dict of userid:value. Return an error
        if not present in all user dicts."""

    def save(self):
        """Save any changes to self.data to the json permanently"""


