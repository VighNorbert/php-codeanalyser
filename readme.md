# Codeanalyser for PHP

Author: Norbert Vígh

This project is a partial fulfillemnt of the [Software Architecture](http://fiit.sk/~vranic/as/) 2022/23 course
completion
conditions at the Faculty of Informatics and
Information Technologies of Slovak University of Technology in Bratislava, .

## Description

This is a simple code analyser for PHP.

It can be used to generate UML class diagrams in UXF format directly from the source code.

After the analysis, it is also possible to list all identified Design Patterns. For now, only Singleton and Composite
are supported.

## Installation and running

1. Download the code analyser
2. Run the code analyser by executing: `python3 main.py`
3. Select the PHP project directory
4. Use one of the following commands:
    1. `diagram`: Generate the UML class diagram. After generating, open the generated UXF file
       in [Umletino](https://www.umletino.com/)
    2. `patterns`: Identify the Design Patterns used in the PHP project. The result will be printed in the console.
    3. `exit`: Exit the application.