from project import app
import os

# If we are in production, make sure we DO NOT use the debug mode
if os.environ.get('ENV') == 'production':
  debug = False
else:
  debug = True

if __name__ == '__main__':
  app.run(debug=debug)