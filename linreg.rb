#!/usr/bin/env ruby

require 'nlp_ruby'
require 'trollop'


def read_data fn
  f = ReadFile.new fn
  data = []
  while line = f.gets
    line.strip!
    v = SparseVector.new
    a = []
    a << 1.0
    tokenize(line).each { |i| a << i.to_f }
    v.from_a(a)
    data << v
  end
  return data  
end

def main
  cfg = Trollop::options do
    opt :input,         "input data",         :type => :string, :required => true
    opt :output,        "output data",        :type => :string, :required => true
    opt :learning_rate, "learning rate",      :type => :float,  :default => 0.07
    opt :stop,          "stopping criterion", :type => :int,    :default => 100
  end
  data = read_data cfg[:input]
  zeros = [0.0]*data[0].size
  t = ReadFile.new(cfg[:output]).readlines.map{ |i| i.to_f }
  model = SparseVector.new zeros
  stop = 0
  prev_model = nil
  i = 0
  while true
    i += 1
    u = SparseVector.new zeros
    data.each_with_index { |d,j|
      u += d * ((model.dot(d) - t[j])*(1.0/t.size))
    }
    u *= cfg[:learning_rate]
    model -= u
    if model.approx_eql? prev_model 
      stop += 1
    else
      stop = 0
    end
    break if stop==cfg[:stop]
    prev_model = model
  end
  tss = t.map{ |y| (y-t.mean)**2 }.sum
  j = -1
  rss = t.map{ |y| j+=1; (y-model.dot(data[j]))**2 }.sum
  STDERR.write "ran for #{i} iterations\n R^2=#{1-(rss/tss)}\n"
  puts model.to_s
end


main

