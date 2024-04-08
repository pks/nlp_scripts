#!/usr/bin/env python3

import sys
from xml.sax.saxutils import escape


if __name__ == "__main__":
    prefix = """<tmx version="1.4">
  <header
    creationtool="bitext2tmx.py" creationtoolversion="1.0"
    datatype="PlainText" segtype="sentence"
    adminlang="en-us" srclang="en"
    o-tmf="ABCTransMem"/>
  <body>"""

    src_file = open(sys.argv[1], "r")
    tgt_file = open(sys.argv[2], "r")

    src_lang = sys.argv[1].split(".")[-1]
    tgt_lang = sys.argv[2].split(".")[-1]

    tus = []
    for src_line, tgt_line in zip(src_file.readlines(), tgt_file.readlines()):
        src_line = src_line.rstrip("\n")
        tgt_line = tgt_line.rstrip("\n")
        tus.append(f"""
    <tu>
      <tuv xml:lang="{src_lang}">
        <seg>{escape(src_line)}</seg>
      </tuv>
      <tuv xml:lang="{tgt_lang}">
        <seg>{escape(tgt_line)}</seg>
      </tuv>
    </tu>""")

    suffix = """  </body>
</tmx>"""

    complete = "\n".join([prefix] + tus + [suffix])

    print(complete)
