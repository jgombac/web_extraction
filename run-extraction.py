import sys
import xpath_extract

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "A":
            xpath_extract.run_all()
    else:
        xpath_extract.run_all()
