# GLDAS icehunk updater

## Instructions

### Export uv dependencies for lambda function

>[!WARN]
>This is currently just a folder skeleton, modeled after [the MUR icechunk updater](https://github.com/developmentseed/mursst-icechunk-updater).

To keep requirements consistent we can export the uv lockfile to a requirements.txt. 

```
uv export --format=requirements.txt > cdk/lambda/requirements.txt
```

>[!CHECK]
> - [ ] Implement this as a post commit hook. I want to make sure that this is 100% in sync whenever pushing to github


## Examples

### EDL refreshable credentials in obstore, icehunk, ...

```
uv run --group=examples examples/earthdata_refreshable_credentials.py
```


