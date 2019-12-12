import ldap3
from ldap3 import Server, Connection, ALL

# LDAP Settings
USER_DN = ''
PASSWORD = ''
SERVER = ''
SEARCH_BASE = ''
SEARCH_FILTER = ''


def format_string(string):
    """
    1. Remove special characters
    2. Remove spaces
    3. Convert OU to lower
    Parameters:
        string      String to convert
    """
    return ''.join(e.lower() for e in string if e.isalnum())


def extract_results(entries):
    """
    Utility method to do the following:
    1. Take a list of LDAP entries
    2. Extract ou attribute
    3. Format the string using format_string method
    4. Return the results in array
    Parameters:
        entries     List of ldap entries
    """
    results = []
    for entry in entries:
        # Get the 'attributes' from item 1 in tuple
        obj = entry[1]
        # Send the OU to format_string method
        ou = format_string(obj['ou'][0])
        # Add result to results list
        results.append(ou)
    # Return the results
    return results


class LdapController:
    """
    Controller to assist with Ldap connections and methods
    1. Bind to ldap SERVER using USER_DN and PASSWORD
    2. Search for objectClass=organizationalUnit
    """
    # LDAP Server and Connection
    server = Server(SERVER, get_info=ALL)
    connection = Connection(server, user=USER_DN, password=PASSWORD)
    search_result = None

    def search_ou(self):
        """
        Perform a search against the LDAP
        """
        # Perform the search on ldap
        self.connection.search(
            search_base=SEARCH_BASE,
            search_filter=SEARCH_FILTER,
            search_scope=ldap3.SUBTREE,
            attributes=ldap3.ALL_ATTRIBUTES,
        )
        # Get entries from connection.response, using list comprehension extract attributes and dn
        entries = [(e['dn'], e['attributes']) for e in self.connection.response]

        # Search results will be the value of extract_results which is a list
        self.search_result = extract_results(entries)

    def __init__(self):
        """
        Upon creating the class we will do the following:
        1. Bind to LDAP with settings provided
        2. Initiate the search against ou's
        """
        if not self.connection.bind():
            raise TypeError(
                'Could not bind to LDAP with\r\nUsername: {}\r\nServer: {}'.format(
                    USER_DN,
                    SERVER
                )
            )
        else:
            # If successfully connected to LDAP, perform search
            self.search_ou()


# CLI
if __name__ == '__main__':
    # Create the LdapController
    ldap_search = LdapController()

    # Get the results of the search
    print(ldap_search.search_result)

