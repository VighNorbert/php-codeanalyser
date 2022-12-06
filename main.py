from reader import Reader
from php.phpClass import PHPClass
from php.phpDesignPattern import design_patterns, PHPDesignPattern
from umletino.diagram import UmletinoDiagram
import sys
import os
import pathlib


def main():
    start_dir = pathlib.Path().resolve()
    filedir = sys.argv[1] if len(sys.argv) > 1 else input("Enter the project folder:\n")
    classes = []
    for f in Reader(filedir).get_files():
        c = PHPClass(f)
        if c.name is not None:
            for sc in c.otherClassesInFile:
                classes.append(sc)
            c.otherClassesInFile = []
            classes.append(c)

    for c in classes:
        c.identify_classes()

    for c in classes:
        c.advanced_parsing()
        has_private_constructor = False
        has_instance_function = False
        for m in c.methods:
            d = m.definition
            if ('private' in d or 'protected' in d) and '__construct' in d:
                has_private_constructor = True
            if 'static' in d and 'private' not in d and 'function' in d and (':' not in d or (
                    ':' in d and c.identify_class(d.split(':')[1].strip(' ')) == c.identify_class(c.name))):
                has_instance_function = True
            if has_instance_function and has_private_constructor:
                dp = PHPDesignPattern('Singleton')
                dp.add(c, 'Singleton')
                break

    inp = input("Write\n - 'diagram' to write the diagram to a file\n - or 'patterns' to show the identified design patterns\n - or 'exit' to exit:\n")
    while inp != 'exit':
        if inp == 'diagram':
            fn = input("Enter the file name to be written (*.uxf): ")
            while not fn.endswith('.uxf') or ' ' in fn or '/' in fn or '\\' in fn:
                print("The file name must end with .uxf and may not contain spaces and slashes")
                fn = input("Enter the file name to be written (*.uxf): ")
            diagram = UmletinoDiagram(classes)
            os.chdir(start_dir)
            f = open(fn, "w")
            f.write(diagram.__str__())
            f.close()
            print(f"Output written to {fn}")
            print("You can open the file with Umletino")
            print("-----------------------------------")
        elif inp == 'patterns':
            if len(design_patterns) > 0:
                print("Design patterns detected:")
                print(*design_patterns, sep='\n')
            else:
                print("No design patterns detected.")
            print("-----------------------------------")
        else:
            print("Unknown command. Please try again.")
        inp = input("Write\n - 'diagram' to write the diagram to a file\n - or 'patterns' to show the identified design patterns\n - or 'exit' to exit:\n")



if __name__ == '__main__':
    main()
