#!/bin/bash

echo "--------------------------------------------------"
echo "PID for child.sh: $$"
echo "In child.sh, variable var=$var from parent.sh"

var="child"
export var

echo "In child.sh, set var=$var"
echo "In child.sh, variable var=$var"
echo "--------------------------------------------------"
