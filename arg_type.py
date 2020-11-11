import magic
import os
import plan_parser
import task_parser
import sys
from open_file import open_file


def arg_type(argv):
    print('determining the argument type')
    type = magic.from_file(str(argv),mime=True)
    #If gzip, decompress and drop me in the folder with the html files
    if type == 'application/gzip':
        try:
            print('detecting gzip file')
            open_file(argv)
            files = os.scandir(os.getcwd())
            for html_file in files:
                if html_file[:-5] == '.html':
                    print('parsing ' + html_file)
                    #call task parcer
                    task = task_parser.main(html_file)
                    #call plan_parser here
                    plan = plan_parser.main(html_file)
                    #call run_parser here
                    #call finalize_parser here
                else:
                    print(html_file + ' is not html, skipping')
        except:
            print('exception gzip')
    #If HTML, parse it
    elif type == 'text/html':
        try:
            print('detecting html file')
            #call parser here
        except:
            print('exception html')
    elif argv is str:
        if 'http' in argv:
            try:
                print('detecting URL')
            except:
                print('exception URL')