from nltk import ngrams, word_tokenize, sent_tokenize, ConditionalFreqDist
import re
import random

def preprocess_corpus(corpus_file):
	with open(corpus_file, 'r') as f:
		corpus = f.read()
	corpus = sent_tokenize(corpus)
	corpus = [word_tokenize(s) for s in corpus]
	return corpus

def make_ngrams(n, corpus):
	ngrams_ = [tuple(ngrams(s, n, 
					pad_right=True, right_pad_symbol='</s>',
					pad_left=True, left_pad_symbol='<s>'))
				for s in corpus]
	ngrams_ = [g for t in ngrams_ for g in t]				#flatten the list
	return ngrams_



def get_ngram_frequencies(ngrams):
	freq = ConditionalFreqDist((ngram[:-1], ngram[-1]) for ngram in ngrams)
	return freq


def get_start_sequence(ngrams):
	while True:
		start_sequence = random.choice(ngrams)
		if not re.findall(r"</s>|\.|n't|'s|'m|'d|'ve|\,", start_sequence[0]):
			break
	return start_sequence

def get_most_common_matches(previous_words, frequencies):
	previous_words = tuple(previous_words)
	matches = dict(frequencies[previous_words])
	matches = sorted(matches, key=matches.get, reverse=True)[:5]
	return matches


def get_next_word(most_common_matches):
	return random.choice(most_common_matches)

def postprocess_sentence(sentence):
    sent  = [w for w in sentence if '<' not in w]
    sent[0] = sent[0].capitalize()
    sent = " ".join(sent)
    sent = re.sub(r" (?=;|'|\.|,|n't|[!]|[?])", "", sent)
    sent += " "
    return sent

def generate_text(n, n_sentences, corpus_file):
	corpus = preprocess_corpus(corpus_file)
	ngrams_ = make_ngrams(n, corpus)
	freqs = get_ngram_frequencies(ngrams_)
	output = ""
	for i in range(n_sentences):
		sent = []
		sent.extend(get_start_sequence(ngrams_))
		while True:
			previous_words = sent[-(n-1):]
			matches = get_most_common_matches(previous_words, freqs)
			next_word = get_next_word(matches)
			sent.append(next_word)
			if next_word == '</s>':
				break
		output += postprocess_sentence(sent)
	return output



	
n = 3
print('GENERATED:', generate_text(n, 5, 'witcher_quotes.txt'))
# grams = make_ngrams(n, preprocess_corpus('witcher_quotes.txt'))
# print(grams[:50])
# freqs = get_ngram_frequencies(grams)
# start = list(freqs[('<s>', '<s>')])
# print(start)
# print(random.choice(start))

# print(get_most_common_matches(('<s>', '<s>'), freqs))
#print(preprocess_corpus('witcher_quotes.txt'))
# output = []
#output.extend(get_start_sequence(freqs))
# print(get_start_sequence(freqs))

# print(output)
# print(output[-(n-1):])
