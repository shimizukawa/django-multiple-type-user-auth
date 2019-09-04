# django-multiple-type-user-auth
PoC django multiple type user authentication 

## Concept

* Two user models as: "Admin User" and "Front User".
* "Admin User" can only login "Django Admin".
* "Front User" can only login "Front site".
* "Front User" have two kind of concrete user types as "Customer" and "Supporter".
* "Customer" can access customer's views.
* "Supporter" can access supporter's views.

## Setup

```
$ pip install -r requirements.txt
$ python apps/manage.py migrate
$ python apps/manage.py createsuperuser  # for admin user
```

## Invocation

```
$ honcho start
```

That invoke 2 django application process for:

* Front: http://localhost:8000/
* Admin: http://localhost:8001/admin/

At first, you must create "Customer" and "Supporter" users in Django Admin with using created super user account.

## Behaviors

* "Admin" user can only login from http://localhost:8001/admin/
* "Customer" and "Supporter" can only login from http://localhost:8000/
* "Customer" can only view http://localhost:8000/customer/
* "Supporter" can only view http://localhost:8000/supporter/
* All users can logout from http://localhost:8000/accounts/logout.html

## Schemas

"Admin User" table (django default):
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

"Front User" table (base model for customer and supporter):
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

"Customer User" table (multi-table inheritance):
```
CREATE TABLE "accounts_customeruser"
(
    "user_id" integer     NOT NULL PRIMARY KEY REFERENCES "accounts_frontuser" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tel"     varchar(20) NOT NULL
);
```

"Customer User" table (multi-table inheritance):
```
CREATE TABLE "accounts_supporteruser"
(
    "user_id"      integer     NOT NULL PRIMARY KEY REFERENCES "accounts_frontuser" ("id") DEFERRABLE INITIALLY DEFERRED,
    "organization" varchar(64) NOT NULL
);
```
