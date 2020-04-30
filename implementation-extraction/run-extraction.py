import sys
import xpath_extract
import regex_extract
import wrapper

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "A":
            xpath_extract.run_all()
        elif arg == "B":
            regex_extract.run_all()
        else:
            wrapper.run()

    else:
        xpath_extract.run_all()
        regex_extract.run_all()
        wrapper.run()
