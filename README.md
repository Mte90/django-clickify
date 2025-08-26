# Django Clickify

A simple Django app to track file downloads with rate limiting, IP filtering, and geolocation.

## Features

*   **Download Tracking**: Logs every file download, including IP address, user agent, and timestamp.
*   **Geolocation**: Automatically enriches download logs with the country and city of the request's IP address via a web API. No local database required.
*   **Rate Limiting**: Prevents abuse by limiting the number of downloads per IP address in a given timeframe.
*   **IP Filtering**: Easily configure allowlists and blocklists for IP addresses.
*   **Secure**: Protects against path traversal attacks.

## Installation

1.  Install the package from PyPI:

    ```bash
    pip install django-clickify
    ```

2.  Add `'clickify'` to your `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
        # ...
        'clickify',
    ]
    ```

3.  Run migrations to create the `DownloadClick` model in your database:

    ```bash
    python manage.py migrate clickify
    ```

## Configuration

### 1. Middleware (for IP Filtering)

To enable IP filtering, add the `IPFilterMiddleware` to your `MIDDLEWARE` setting in `settings.py`.

```python
MIDDLEWARE = [
    # ...
    'clickify.middleware.IPFilterMiddleware',
    # ...
]
```

### 2. Settings (Optional)

You can customize the behavior of `django-clickify` by adding the following settings to your `settings.py`:

*   `CLICKIFY_GEOLOCATION`: A boolean to enable or disable geolocation via the `ip-api.com` service. Defaults to `True`.

    ```python
    # settings.py
    CLICKIFY_GEOLOCATION = False # Disable geolocation lookups
    ```

*   `CLICKIFY_RATE_LIMIT`: The rate limit for downloads. Defaults to `'5/m'` (5 downloads per minute).

    ```python
    # settings.py
    CLICKIFY_RATE_LIMIT = '10/h' # 10 downloads per hour
    ```

*   `CLICKIFY_IP_ALLOWLIST`: A list of IP addresses that are always allowed, bypassing the blocklist.

    ```python
    # settings.py
    CLICKIFY_IP_ALLOWLIST = ['127.0.0.1', '192.168.1.1']
    ```

*   `CLICKIFY_IP_BLOCKLIST`: A list of IP addresses that are always blocked.

    ```python
    # settings.py
    CLICKIFY_IP_BLOCKLIST = ['10.0.0.1']
    ```

## Usage

To track downloads for a file, use the `track_download` view in your project's `urls.py`.

You need to configure your project to serve media files. Make sure you have `MEDIA_URL` and `MEDIA_ROOT` set in your `settings.py`.

```python
# your_project/urls.py

from django.urls import path
from clickify.views import track_download

urlpatterns = [
    # ...
    path('downloads/<path:file_path>', track_download, name='track_download'),
]
```

Now, any request to `/downloads/path/to/your/file.txt` will be logged, and the file will be served to the user. The `file_path` should be relative to your `MEDIA_ROOT`.

## Testing

To run the tests for this app:

```bash
poetry install
poetry run pytest
```