# µHTTP Multipart

Multipart support for µHTTP.

### Usage

Only parse when required:

```python
from uhttp import App
from uhttp_multipart import parse_form

app = App()

@app.post('/')
def submit(request):
    form = parse_form(request.form)
```

Always parse `multipart/form-data` requests (middleware):

```python
from uhttp import App
from uhttp_multipart import app as mutipart_app

app = App()
app.mount(mutipart_app)
```

The function `parse_form` (which is also used in the middleware) returns a `MultiDict`. Form fields are `str`, file fields are `BytesIO`.

### License

Released under the MIT license.
