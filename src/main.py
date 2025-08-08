
import string
from collections import Counter, defaultdict
import re

def read_signal(filename='signal.txt'):
    """Read the encrypted signal from file."""
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return None

def get_english_patterns():
    """Return common English patterns for pattern matching."""
    return {
        1: ['A', 'I'],  # Single letter words
        2: ['OF', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'AT', 'SO', 'WE', 'HE', 'BY', 'OR', 'ON', 'DO', 'IF', 'ME', 'MY', 'UP', 'AN', 'GO', 'NO', 'US', 'AM', 'GET'],
        3: ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WHO', 'BOY', 'DID', 'CAR', 'EAT', 'END', 'FAR', 'GOD', 'HOT', 'LET', 'MAN', 'PUT', 'RUN', 'SAY', 'SHE', 'TRY', 'WAY', 'WIN', 'YES', 'YET'],
        4: ['THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'KNOW', 'WANT', 'BEEN', 'GOOD', 'MUCH', 'SOME', 'TIME', 'VERY', 'WHEN', 'COME', 'HERE', 'JUST', 'LIKE', 'LONG', 'MAKE', 'MANY', 'OVER', 'SUCH', 'TAKE', 'THAN', 'THEM', 'WELL', 'WORK']
    }

def analyze_word_patterns(text):
    """Analyze patterns in the text to help with decryption."""
    words = text.split()
    pattern_analysis = defaultdict(list)
    
    for word in words:
        length = len(word)
        if length <= 4:  
            pattern_analysis[length].append(word)
    
    # In this step I am Getting most common words by length
    for length in pattern_analysis:
        counter = Counter(pattern_analysis[length])
        pattern_analysis[length] = counter.most_common(10)  
    
    return pattern_analysis

def create_pattern_based_mapping(text):
    """Create cipher mapping based on word patterns and frequencies."""
    words = text.split()
    word_patterns = analyze_word_patterns(text)
    english_patterns = get_english_patterns()
    
  
    letter_freq = Counter(''.join(words))
    most_common_encrypted = [item[0] for item in letter_freq.most_common()]
    
    # Known English letter frequency order
    english_freq_order = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'U', 'L', 'D', 'C', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
    
    mapping = {}
    

    if 1 in word_patterns and word_patterns[1]:
        single_letters = [word for word, count in word_patterns[1]]
        for i, encrypted_letter in enumerate(single_letters[:2]):  # A and I
            if i < len(['A', 'I']):
                mapping[encrypted_letter] = ['A', 'I'][i]
    

    if 2 in word_patterns and word_patterns[2]:
        # Here I am Looking for different patterns like double letters or common combinations
        two_letter_words = [word for word, count in word_patterns[2]]
        for word in two_letter_words[:5]: 
            if len(set(word)) == 1:  
               
                pass
         
    

    used_english = set(mapping.values())
    used_encrypted = set(mapping.keys())
    
    remaining_encrypted = [c for c in most_common_encrypted if c not in used_encrypted]
    remaining_english = [c for c in english_freq_order if c not in used_english]
    
    for i, enc_char in enumerate(remaining_encrypted):
        if i < len(remaining_english):
            mapping[enc_char] = remaining_english[i]
    
    return mapping

def apply_substitution(text, mapping):
    """Apply substitution mapping to decrypt text."""
    result = ""
    for char in text:
        if char == ' ':
            result += ' '
        elif char in mapping:
            result += mapping[char]
        else:
            result += char  
    return result

def score_english_quality(text):
    """Score how English-like the text appears."""
    words = text.split()
    if not words:
        return -1000
    
    score = 0
    
    # Common English words bonus
    common_words = set(['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'YOU', 'THAT', 'HE', 'WAS', 'FOR', 'ON', 'ARE', 'AS', 'WITH', 'HIS', 'THEY', 'I', 'AT', 'BE', 'THIS', 'HAVE', 'FROM', 'OR', 'ONE', 'HAD', 'BY', 'WORD', 'BUT', 'NOT', 'WHAT', 'ALL', 'WERE', 'WE', 'WHEN', 'YOUR', 'CAN', 'SAID', 'THERE', 'EACH', 'WHICH', 'SHE', 'DO', 'HOW', 'THEIR', 'IF', 'WILL', 'UP', 'OTHER', 'ABOUT', 'OUT', 'MANY', 'THEN', 'THEM', 'THESE', 'SO', 'SOME', 'HER', 'WOULD', 'MAKE', 'LIKE', 'INTO', 'HIM', 'TIME', 'HAS', 'TWO', 'MORE', 'VERY', 'AFTER', 'WORDS', 'ITS', 'JUST', 'WHERE', 'MOST', 'KNOW', 'GET', 'THROUGH', 'BACK', 'MUCH', 'BEFORE', 'GOOD', 'NEW', 'WRITE', 'OUR', 'USED', 'ME', 'MAN', 'TOO', 'OLD', 'SEE', 'NOW', 'WAY', 'WHO', 'BOY', 'COME', 'ITS', 'OVER', 'THINK', 'ALSO', 'BACK', 'AFTER', 'USE', 'TWO', 'HOW', 'OUR', 'WORK', 'FIRST', 'WELL', 'WATER', 'BEEN', 'CALL', 'WHO', 'OIL', 'ITS', 'NOW', 'FIND', 'LONG', 'DOWN', 'DAY', 'DID', 'GET', 'COME', 'MADE', 'MAY', 'PART'])
    
    for word in words:
        if word.upper() in common_words:
            score += 10
        
        if len(word) > 15:
            score -= 20
        elif len(word) == 1 and word.upper() not in ['A', 'I']:
            score -= 5
        elif 3 <= len(word) <= 8:
            score += 1
    
    text_letters = ''.join(words)
    if text_letters:
        letter_freq = Counter(text_letters)
        total = sum(letter_freq.values())
        

        expected_freq = {'E': 0.127, 'T': 0.091, 'A': 0.082, 'O': 0.075, 'I': 0.070, 'N': 0.067}
        
        for letter, expected in expected_freq.items():
            actual = letter_freq.get(letter, 0) / total if total > 0 else 0
            score += max(0, 50 - abs(expected - actual) * 1000)
    

    if text.count('.') > 0 or text.count('!') > 0 or text.count('?') > 0:
        score += 20
    
    return score

def improve_mapping_iteratively(text, initial_mapping, iterations=5):
    """Iteratively improve the mapping by testing alternatives."""
    current_mapping = initial_mapping.copy()
    best_mapping = current_mapping.copy()
    best_score = score_english_quality(apply_substitution(text, current_mapping))
    
    for iteration in range(iterations):

        letters = list(current_mapping.keys())
        for i in range(len(letters)):
            for j in range(i + 1, len(letters)):

                test_mapping = current_mapping.copy()
                test_mapping[letters[i]], test_mapping[letters[j]] = test_mapping[letters[j]], test_mapping[letters[i]]
                

                test_text = apply_substitution(text, test_mapping)
                test_score = score_english_quality(test_text)
                
                if test_score > best_score:
                    best_score = test_score
                    best_mapping = test_mapping.copy()
        
        current_mapping = best_mapping.copy()
    
    return best_mapping, best_score

def find_message_in_signal(signal):
    """Find the 721-character message with the best decryption."""
    message_length = 721
    best_score = float('-inf')
    best_decryption = ""
    best_position = 0
    
    print(f"Scanning {len(signal) - message_length + 1} possible positions...")
    

    for pos in range(len(signal) - message_length + 1):
        if pos % 2000 == 0: 
            print(f"Position {pos}/{len(signal) - message_length + 1}")
        
        candidate = signal[pos:pos + message_length]
        
 
        unique_letters = len(set(c for c in candidate if c.isalpha()))
        if unique_letters < 15: 
            continue
        
  
        initial_mapping = create_pattern_based_mapping(candidate)
        

        improved_mapping, score = improve_mapping_iteratively(candidate, initial_mapping, 3)
        
        if score > best_score:
            best_score = score
            best_decryption = apply_substitution(candidate, improved_mapping)
            best_position = pos
            print(f"New best at position {pos}: score {score:.1f}")
            print(f"Preview: {best_decryption[:100]}")
    
    return best_decryption, best_position, best_score

def extract_first_nine_words(text):
    """Extract the first 9 words from decrypted text."""
    words = text.split()
    return ' '.join(words[:9]) if len(words) >= 9 else ' '.join(words)

def main():
    """Main function to decode the Dyslexian message."""
    print("=" * 60)
    print("NASA DYSLEXIAN MESSAGE DECODER v2.0")
    print("From: The Broom Closet (Now with Better Algorithms!)")
    print("=" * 60)
    

    signal = read_signal()
    if signal is None:
        return
    
    print(f"Signal loaded: {len(signal)} characters")
    
    # In this step I am finding decrypt the message
    decrypted_message, position, score = find_message_in_signal(signal)
    
    print("\n" + "=" * 60)
    print("DECRYPTION RESULTS")
    print("=" * 60)
    print(f"Best match found at position: {position}")
    print(f"Quality score: {score:.1f}")
    
    first_nine = extract_first_nine_words(decrypted_message)
    
    print("\n" + "FIRST 9 WORDS (ANSWER FOR PROPOSAL):")
    print("=" * 50)
    print(first_nine)
    print("=" * 50)
    
    print("\nFULL DECRYPTED MESSAGE:")
    print("-" * 40)
    print(decrypted_message)
    
    print("\nMESSAGE ANALYSIS:")
    print("-" * 40)
    words = decrypted_message.split()
    print(f"Total words: {len(words)}")
    print(f"Total characters: {len(decrypted_message)}")
    print(f"Average word length: {sum(len(w) for w in words) / len(words):.1f}")

if __name__ == "__main__":
    main()