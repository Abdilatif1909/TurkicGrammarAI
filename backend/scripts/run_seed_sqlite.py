import os
import sys
from pathlib import Path
import django
from django.core.management import call_command

# Ensure backend is on sys.path so `import config` works
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
# Force USE_SQLITE to True for this process
os.environ['USE_SQLITE'] = '1'
django.setup()

def main():
    # Run migrations then seed cognates in same process (in-memory DB)
    call_command('migrate', verbosity=1)
    call_command('seed_cognates', '--path', os.path.join('backend', 'data', 'cognates'), '--file', 'cognates.json')

if __name__ == '__main__':
    main()
