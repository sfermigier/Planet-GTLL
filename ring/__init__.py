"""Entry point for the ring project.
"""

__author__ = 'fermigier'
__doc__ = """Usage: ring <command> <options>

Where command can be:

- crawl
- serve
- scaffold [TODO]
"""

import sys
import server
import crawler

def usage():
    print __doc__

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == 'serve':
        server.main()
    elif sys.argv[1] == 'crawl':
        crawler.main()
    else:
        usage()
        sys.exit(1)

if __name__ == "__main__":
    main()