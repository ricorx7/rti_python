DEVELOP
Run this command to develop.  It will auto refresh the electron app with the latest code.
```
npm run dev
```

BUILD

Build PlanR to run in Electron
In the Frontend build the electron desktop app:
```
npm run build
```
This will create an executable depending on the platform it was built.

Build PlanR for web browswer
In the Frontend PlanR project run:
```
npm run build:web
```

Then in the Backend run node to view the app in the web browser.
```
node app.js
```
