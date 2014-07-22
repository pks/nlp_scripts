#!/usr/bin/env ruby

# works with gigaword en v5

STDIN.set_encoding 'utf-8'
STDOUT.set_encoding 'utf-8'


in_p = false
in_dateline = false
collect = []

while line = STDIN.gets
  line.strip!
  if line.downcase == "<dateline>"
    in_dateline = true
    next
  elsif line.downcase == "</dateline>"
    in_dateline = false
    next
  elsif in_dateline
    next
  elsif line.downcase == "<p>" and not in_p
    in_p = true
    collect = []
    next
  elsif line.downcase == "</p>" and in_p
    if collect.size > 0
        puts collect.join(" ").strip
    end
    in_p = false
    next
 elsif in_p
   collect.push line
   next
 else
   puts line
 end
end

