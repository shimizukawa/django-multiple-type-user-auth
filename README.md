# django-multiple-type-user-auth
PoC django multiple type user authentication 

## What I want to do

* I want to completely separate user model of front-side users and Django Admin users.
* Both authentication for user types must use Django's standard authentication mechanism.
* Front-side users have multiple user type, so I want to manage them separately on the Django Admin.

## Constraints

* Django's authentication mechanism cannot handle multiple user types in a project (only one user table can be used for authentication)

  * "Django doesn't have multiple users" -- [django best approach for creating multiple type users](https://stackoverflow.com/a/25842236)
  * "First of all, you cannot make multiple authentication user base for a project." -- [python - Django 1.8, Multiple Custom User Types - Stack Overflow](https://stackoverflow.com/a/31103029)

## Concept

* Invoke server processes with separated [settings.AUTH_USER_MODEL](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model) to specify the different user model to be used for authentication on the front-side and the Django Admin.
* Front-side user types are treated as separate models by [Multi Table Inheritance](https://docs.djangoproject.com/en/2.2/topics/db/models/#multi-table-inheritance), which inherits the authentication model.

## Spec

* Two user models for authentication is: `User` and `FrontUser`.
* `User` can only login "Django Admin".
* `FrontUser` can only login "Front site".
* `FrontUser` have two kind of concrete user types as `CustomerUser` and `SupporterUser`.
* `CustomerUser` can access customer's views.
* `SupporterUser` can access supporter's views.

## Setup

```
$ pip install -r requirements.txt
$ python apps/manage.py migrate
$ USER_MODEL=admin python apps/manage.py createsuperuser  # for admin user
```

## Invocation

```
$ honcho start
```

This command invokes 2 django application and 1 dispatcher process as:

* Front: http://localhost:8000/
* Admin: http://localhost:8001/admin/
* Dispatcher: http://localhost:8080/

At first, you must create "Customer" and "Supporter" users in Django Admin
http://localhost:8080/admin/ with using created super user account.

## Behaviors

* "Admin" user can only login from http://localhost:8001/admin/
* "Customer" and "Supporter" can only login from http://localhost:8000/
* "Customer" can only view http://localhost:8000/customer/
* "Supporter" can only view http://localhost:8000/supporter/
* All users can logout from http://localhost:8000/accounts/logout.html

## Schemas

`User` model table (django default):
```
CREATE TABLE "auth_user"
(
    "id"           integer      NOT NULL PRIMARY KEY AUTOINCREMENT,
    "password"     varchar(128) NOT NULL,
    "last_login"   datetime     NULL,
    "is_superuser" bool         NOT NULL,
    "username"     varchar(150) NOT NULL UNIQUE,
    "first_name"   varchar(30)  NOT NULL,
    "email"        varchar(254) NOT NULL,
    "is_staff"     bool         NOT NULL,
    "is_active"    bool         NOT NULL,
    "date_joined"  datetime     NOT NULL,
    "last_name"    varchar(150) NOT NULL
);
```

`FrontUser` model table (Base user model for front side):
```
CREATE TABLE "accounts_frontuser"
(
    "id"         integer      NOT NULL PRIMARY KEY AUTOINCREMENT,
    "password"   varchar(128) NOT NULL,
    "last_login" datetime     NULL,
    "email"      varchar(254) NOT NULL UNIQUE,
    "is_active"  bool         NOT NULL
);
```

`CustomerUser` model table (multi-table inheritance):
```
CREATE TABLE "accounts_customeruser"
(
    "user_id" integer     NOT NULL PRIMARY KEY REFERENCES "accounts_frontuser" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tel"     varchar(20) NOT NULL
);
```

`SupporterUser` model table (multi-table inheritance):
```
CREATE TABLE "accounts_supporteruser"
(
    "user_id"      integer     NOT NULL PRIMARY KEY REFERENCES "accounts_frontuser" ("id") DEFERRABLE INITIALLY DEFERRED,
    "organization" varchar(64) NOT NULL
);
```
