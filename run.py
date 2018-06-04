from proxypool.scheduler import Scheduler
from proxypool.api import app
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    try:
        s = Scheduler()
        s.run()
        app.run()
    except:
        main()


if __name__ == '__main__':
    main()