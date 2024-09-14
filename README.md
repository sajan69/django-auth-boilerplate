### Step-by-Step Guide for Using `django-auth-app` in a Django Project

#### 1. **Install the Package**

First, you need to install this package using `pip`. This will install `django-auth-app` along with its dependencies.

```bash
pip install django-auth-app
```

#### 2. **Configure `settings.py`**

Next, You need to modify your Django project's `settings.py` to include the necessary settings for `django-auth-app`. Here’s how you should configure it:

- **Add the app to `INSTALLED_APPS`:**

  In your `settings.py` file, you need to include this app:

  ```python
  INSTALLED_APPS = [
      ...
      'auth_app',
      'rest_framework',  # Make sure DRF is also installed
      'drf_yasg',  # For Swagger documentation
      
      ...
  ]
  ```

- **Set the custom user model:**

  this package provides a custom user model. you should update the `AUTH_USER_MODEL` setting:

  ```python
  AUTH_USER_MODEL = 'auth_app.CustomUser'
  ```

- **Add SMTP email settings for OTP and email verification:**

  you need to configure your email backend (for sending OTPs or verification emails):

  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.example.com'  # SMTP provider
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = 'this-email@example.com'
  EMAIL_HOST_PASSWORD = 'this-email-password'
  ```


#### 3. **Add URLs**

You need to include this package's URLs in your `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('auth/', include('auth_app.urls')),  # Include auth_app URLs
]
```

you can access authentication views at `/auth/`, such as `/auth/login/`, `/auth/register/`, etc.

#### 4. **Run Migrations**

To apply this package’s models (e.g., `CustomUser`, `OTP`), you should run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. **Use the Package**

At this point, you can use this `django-auth-app` package as part of your project. For example:

- **Register a new customer:**

  you can visit `/auth/register/customer/` to register a customer.

- **Register a new admin:**

  you can visit `/auth/register/admin/` to register an admin user.

- **OTP Verification:**

  When registering or resetting a password, you will receive an OTP via email, which you can verify at `/auth/otp/verify/<user_id>/<action>/`.

#### 6. **Swagger API Documentation (Optional)**

If you want to access the Swagger UI for API documentation (assuming you’ve configured Swagger as part of the package), you can visit `/swagger/`.

To ensure Swagger is correctly set up, the following settings should be added to `settings.py`:

```python
INSTALLED_APPS += ['drf_yasg']
```

And the necessary URL configuration in `urls.py`:

```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Django Auth API",
      default_version='v1',
      description="API documentation for django-auth-app",
      contact=openapi.Contact(email="sajana46@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
```

#### 7. **Customization**

you can now extend this app based on your project’s needs:

- **Custom Fields**: you can add custom fields to `Customer` and `AdminUser` models.
- **Views**: you can modify views to match your business logic or extend them with additional forms or functionality.

#### 8. **Deployment**

When deploying your project, you should ensure proper configuration for email services, database settings, and other environment-specific settings.

---

### Additional Notes

1. **Extensibility**: Users can extend this app by overriding or adding new views, templates, or forms.
2. **Security**: you should make sure sensitive data such as SMTP credentials and the Django `SECRET_KEY` are properly managed using environment variables.
3. **Contributions**: you can contribute to this project by forking it on GitHub and submitting pull requests if you want to improve the package.

This process is fairly straightforward and covers most users' needs for integrating `django-auth-app` into your Django project!