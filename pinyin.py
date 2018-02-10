import re

def prettify_pinyin(pinyin, delimiter=" "):
    """
    Convert pinyin with tone numbers to pinyin with diacritical marks (e.g. ni3 hao3 --> nǐ hǎo).
    
    Input tone mark number must come after the pinyin letters. It cannot be interspersed with letters:
    
    Yes: ni3 hao3.   No: ni3 ha3o
    
    Function preserves capitalization.
    
    Covers all cases from table of possible endings at http://pinyin.info/rules/where.html
    """
    # Combining marks for consonants (Unicode that combines with previous character, e.g., \u0061\u0304 --> ā)
    # 1st tone --> \u0304 ( ̄ , macron), 2nd tone --> \u0301 ( ́, acute accent), 3rd tone --> \u030C ( ̌, caron) 
    # 4th tone --> \u0300 ( ̀, grave accent), 5th tone --> \u0307 ( ̇, over dot)
    tone_marks = {
                    0: '',
                    1: '\u0304',
                    2: '\u0301',
                    3: '\u030C',
                    4: '\u0300',
                    5: '\u0307'
                 }
    # tones for vowels. 5th tone for ü does not appear in CEDICT
    vowel_tones = {
        'a': {0: 'a', 1: 'ā', 2: 'á', 3: 'ǎ', 4: 'à', 5: 'ȧ'},
        'A': {0: 'A', 1: 'Ā', 2: 'Á', 3: 'Ǎ', 4: 'À', 5: 'Ȧ'},
        'o': {0: 'o', 1: 'ō', 2: 'ó', 3: 'ǒ', 4: 'ò', 5: 'ȯ'},
        'e': {0: 'e', 1: 'ē', 2: 'é', 3: 'ě', 4: 'è', 5: 'ė'},
        'E': {0: 'E', 1: 'Ē', 2: 'É', 3: 'Ě', 4: 'È', 5: 'Ė'},
        'i': {0: 'i', 1: 'ī', 2: 'í', 3: 'ǐ', 4: 'ì', 5: 'i'},
        'u': {0: 'u', 1: 'ū', 2: 'ú', 3: 'ǔ', 4: 'ù', 5: 'u̇̇̇'},
        'ü': {0: 'ü', 1: 'ǖ', 2: 'ǘ', 3: 'ǚ', 4: 'ǜ', 5: 'ü5'},
    }
    pinyin_list = pinyin.split(delimiter)
    pretty_pinyin_list = []
    
    for text in pinyin_list:
        # replace u: and v with ü
        pretty_pinyin = text
        pretty_pinyin = pretty_pinyin.replace('u:', 'ü') #u\u0308
        pretty_pinyin = pretty_pinyin.replace('v', 'ü')

        regex = re.compile(r"([a-zA-Zü]+)([0-5])$") # $ guarantees that only one number matches 'a10'

        match = regex.match(pretty_pinyin)
        if match == None:
            # Remove digits from text
            pretty_pinyin = pretty_pinyin.translate(text.maketrans('', '', '1234567890'))
            pretty_pinyin_list.append(pretty_pinyin)
            continue
        else:
            base = match.group(1)
            tone = int(match.group(2))

            # match vowels
            regex = re.compile(r"[aeiouüAE]+")
            match = regex.search(base)
            if match == None:
                # no vowels
                if base == "xx": # "xx" appears as base for some pinyin in CEDICT. This handles the case as "N/A".
                    # pinyin not applicable
                    pretty_pinyin_list.append("N/A")
                    continue
                # No vowels. Add tone to last character
                # handles m2, m4, etc.
                last_character = base[-1]
                base = base[0:-1] + last_character + tone_marks[tone]
                pretty_pinyin_list.append(base)
                continue
            else:
                vowels = match.group(0)
                # Derived to cover all cases from table of possible endings at http://pinyin.info/rules/where.html
                if 'a' in vowels:
                    base = base.replace('a', vowel_tones['a'][tone])
                elif 'A' in vowels:
                    base = base.replace('A', vowel_tones['A'][tone])
                elif 'e' in vowels: 
                    base = base.replace('e', vowel_tones['e'][tone])
                elif 'E' in vowels:
                    base = base.replace('E', vowel_tones['E'][tone])
                elif 'o' in vowels:
                    base = base.replace('o', vowel_tones['o'][tone])
                elif 'u' in vowels:
                    base = base.replace('u', vowel_tones['u'][tone])
                else:
                    final_vowel = vowels[-1]
                    base = base.replace(final_vowel, vowel_tones[final_vowel][tone])
                pretty_pinyin_list.append(base)
                continue
    
    # re-join list of pretty pinyin
    pinyin_string = delimiter.join(pretty_pinyin_list)
    return pinyin_string