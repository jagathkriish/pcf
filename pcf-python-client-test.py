import os
from cloudfoundry_client.client import CloudFoundryClient
target_endpoint = 'https://somewhere.org'
proxy = dict(http=os.environ.get('HTTP_PROXY', ''), https=os.environ.get('HTTPS_PROXY', ''))
client = CloudFoundryClient(target_endpoint, proxy=proxy, skip_verification=True)
client.init_with_user_credentials('login', 'password')

for organization in client.organizations:
    print organization['metadata']['guid']