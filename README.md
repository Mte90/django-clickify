# Django Clickify

A simple Django app to track file downloads with rate limiting, IP filtering, and geolocation.

## Features

*   **Download Tracking**: Logs every file download, including IP address, user agent, and timestamp.
*   **Geolocation**: Automatically enriches download logs with the country and city of the request's IP address via a web API. No local database required.
*   **Rate Limiting**: Prevents abuse by limiting the number of downloads per IP address in a given timeframe.
*   **IP Filtering**: Easily configure allowlists and blocklists for IP addresses.
*   **Secure**: Protects against path traversal attacks.
*   **Django Admin Integration**: Create and manage your download targets directly in the Django admin.
*   **Template Tag**: A simple template tag provides an easy and robust way to generate tracking URLs.

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

3.  Run migrations to create the necessary database models:

    ```bash
    python manage.py migrate
    ```

## Configuration

### 1. Middleware (for IP Filtering)

To enable the IP allowlist and blocklist feature, add the `IPFilterMiddleware` to your `settings.py`.

```python
MIDDLEWARE = [
    # ...
    'clickify.middleware.IPFilterMiddleware',
    # ...
]
```

### 2. Settings (Optional)

You can customize the behavior of `django-clickify` by adding the following settings to your `settings.py`:

*   `CLICKIFY_GEOLOCATION`: A boolean to enable or disable geolocation. Defaults to `True`.
*   `CLICKIFY_RATE_LIMIT`: The rate limit for downloads. Defaults to `'5/m'`.
*   `CLICKIFY_IP_ALLOWLIST`: A list of IP addresses that are always allowed. Defaults to `[]`.
*   `CLICKIFY_IP_BLOCKLIST`: A list of IP addresses that are always blocked. Defaults to `[]`.

## Usage Example

Here is a complete example of how to track a download for a file hosted on an external service like Amazon S3.

### Step 1: Create a Download Target

In your Django Admin, go to the "Clickify" section and create a new "Download Target".

*   **Name:** `Monthly Report PDF`
*   **Slug:** `monthly-report-pdf` (this will be auto-populated from the name)
*   **Target Url:** `https://your-s3-bucket.s3.amazonaws.com/reports/monthly-summary.pdf`

### Step 2: Include Clickify URLs

In your project's `urls.py`, include the `clickify` URL patterns.

```python
# your_project/urls.py
from django.urls import path, include

urlpatterns = [
    # ... your other urls
    path('downloads/', include('clickify.urls', namespace='clickify')),
]
```

### Step 3: Create the Download Link

In your Django template, use the `track_url` template tag to generate the tracking link. Use the slug of the `DownloadTarget` you created in Step 1.

```html
<!-- your_app/templates/my_template.html -->
{% load clickify_tags %}

<a href="{% track_url 'monthly-report-pdf' %}">
  Download Monthly Summary
</a>
```

### How It Works

1.  The `track_url` tag generates a URL like `/downloads/monthly-report-pdf/`.
2.  When a user clicks this link, the request is sent to the `track_download` view.
3.  The view records the download event in the database, associating it with the "Monthly Report PDF" target.
4.  The view then issues a redirect to the `target_url` you defined, and the user's browser downloads the file from your S3 bucket.

This approach is powerful because if you ever need to change the file's location, you only need to update the `Target Url` in the Django Admin. All your download links will continue to work and track correctly.