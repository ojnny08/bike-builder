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

## Styling css
- Dont make every word capatialized

## General
- dont add comments


## Code style
- Avoid writting unessesaary code that tries to cover every type of issue
- Prefer functional programming patterns over object-oriented design. Use early returns to minimize nesting.
- for designs do not wrap everything in a rectangle with curved edges

## Must do
- Always ask me question instead of assuming
- Always make a plan to review before implmeneting code

## 3d-builder
Interactive 3D bike builder using raw three.js (not react-three-fiber).

### Goal
As the user selects components, matching 3D models populate a single assembled
bike in fixed assembly order. The camera glides to focus each part; revisiting a
part returns to that part's saved view. User can orbit the whole bike.

### Folder — src/bike3d/ (raw three.js, one React file)
- BikeScene.js — scene, camera, WebGLRenderer({ antialias: true }),
  setPixelRatio(min(devicePixelRatio, 2)), OrbitControls, render loop,
  sync(), focusPart(), dispose()
- cameraViews.js — per-category { position, target } presets (tuned live)
- parts/index.js — registry: component_type -> { build(), transform }
- parts/*.js — one geometry builder per category (~14); materials.js, helpers.js
- BikeViewer.jsx — the only React file: <canvas> + useEffect lifecycle

### Models
- One model per component CATEGORY (generic frame, wheel, etc.), not per product.
- Built procedurally from three.js primitives; wheel/tire reused front + rear.
- Each part has a fixed transform (position/rotation) that drives assembly.

### Scene behavior
- sync(components): diff component_types against a Map<type, Object3D>; add newly
  selected parts, remove deselected ones with geometry/material.dispose().
- focusPart(type): set camera goal from cameraViews[type]; render loop lerps
  camera + controls.target for the glide. null -> overview.
- Overview camera on open (empty) and on finish; drag-to-orbit enabled.

### Flow (selection stays on its own page)
1. Open builder -> empty space, camera at overview.
2. Click a category card -> navigate to /builds/new/select/:category
   (existing ComponentSelectPage — unchanged).
3. Pick a product -> return to builder -> its category model renders at the
   assembly position -> camera glides to that part's assigned view.
4. Repeat; parts keep populating the one bike in fixed assembly order.
5. Revisit a category -> camera transitions back to that part's saved view.
6. Finish -> camera returns to overview.

### Integration
- Replace the .bs-canvas placeholder in BikeStageBuilder.jsx with <BikeViewer
  components={build.components} focused={focusedCategory} />; keep the div/layout.
- focusedCategory (already in BikeStageBuilder) drives focusPart via a prop.
- No changes to routing or ComponentSelectPage.

### Setup
- Branch: feature/3d-builder off main.
- npm install three inside bikebuilder-frontend/ (not the repo root).

### Build order
1. Empty scene + OrbitControls + overview camera.
2. One placeholder box + sync().
3. focusPart() camera glide.
4. Real per-category geometry builders, one at a time.