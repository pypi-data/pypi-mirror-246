import os, re
from .base import ChunkingPipeline, Chunk, Document
import bustercp.constants.chunkingconstants as const
from bustercp.utils.scoreref import calc_score, classify_text
from nltk.tokenize import sent_tokenize
from bustercp.utils.utils import iso_to_country_name

class ChunkingPipelineBeta(ChunkingPipeline):


    def transform(self, documents: list[Document]) -> list[Chunk]:
        docs_new_dict = self.clean_docs_raw_text(documents) 

        chunks = []

        for doc_id, text in docs_new_dict.items():
            text = re.sub(r'\s{2,}', ' ', text)
            text = re.sub(r'\.{2,}', '.', text)
            text = text.strip()
            sentences = sent_tokenize(text)
            t_final = "" # text that is written to file- we join few sentences to block of text that should be smaller than max_length

            p_id = 0
            
            for i,t in enumerate(sentences):
                max_length = self.chunk_max_length
            
                if i == len(sentences)-1:
                    t_final += " " + t if len(t_final) > 0 else t

                    if len(t_final) > 0: chunks.append(Chunk(doc_id, p_id, t_final))
                elif (len(t_final) + len(t)) < max_length:
                    t_final += " " + t if len(t_final) > 0 else t
                elif (len(t_final) + len(t)) >= max_length:

                    if len(t_final) > 0: chunks.append(Chunk(doc_id, p_id, t_final))

                    t_final = t
                    p_id += 1


        for i in range(len(chunks)):
            first_char = chunks[i].text[0]

            if first_char in const.indents:
                chunks[i].text = chunks[i].text[1:].strip()

        print(f'chunks.len={len(chunks)}')
        return chunks
        

    def clean_docs_raw_text(self, documents: list[Document]):
        docs_new_dict = {}
        initial_paragraphs = self.create_initial_paragraphs(documents) # 1d array of pairs (document_id, paragraph_text)
        print("initial_paragraphs.len=%d" % len(initial_paragraphs))
        assigns = self.assign_paragraphs(initial_paragraphs)
        
        for i, (doc_id, text) in enumerate(initial_paragraphs):

            assign = assigns[i]

            if not doc_id in docs_new_dict:
                docs_new_dict[doc_id] = ""

            if assign == 'FT' and len(text) > 70: # 'healty text', threshold(len) to skip headings, page numberings, etc.
                docs_new_dict[doc_id] += " " + text

            elif assign == 'FR' and len(text) > 800: # try to extract some nonreference stuff from text- skip smaller texts (threshold)
                subparagraphs = self.split_into_subparagraphs(text)

                for t in subparagraphs:
                    s_score = calc_score(t)
                    s_assign = classify_text(s_score)

                    if s_assign == 'FT' and len(t) > 30: # this text chunk is ok
                        docs_new_dict[doc_id] += t + "."
                    else: # throw away text chunk
                        pass
                
            else: # throw away text chunk
                pass

        return docs_new_dict # dict, key-doc_id, val-text (document text, cleaned with reference classifier)


    def split_into_sentences(self, text):
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(const.prefixes,"\\1<prd>",text)
        text = re.sub(const.websites,"<prd>\\1",text)
        text = re.sub(const.digits + "[.]" + const.digits,"\\1<prd>\\2",text)
        if "..." in text: text = text.replace("...","<prd><prd><prd>")
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + const.alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(const.acronyms+" "+const.starters,"\\1<stop> \\2",text)
        text = re.sub(const.alphabets + "[.]" + const.alphabets + "[.]" + const.alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(const.alphabets + "[.]" + const.alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+const.suffixes+"[.] "+const.starters," \\1<stop> \\2",text)
        text = re.sub(" "+const.suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + const.alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences


    def split_into_subparagraphs(self, text):
        subparagraphs = re.split(r'(?<!(\s[a-zA-Z]))((?<!(\s[a-zA-Z][a-zA-Z])))(\.)(?!(\s\(20[0-2][0-9]\)))', text)
        subparagraphs = [s + '.' for s in subparagraphs if s != None and len(s) > 0]
        return subparagraphs

    def assign_paragraphs(self, paragraphs:list):
        assigns = []
        assign_count = {'FT':0, 'FR':0, 'M': 0, '?':0}

        for doc_id, text in paragraphs:
            score = calc_score(text)
            assign = classify_text(score)
            assigns.append(assign)
            assign_count[assign] += 1
        
        # print("assign_count=%s" % repr(assign_count))
        return assigns
        
        
    def is_avg_word_len_ok(self, text):
        words = text.split()
        avg_word_len = sum([len(w) for w in words])/len(words) if len(words) > 0 else 0

        return avg_word_len >= 2

    def clean_text(self, text):
        clean_text = text.replace('\n', ' ').replace('\t', ' ')
        clean_text = clean_text.replace('\0','').replace('\f', ' ')
    

        for symbol in const.symbols_blacklist:
            clean_text = clean_text.replace(symbol, '')
    
        clean_text = re.sub('\(cid:\d+\)', ' ', clean_text) # 50 10
        clean_text = re.sub(' +', ' ', clean_text)
        clean_text = re.sub('\d+\s\d+', ' ', clean_text) # 50 10
        clean_text = re.sub('\(\d{1,2}\)', ' ', clean_text) # 50 10
        clean_text = clean_text.strip()

        return clean_text


    def can_join_next(self, i, j, splitted):

        last_char = splitted[i][-1]
        last_word =  splitted[i].partition(' ')[-1].strip()

        if j > len(splitted)-1:
            return False

        first_char = splitted[j][0]
        first_word = splitted[j].split(' ', 1)[0].strip()

        if len(first_word) >= 2:
            remain = first_word[0: len(first_word)-1]
            last_char_first_word = first_word[-1]

            if remain.isnumeric() and last_char_first_word in const.numberings:
                return True

        if last_char == const.colon and first_char in const.punctuations:
            return True

        if last_char not in const.indents and (first_char.islower() or first_char in const.valid_first_char_list):
            return True

        if last_char not in const.indents and first_word.isnumeric():
            return True

        if last_word.isnumeric():
            return True

        if first_char in const.indents:
            return True

        return False


    def create_initial_paragraphs(self, documents: list[Document]):
        initial_paragraphs = []
        paragraph_id = 0

        for document in documents:  
            paragraphs = self.split_raw_text_to_paragraphs(document.text)
            initial_paragraphs.extend([(document.id, p) for p in paragraphs])
            paragraph_id += 1

        return initial_paragraphs


    def split_raw_text_to_paragraphs(self, raw_text:str):

        splitted = re.split('\n{2,}', raw_text)

        paragraphs = []
        text = ""
        i = 0

        while i < len(splitted):

            text_i = self.clean_text(splitted[i])

            if len(text_i) == 0 or not self.is_avg_word_len_ok(text_i):
                i += 1
                continue

            j = i + 1
            text = text_i

            while j < len(splitted):
                text_j = self.clean_text(splitted[j])

                if len(text_j) == 0 or not self.is_avg_word_len_ok(text_j) or text_j.isupper():
                    j += 1
                    continue

                if self.can_join_next(i, j, splitted):
                    text += " " + text_j
                    j += 1
                else:
                    break

            paragraphs.append(self.clean_text(text))

            i = j
            text = ""

        return [p for p in paragraphs if len(p) > 80]
