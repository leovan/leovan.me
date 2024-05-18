#!/bin/bash

echo "--------------------------------------------------"
echo "Before calling child.sh"
echo "--------------------------------------------------"
echo "PID for parent.sh: $$"

var="parent"
export var

echo "In parent.sh, set var=$var"
echo "In parent.sh, variable var=$var"

echo "--------------------------------------------------"
case $1 in
    exec)
        echo "Call child.sh using exec"
        exec ./child.sh ;;
    source)
        echo "Call child.sh using source"
        source ./child.sh ;;
    *)
        echo "Call child.sh using fork"
        ./child.sh ;;
esac

echo "After calling child.sh"
echo "--------------------------------------------------"
echo "PID for parent.sh: $$"
echo "In parent.sh, variable var=$var"
echo "--------------------------------------------------"
