from utils import str2bool, get_all_file_paths
from models.RakeKor import RakeKor
from tqdm import tqdm
import pandas as pd
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_texts_dir", default="samples/")
    parser.add_argument("--output_dir", default="./output/")
    parser.add_argument("--compound", default=False, type=str2bool)
    parser.add_argument("--min_length", default=-1, type=int)
    parser.add_argument("--max_length", default=-1, type=int)
    parser.add_argument("--show_result", default=True, type=str2bool)

    args = parser.parse_args()
    try:
        assert (args.min_length <= args.max_length and args.min_length != -1 and args.max_length != -1) or\
                args.min_length == -1 or args.max_length == -1
    except AssertionError:
        raise AssertionError("the min_length must be smaller or equal than the max_length")

    rake = RakeKor()
    for path in tqdm(get_all_file_paths(args.source_texts_dir)):
        print(path)
        name = path[path.rindex("/")+1:path.rindex(".")]
        text = open(path).read()

        result = rake(text,
                    compound=args.compound,
                    length_filter=(args.min_length, args.max_length)
                    )
    
        data=[]
        for length in result:
            for keyword, score in result[length]:
                data.append([length, keyword, score])

        df = pd.DataFrame(data, columns=["length", "keyword", "score"])
        
        if args.output_dir[-1] != "/":
            args.output_dir+="/"

        df.to_excel(args.output_dir+name+".xlsx", index=False)

        if args.show_result:
            print("="*30)
            print(name)
            print(df)
            
