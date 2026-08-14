# Notes API

A secure, single-resource REST API for managing personal notes, built with Django REST Framework. Each user can only create, view, update, and delete their own notes — ownership is enforced at both the query and permission level, not just checked at the surface.

## Architecture

```
Client (Postman / curl / frontend)
        │
        ▼
   JWT Authentication
        │
        ▼
 Django REST Framework
   (NoteViewSet + IsOwner permission)
        │
        ▼
      SQLite
```

## Key Technical Decisions

- **JWT over session auth** — access/refresh token pair instead of a single long-lived token, so a leaked access token is only useful for a short window (30 min) rather than indefinitely.
- **Custom `IsOwner` permission + `get_queryset()` filtering, used together** — `get_queryset()` restricts which notes a user can even see in the list view; `IsOwner` restricts direct detail access. Both are needed: filtering alone doesn't protect direct-by-ID requests, and the permission class alone doesn't protect the list endpoint.
- **404, not 403, for other users' notes** — when a user requests a note they don't own, the API returns 404 rather than 403. This avoids leaking whether a given note ID exists at all, which is the more defensible default for a resource that shouldn't be discoverable by non-owners.
- **Server-side ownership assignment** — `owner` is a read-only field in the serializer and is set explicitly in `perform_create()` from the authenticated request, never accepted from client input. A request can't spoof ownership by passing a different `owner` value.
- **Field-level validation beyond "any string goes"** — a custom `validate_title` rejects empty or whitespace-only titles, enforced server-side regardless of what a client sends.

## Tech Stack

Python | Django | Django REST Framework | Simple JWT | drf-spectacular | SQLite | django-filter | Postman

## API Docs

Live Swagger: [https://notesapi.pythonanywhere.com/api/docs/](https://notesapi.pythonanywhere.com/api/docs/)
Postman collection: Coming Soon

## Running Locally

```bash
git clone https://github.com/megzinx/notesapi.git
cd notesapi
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API available at `http://127.0.0.1:8000/api/`
Swagger docs at `http://127.0.0.1:8000/api/docs/`

### Key Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain JWT access + refresh token pair |
| POST | `/api/token/refresh/` | Refresh an expired access token |
| GET | `/api/notes/` | List the authenticated user's notes (supports `?search=`) |
| POST | `/api/notes/` | Create a new note |
| GET | `/api/notes/{id}/` | Retrieve a single note (owner only) |
| PATCH | `/api/notes/{id}/` | Update a note (owner only) |
| DELETE | `/api/notes/{id}/` | Delete a note (owner only) |

## Testing

5 tests covering JWT authentication enforcement, per-user data isolation, object-level permission checks, server-side ownership assignment, and field validation.

```bash
python manage.py test
```

## Demo Video

Coming Soon