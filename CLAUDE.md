# BikeBuilder
- A dynamic bike builder where selecting a component updates the UI in real time. 
- Each component displays an image, name, and price.
## Stack
- Frontend: React (plain CSS), deployed on Vercel
- Backend: Django REST Framework, deployed on Railway
- Database: PostgreSQL
- Auth: Firebase OAuth (JWT verified in Django middleware)

## Project Structure
- /frontend — React app
- /backend — Django project

## Conventions
- API routes prefixed with /api/
- Compatibility filtering handled server-side

### Code style
- Avoid writting unessesaary code that tries to cover every type of issue
- Prefer functional programming patterns over object-oriented design. Use early returns to minimize nesting.