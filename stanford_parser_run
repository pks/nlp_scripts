#!/bin/bash

if [ $# != 1 ]; then
	echo "$0 text-file" 
	exit 1
fi

export CLASSPATH=:/toolbox/stanfordparser_3_2_0/*

IN=$1

cat $IN | java -server -mx25000m  edu.stanford.nlp.parser.lexparser.LexicalizedParser -nthreads 8 -sentences newline -encoding utf-8 -tokenized -outputFormat "typedDependencies" -outputFormatOptions "basicDependencies" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz - | tr '\n' '\t' | sed 's/\t\t/\n/g' | sed 's/\t/ /g' | sed 's/ *$//' | sed 's/, /,/g' > $IN.stp

