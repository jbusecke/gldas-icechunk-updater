# Demo how to provide refreshable credentials for EDL for various 'clients'
from __future__ import annotations
import datetime as dt 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from obstore.store import S3Credential

from obstore.store import S3Store
from urllib.parse import urlparse
import icechunk as ic
import xarray as xr
import earthaccess

## define global inputs
# pre treat urls
url = "s3://gesdisc-cumulus-prod-protected/GLDAS/GLDAS_NOAH025_3H.2.1/2022/091/GLDAS_NOAH025_3H.A20220401.0000.021.nc4"
parsed = urlparse(url)
bucket = f"{parsed.scheme}://{parsed.netloc}"

## non-wrapped EDL credentials getter
def get_earthdata_creds() -> Dict[str, str]:
    auth = earthaccess.login()
    creds = auth.get_s3_credentials("GES_DISC")
    return creds

## obstore
def get_obstore_creds() -> S3Credential:
    creds = get_earthdata_creds()
    return {
        "access_key_id": creds['accessKeyId'],
        "secret_access_key": creds['secretAccessKey'],
        "token": creds['sessionToken'],
        "expires_at": dt.datetime.fromisoformat(creds['expiration']),
    }

print('Testing Obstore')
store = S3Store.from_url(url=bucket, credential_provider=get_obstore_creds)
print(store.head(parsed.path))

## Icechunk
def get_icechunk_creds() -> S3StaticCredentials:
    creds = get_earthdata_creds()
    return ic.s3_static_credentials(
        access_key_id=creds['accessKeyId'],
        secret_access_key=creds['secretAccessKey'],
        expires_after=dt.datetime.fromisoformat(creds['expiration']),
        session_token=creds['sessionToken']
    )

print('testing_icechunk')
storage = ic.s3_storage(
    bucket='nasa-veda-scratch',
    prefix='jbusecke/derecho_test_icechunk',
    region='us-west-2',
    from_env=True,
)
# mmmmh this is super convoluted now because the user has to know the container name?
# virtual_chunk_credentials = ic.containers_credentials(ges_disc=get_icechunk_creds())
virtual_chunk_credentials = ic.containers_credentials(some_other_name=get_icechunk_creds())

repo = ic.Repository.open(
    storage=storage,
    virtual_chunk_credentials=virtual_chunk_credentials
)

session = repo.readonly_session('main')

ds_icechunk = xr.open_zarr(session.store, consolidated=False)

print(ds_icechunk)

## TODO
# - How to test the actual refresh? This just checks that the auth works.
# - The icechunk example relies on env authentication in the hub. It would be more reusable 
#    with an icechunk store that is publicly accessible and points to EDL accessible data