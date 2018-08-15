import ldap
from ldap.controls import SimplePagedResultsControl
import sys
import ldap.modlist as modlist

def CreateUser(username, password, base_dn, fname, lname, domain, employee_num):
  """
  Create a new user account in Active Directory.
  """
  # LDAP connection
  try:
      ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
      ldap_connection = ldap.initialize(LDAP_SERVER)
      ldap_connection.simple_bind_s(BIND_DN, BIND_PASS)
  except ldap.LDAPError, error_message:
      print "Error connecting to LDAP server: %s" % error_message
      return False

  # Check and see if user exists
  try:
      user_results = ldap_connection.search_s(base_dn, ldap.SCOPE_SUBTREE,
                                              '(&(sAMAccountName=' +
                                              username +
                                              ')(objectClass=person))',
                                              ['distinguishedName'])
  except ldap.LDAPError, error_message:
      print "Error finding username: %s" % error_message
      return False

  # Check the results
  if len(user_results) != 0:
      print "User", username, "already exists in AD:", \
            user_results[0][1]['distinguishedName'][0]
      return False

  # Lets build our user: Disabled to start (514)
  user_dn = 'cn=' + fname + ' ' + lname + ',' + base_dn
  user_attrs = {}
  user_attrs['objectClass'] = \
            ['top', 'person', 'organizationalPerson', 'user']
  user_attrs['cn'] = fname + ' ' + lname
  user_attrs['userPrincipalName'] = username + '@' + domain
  user_attrs['sAMAccountName'] = username
  user_attrs['givenName'] = fname
  user_attrs['sn'] = lname
  user_attrs['displayName'] = fname + ' ' + lname
  user_attrs['userAccountControl'] = '514'
  user_attrs['mail'] = username + '@host.com'
  user_attrs['employeeID'] = employee_num
  user_attrs['homeDirectory'] = '\\\\server\\' + username
  user_attrs['homeDrive'] = 'H:'
  user_attrs['scriptPath'] = 'logon.vbs'
  user_ldif = modlist.addModlist(user_attrs)

  # Prep the password
  unicode_pass = unicode('\"' + password + '\"', 'iso-8859-1')
  password_value = unicode_pass.encode('utf-16-le')
  add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]
  # 512 will set user account to enabled
  mod_acct = [(ldap.MOD_REPLACE, 'userAccountControl', '512')]
  # New group membership
  add_member = [(ldap.MOD_ADD, 'member', user_dn)]
  # Replace the primary group ID
  mod_pgid = [(ldap.MOD_REPLACE, 'primaryGroupID', GROUP_TOKEN)]
  # Delete the Domain Users group membership
  del_member = [(ldap.MOD_DELETE, 'member', user_dn)]

  # Add the new user account
  try:
      ldap_connection.add_s(user_dn, user_ldif)
  except ldap.LDAPError, error_message:
      print "Error adding new user: %s" % error_message
      return False

  # Add the password
  try:
      ldap_connection.modify_s(user_dn, add_pass)
  except ldap.LDAPError, error_message:
      print "Error setting password: %s" % error_message
      return False

  # Change the account back to enabled
  try:
      ldap_connection.modify_s(user_dn, mod_acct)
  except ldap.LDAPError, error_message:
      print "Error enabling user: %s" % error_message
      return False

  # Add user to their primary group
  try:
      ldap_connection.modify_s(GROUP_DN, add_member)
  except ldap.LDAPError, error_message:
      print "Error adding user to group: %s" % error_message
      return False

  # Modify user's primary group ID
  try:
      ldap_connection.modify_s(user_dn, mod_pgid)
  except ldap.LDAPError, error_message:
      print "Error changing user's primary group: %s" % error_message
      return False

  # Remove user from the Domain Users group
  try:
      ldap_connection.modify_s(DU_GROUP_DN, del_member)
  except ldap.LDAPError, error_message:
      print "Error removing user from group: %s" % error_message
      return False

  # LDAP unbind
  ldap_connection.unbind_s()

  # Setup user's home directory
  os.system('mkdir -p /home/' + username + '/public_html')
  os.system('cp /etc/skel/.bashrc /etc/skel/.bash_profile ' +
            '/etc/skel/.bash_logout /home/' + username)
  os.system('chown -R ' + username + ' /home/' + username)
  os.system('chmod 0701 /home/' + username)

  # All is good
  return True