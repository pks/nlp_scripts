#!/usr/bin/env ruby


while line = STDIN.gets
  encoding_options = {
    :invalid           => :replace,
    :undef             => :replace,
    :replace           => '?',
    :universal_newline => true
  }
  puts line.encode 'ASCII', encoding_options
end

