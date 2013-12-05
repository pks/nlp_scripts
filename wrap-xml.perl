#!/usr/bin/perl -w
# original: https://smt.googlecode.com/svn/trunk/moses64/tools/scripts/wrap-xml.perl

use strict;

my $src = $ARGV[0];
my $language = $ARGV[1];
die("syntax: wrap-xml.perl xml-frame language [system-name]")
    unless $src && $language && -e $src;
my $system = "my-system";
$system = $ARGV[2] if defined($ARGV[2]);

open(SRC,$src);
my @OUT = <STDIN>;
chomp(@OUT);
#my @OUT = `cat $decoder_output`;
while(<SRC>) {
    chomp;
    if (/^<srcset/) {
	s/<srcset/<tstset trglang="$language" sysid="$system"/;
    }
    elsif (/^<\/srcset/) {
	s/<\/srcset/<\/tstset/;
    }
    elsif (/^<DOC/) {
	s/<DOC/<DOC sysid="$system"/;
    }
    elsif (/<seg/) {
	my $line = shift(@OUT);
        $line = "" if $line =~ /NO BEST TRANSLATION/;
        if (/<\/seg>/) {
	  s/(<seg[^>]+> *).+(<\/seg>)/$1$line$2/;
        }
        else {
	  s/(<seg[^>]+> *)[^<]+/$1$line/;
        }
    }
    print $_."\n";
}

