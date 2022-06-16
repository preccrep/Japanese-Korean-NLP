from eunjeon import Mecab
import numpy as np
import re

class RakeKor:
    def __init__(self,
                    delimeters_path={"single":"single_delimeters.txt",
                                    "multi":"multi_delimeters.txt",},
                    stopwords_path="stopwords.txt",
                    content_pos_path="content_pos.txt",
					patterns_path = "patterns.txt"
                ):
        
        # Exact Match
        self.stopwords = set([d[:-1] for d in open(stopwords_path)])
        self.stopword_pattern = "(^{}$)".format("$|^".join(self.stopwords))
        
        self.delimeters = {"single" : set([d[:-1] for d in open(delimeters_path["single"])]), "multi" : set([d[:-1] for d in open(delimeters_path["multi"])])}
        self.delimeter_pattern = ".*?(?:[{}]|{})".format("".join([d for d in self.delimeters["single"] if len(d)<=2]), "|".join(self.delimeters["multi"]))
        
        self.content_pos = set([d[:-1] for d in open(content_pos_path)])
        self.to_remove = set([d[:-1] for d in open(patterns_path)])
        self.tokenizer = Mecab()
		
    def __call__(self, text, compound, length_filter):
        cleaned = self.preprocess(text)
        splt = self.split(cleaned)
        return self.rake(splt, compound=compound, length_filter=length_filter)
        
        
    def get_tokenizer(self, tokenizer):
        if tokenizer == "mecab":
            return Mecab()
    
    def preprocess(self, string:str):
        hangul = ("AC00", "D7AF")
        hanja = ("4E00", "9FFF") # CJK_UNIFIED
        symbols = [("2600", "26FF"), ("25A0", "25FF"), ("2000", "206F"),
            ("119E", "119E"), # HANGUL JUNGSEONG ARAEA
            ("318D", "318D")] # HANGUL LETTER ARAEA
        valid_unicode = ("0000", "10FFFF")

        get_ucode = lambda sym : str(sym.encode("unicode-escape"))[5:-1]
        to_hex = lambda s: int(s, 16)
        in_range = lambda ranged, sym : True if to_hex(ranged[0]) <= to_hex(sym) <= to_hex(ranged[1]) else False
        to_remove = self.to_remove

        
        
        for pat in to_remove:
            string = re.sub(pat, "", string)
            
        cleaned=[]    
        for c in string:
            u = get_ucode(c)
            if u == "": # whitespace
                u="0020"
            
            try:
                in_range(valid_unicode, u)
            except ValueError:
                print(u)
                raise
                
            if not in_range(valid_unicode, u):
                continue
            
            sign=False
            for sym in symbols:
                if in_range(sym, u):
                    sign=True
                    break

            if not sign:
                cleaned.append(c)

        return "".join(cleaned)

    
    def split(self, string:str):
        chunks = [(e.group(0), e.span()[0], e.span()[1]) for e in re.finditer(self.delimeter_pattern, string) if re.escape(e.group(0)) not in self.delimeters["single"] and e.group(0) != " "]
        
        split, nouns, nonnouns = [], [], []
        self.vocab = set()
        self.tkn_locs={} # word locations
        
        for chunk, begin, end in chunks:
            for tkn, pos in self.tokenizer.pos(chunk):
                # If the token has space behind it
                self.tkn_locs.setdefault(tkn, [])
                
                for match in re.finditer(re.escape(tkn), chunk):
                    s, e = match.span()
                    if (begin+s, begin+e) not in self.tkn_locs[tkn]:
                        self.tkn_locs[tkn].append((begin+s, begin+e))
                
                
                # Appending as CONTENT WORD or STOPWORD
                if pos in self.content_pos and not re.search(self.stopword_pattern, tkn):
                    # CONTENT WORD
                    self.vocab.add(tkn)
                    nouns.append(tkn)

                    if nonnouns:
                        split.append(tuple(nonnouns))
                        nonnouns=[]
                    

                else: # STOPWORD
                    nonnouns.append(tkn)
                    
                    if nouns:
                        split.append(nouns)
                        nouns=[]
                        
            nonnouns=[]
            if nouns:
                split.append(nouns)
                nouns=[]
                
        nonnouns=[]
        if nouns:
            split.append(nouns)
            nouns=[]

        return split
    
    # Recovering the occurence of the keywords (for spacing)
    def recover_string(self, words):
        
        if len(words) == 1:
            return words[0]
        
        votes={}
        for i in range(len(self.tkn_locs[words[0]])):
            tmp=[words[0]]
            
            for w in range(len(words)-1):
                word1, word2 = words[w], words[w+1]
                passed=False
                
                for s1, e1 in self.tkn_locs[word1]:
                    for s2, e2 in self.tkn_locs[word2]:
                        if e1 + 1 == s2: # with space
                            tmp.extend([" ", word2])
                            passed=True
                            break
                        elif e1 == s2: # without space
                            tmp.append(word2)
                            passed=True
                            break
                    if passed:
                        break
                if not passed:
                    break
                    
            if passed:
                votes["".join(tmp)] = votes.get("".join(tmp), 0) + 1
                
        if votes:
            return max(votes, key=votes.get)
        else:
            return None # if there is big gap between elements
                    
                
    def rake(self, phrases, compound, length_filter):
        indicies = list(self.vocab)
        graph = np.zeros((len(indicies), len(indicies)))
        scores = np.zeros((3, len(indicies)))
        itos, stoi = {i:s for i, s in enumerate(indicies)}, {s:i for i, s in enumerate(indicies)}
        
        
        # Building Co-Occurrence Graph
        for phrase in phrases:
            if isinstance(phrase, list):
                token_type="content"
            elif isinstance(phrase, tuple):
                token_type="stopword"
                
                
            if token_type == "content":
                for i in range(len(phrase)):
                    for j in range(i, len(phrase)):
                        idx1, idx2 = stoi[phrase[i]], stoi[phrase[j]]
                        graph[idx1, idx2] += 1

            
        # Building Scores
        for i in range(len(indicies)):
            freq, deg = graph[i, i].item(), sum(graph[i, :]).item()
            assert freq != 0 and deg != 0
            
            score = deg / freq
            scores[0, i], scores[1, i], scores[2, i] = deg, freq, score
                        
                
        
        result=[]
        already=set()
        for phrase in phrases:
            if isinstance(phrase, tuple):
                continue
            
            score=.0    
            for i in range(len(phrase)):
                idx = stoi[phrase[i]]
                score+=scores[2, idx].item()
                
            keyword = " ".join(phrase)
            
            if keyword not in already:
                result.append((keyword, score, len(phrase)))
                already.add(keyword)

                
        if compound: # Compound Keyword Candidates
            for i in range(len(phrases)-2):
                prior, middle, later = phrases[i], phrases[i+1], phrases[i+2]
                
                # prior must be content words & middle must be stopwords & later must be content words
                if not (isinstance(prior, list) and isinstance(middle, tuple) and isinstance(later, list)):
                    continue 
                
                score=.0
                for j in range(len(prior)):
                    idx = stoi[prior[j]]
                    score+=scores[2, idx].item()
                for j in range(len(later)):
                    idx = stoi[later[j]]
                    score+=scores[2, idx].item()
                    
                    
                concatenated = "".join(prior) + " " + "".join(middle) + " " + "".join(later)
                if concatenated not in already:
                    length = len(prior) + len(middle) + len(later)
                    keywords = " ".join(prior + list(middle) + later)
                    result.append((keywords, score, length))
                    already.add(concatenated)
            
        keywords_by_len ={}
        lengths = [e[2] for e in result]
        mx, mn = max(lengths), min(lengths)
        for keyword, score, length in sorted(result, key=lambda item:item[1], reverse=True):
            recovered = self.recover_string(keyword.split())
            if recovered:
                if length in range(length_filter[0], length_filter[1]+1) and length_filter != (-1, -1) or\
                    (length in range(length_filter[0], mx) and length_filter[0] != -1 and length_filter[1] == -1) or \
                    (length in range(mn, length_filter[1]) and length_filter[0] == -1 and length_filter[1] != -1) or\
                    length_filter == (-1, -1):
                    keywords_by_len.setdefault(length, []).append((recovered, score))
                
        return keywords_by_len
