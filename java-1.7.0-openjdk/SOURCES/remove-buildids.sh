#!/bin/bash

JAVA_HOME=$1

# remove build id in ELF file $1
remove_buildid() {
   echo "Removing build id from $1"
   objcopy --rename-section=.note.gnu.build-id=.ignore.note.gnu.build-id "$1"
}

remove_buildids_in() {
    for f in $(find $1 -type f) ; do
        echo "$f"
        if [ -f $f ]; then
            file $f | grep ELF > /dev/null 2>&1
            is_elf=$?
            if [ $is_elf -eq 0 ] ; then
                remove_buildid $f
            fi
        fi
    done
}

remove_buildids_in ${JAVA_HOME}/bin
remove_buildids_in ${JAVA_HOME}/lib
remove_buildids_in ${JAVA_HOME}/demo
remove_buildids_in ${JAVA_HOME}/jre/bin
remove_buildids_in ${JAVA_HOME}/jre/lib
