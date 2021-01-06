# hidl-visualizer
Python script that takes the output from 'ps -ef' and 'lshal' from a running Android target and produces a Graphviz dot source file with the dependencies between services and interfaces.

Example usage:
adb shell lshal > lshal_example.txt
adb shell ps -ef >> lshal_example.txt

./hidlizer.py -i lshal_example.txt -o lshal_example

![Image](lshal_example.png "example output")
