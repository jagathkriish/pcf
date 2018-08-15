import ldap

val = 'venkatesh'
con = ldap.initialize('ldap://localhost:10389', bytes_mode=False)
con.simple_bind_s(u'cn=jagathpathi,ou=users,dc=example,dc=com', u'0787')
results = con.search_s(u'ou=Groups,dc=example,dc=com', ldap.SCOPE_SUBTREE , u"(cn=admin)")

print(results)