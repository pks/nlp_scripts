import argparse
import datetime
import sys

from translate.storage.tmx import tmxfile


def extract_from_tmx(tmx_file_path,
                     src_out_path,
                     tgt_out_path,
                     begin_date,
                     date,
                     src_out_after,
                     tgt_out_after):
    with open(tmx_file_path, 'rb') as in_fp:
        tmx_file = tmxfile(in_fp)
    
    if src_out_after is not None and tgt_out_after is not None:
        src_out_after_fp = open(src_out_after, "w")
        tgt_out_after_fp = open(tgt_out_after, "w")
    
        
    with open(src_out_path, "w") as src_out_fp, open(tgt_out_path, "w") as tgt_out_fp:
        for index, node in enumerate(tmx_file.unit_iter()):
            src_out_fp_ = src_out_fp
            tgt_out_fp_ = tgt_out_fp
            
            if begin_date is not None:
                date_string = node.get_target_dom().get('lastusagedate')[:8]
                date_obj = datetime.datetime.strptime(date_string, '%Y%m%d').date()
                if date_obj < begin_date:
                    continue
            
            if date is not None:
                date_string = node.get_target_dom().get('changedate')[:8]
                date_obj = datetime.datetime.strptime(date_string, '%Y%m%d').date()
                if date_obj > date:
                    src_out_fp_ = src_out_after_fp
                    tgt_out_fp_ = tgt_out_after_fp
        
            src_string = f"{node.source}"
            tgt_string = f"{node.target}"
            src_string = src_string.replace('\n', ' ').replace('\r', '')
            tgt_string = tgt_string.replace('\n', ' ').replace('\r', '')
        
            src_out_fp_.write(f"{src_string}\n")
            tgt_out_fp_.write(f"{tgt_string}\n")
            if (index + 1) % 1000 == 0:
                sys.stdout.write(f"Processed {index + 1} lines\r")
                sys.stdout.flush()

    if src_out_after is not None and tgt_out_after is not None:
        src_out_after_fp.close()
        tgt_out_after_fp.close()


def main():

    usage = "Usage: python tmx_to_plain.py [options]"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-i", "--input", help="input tmx file")
    parser.add_argument("-d", "--date", help="date for splitting the output")
    parser.add_argument("-b", "--begin_date", help="earliest date (lastusage) to retain data")

    args = parser.parse_args()

    if args.input is None:
        parser.print_help()
        sys.exit(1)
    
    args.input
    
    src_out = args.input + ".src"
    tgt_out = args.input + ".tgt"
    
    
    if args.date is not None:
        date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
        src_out_after = src_out + ".after." + args.date
        tgt_out_after = tgt_out + ".after." + args.date
    else:
        date = None
        src_out_after = None
        tgt_out_after = None
        
    if args.begin_date is not None:
        begin_date = datetime.datetime.strptime(args.begin_date, '%Y-%m-%d').date()
    else:
        begin_date = None
        
    extract_from_tmx(args.input, src_out, tgt_out, begin_date, date, src_out_after, tgt_out_after)    
    

if __name__ == '__main__':
    main()
