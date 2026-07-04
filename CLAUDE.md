# BikeBuilder
- A dynamic bike builder where selecting a component updates the UI in real time. 
- Each component displays an image, name, and price.
## Stack
- Frontend: React (plain CSS), deployed on Vercel
- Backend: Django REST Framework, deployed on Railway
- Database: PostgreSQL
- Auth: Firebase OAuth (JWT verified in Django middleware)

## Project Structure
- /bikebuilder-frontend — React app
- /bikebuilder — Django project (apps live in /bikebuilder/apps)

## Conventions
- API routes prefixed with /api/
- Compatibility filtering handled server-side

### Code style
- Avoid writting unessesaary code that tries to cover every type of issue
- Prefer functional programming patterns over object-oriented design. Use early returns to minimize nesting.
- for designs do not wrap everything in a rectangle with curved edges