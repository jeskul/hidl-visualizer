# hidl-visualizer
Python script that takes the output from 'ps -ef' and 'lshal' from a running Android target and produces a Graphviz dot source file with the dependencies between services and interfaces.
If Graphviz is found the script will generate an image file if the -o option is specified.

Note: This tool is mainly for the use of developing an Android device i.e. working with AOSP
Note: This tool is deprecated since hwbinder and HIDL is deprecated in AOSP

Example usage:

    adb shell lshal > lshal_example.txt
    adb shell ps -ef >> lshal_example.txt

    ./hidlizer.py -i lshal_example.txt -o lshal_example

![Image](lshal_example.png "example output")
