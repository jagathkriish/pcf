org_group_map = {'ci-org': 'org1', 'demo-org': 'org1', 'qa-org': 'org1', 'qa-space': 'org1'}

print('ci-org' in org_group_map)

data = [(u'CN=pcf_test_user_003,OU=Test,OU=PCF,OU=Offices,DC=int,DC=8451,DC=com', 
{u'primaryGroupID': ['513'], u'cn': ['pcf_test_user_003'], u'countryCode': ['0'], 
u'objectClass': ['top', 'person', 'organizationalPerson', 'user'], 
u'userPrincipalName': ['pcf_test_user_003@int.8451.com'], u'instanceType': ['4'], 
u'description': ['PCF Test User for ILM Automation Testing - see INC880775'], 
u'distinguishedName': ['CN=pcf_test_user_003,OU=Test,OU=PCF,OU=Offices,DC=int,DC=8451,DC=com'], 
u'dSCorePropagationData': ['20180727144222.0Z', '20180713184446.0Z', '16010101000001.0Z'], 
u'objectSid': ['\x01\x05\x00\x00\x00\x00\x00\x05\x15\x00\x00\x00\x1ey\x85\x05\xa8t\xc8\xfc4\x95-\xda1>\x00\x00'], 
u'whenCreated': ['20180713184431.0Z'], u'uSNCreated': ['44379405'], u'pwdLastSet': ['131759810716751735'], 
u'sAMAccountName': ['pcf_test_user_003'], u'objectCategory': ['CN=Person,CN=Schema,CN=Configuration,DC=int,DC=8451,DC=com'], 
u'objectGUID': ['\x12\x87\xe6\x18\xf3\xed\x1fE\x93*\x96)\x9a\xfaJ\xae'], u'whenChanged': ['20180713184645.0Z'], 
u'accountExpires': ['9223372036854775807'], u'displayName': ['pcf_test_user_003'], u'name': ['pcf_test_user_003'], 
u'orclCommonAttribute': ['{SSHA}4tXrczo/p1XDCxAY+Qr7bUBid1QYlPbGtlrSBg=='], 
u'memberOf': [],
u'codePage': ['0'], u'userAccountControl': ['66048'], 
u'sAMAccountType': ['805306368'], u'uSNChanged': ['44379549'], u'givenName': ['pcf_test_user_003']})]

test = {'org1': ['hello', 'world'], 'org2':[]}

for i in test:
    print(test[i])

print(test['org1'])

print('CN=PCF_Sandbox_SpaceDevelopers_SYT,OU=Test,OU=PCF,OU=Groups,OU=Enterprise,DC=int,DC=8451,DC=com' in data[0][1]['memberOf'])