# django-view-tracking

Simple logging of user access to URLs in Django.

## Usage

**Install:**

```shell
pip install django-view-tracking
```

**Enable:**

```python
# settings.py

INSTALLED_APPS = [
    ...
    'django_view_tracking',
    ...
]

MIDDLEWARE = [
    ...
    'django_view_tracking.middleware.ViewTrackingMiddleware',
    ...
]
```

**Configure:**

```python
# global kill switch
DJANGO_VIEW_TRACKING_ENABLED = True

# switch logging for anonymous users on or off
DJANGO_VIEW_TRACKING_ANONYMOUS_USER = True

# ignore logging for specific paths
DJANGO_VIEW_TRACKING_BLACKLIST = [
    reverse('admin:index'),
]
```

**Migrate:**

```shell
python manage.py migrate
```

**Enjoy:**

View logs in the Django Admin under `Django View Tracking`.

### License

[MIT License](LICENSE)
