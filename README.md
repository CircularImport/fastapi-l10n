# FastAPI Localization

Util for localization FastAPI application (powered by Fluent)

### Example:

```python
from fastapi import FastAPI
from fastapi_l10n import L10nDepends, setup_localization

setup_localization(
    allowed_locales=["en", "fr", "de"],
    default_locale="en",
    resource_ids={
        "en": ["main.ftl"],
        "fr": ["main.ftl"],
        "de": ["main.ftl"],
    }
)
app = FastAPI()

@app.get("/")
async def root(_: L10nDepends):
    return _("hello-message", args={"username": "John"})
```
