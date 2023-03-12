# How to run React client

`npm install`
`set HTTPS=false&&npm start`

Then navigate to http://localhost:3000

# How to use QR code scanner (for now)
## Desktop
As long as you are navigating to QR code scanner from `localhost` then it should use your webcam as expected

## Mobile
To use it on mobile, React and Flask must be running securely on HTTPS.

To run React on HTTPS run `set HTTPS=true&&npm start` from the frontend directory and navigate to https://localip:3000 in mobile browser.

To run Flask on HTTPS add following parameters to `app.run()` => `
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("certificate/cert.pem", "certificate/key.pem"))`

You must also add your local IP to the CORS origins in `app.py`.

Then you must change the routes to be in the form `https://localip:5000/route` anywhere there is a request in the frontend.