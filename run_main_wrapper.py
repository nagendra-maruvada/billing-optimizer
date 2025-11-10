import os
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from app import main

if __name__ == '__main__':
    main.main()

