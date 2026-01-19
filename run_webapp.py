#!/usr/bin/env python3
"""
Run the Kidney Stone Predictor Flask Web Application

This script starts the Flask web application for kidney stone prediction.
"""

import os
import sys
import argparse
from app import app

def main():
    parser = argparse.ArgumentParser(description='Run Kidney Stone Predictor Web App')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    parser.add_argument('--no-reload', action='store_true',
                       help='Disable auto-reload in debug mode')

    args = parser.parse_args()

    # Set environment variables
    if args.debug:
        os.environ['FLASK_DEBUG'] = 'true'
        os.environ['FLASK_ENV'] = 'development'

    # Configure app
    app.config['DEBUG'] = args.debug

    print("=" * 60)
    print("KIDNEY STONE PREDICTOR - FLASK WEB APPLICATION")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Debug Mode: {args.debug}")
    print(f"URL: http://localhost:{args.port}")
    print("=" * 60)

    # Check if config exists
    if not os.path.exists('config.json'):
        print("WARNING: config.json not found!")
        print("Please run 'python setup.py' first to configure your Watson credentials.")
        print("The app will still run but predictions will fail without proper configuration.\n")

    # Check if model is deployed
    if not os.path.exists('deployment_info.json'):
        print("WARNING: deployment_info.json not found!")
        print("Please run the AutoML experiment first: 'python run_experiment.py --data your_data.csv'")
        print("The app will still run but predictions will fail without a deployed model.\n")

    try:
        # Run the app
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            use_reloader=not args.no_reload if args.debug else False
        )
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()