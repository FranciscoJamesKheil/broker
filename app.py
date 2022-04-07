from broker import create_app
from flask import Flask, request, jsonify

app = create_app()

if __name__ == '__main__':
    print("Starting Python Flask Server For House and Lot Price Prediction...")
    from browserstack.local import Local

    # Creates an instance of Local
    bs_local = Local()

    # You can also set an environment variable - "BROWSERSTACK_ACCESS_KEY".
    bs_local_args = { "key": "2e3js5LccVGRkWYKpkWB" }

    # Starts the Local instance with the required arguments
    bs_local.start(**bs_local_args)

    # Check if BrowserStack local instance is running
    print(bs_local.isRunning())


    app.run(debug=True)

    # Stop the Local instance
    bs_local.stop()