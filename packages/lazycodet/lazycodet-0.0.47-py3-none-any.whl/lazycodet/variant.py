from unidecode import unidecode
import pickle, os
import re
from tqdm import tqdm

class Dictionary:
    path_data_folder = ''
    variant_live_full_path = ''
    valid_words = {}
    @staticmethod
    def setPath(path):
        Dictionary.path_data_folder = path
        Dictionary.variant_live_full_path = Dictionary.path_data_folder + '/variant-live-full' 
        # Load dictionary chính
        data = pickle.load( open(  os.path.join(Dictionary.path_data_folder,'dictionary'), "rb" ) )
        Dictionary.valid_words = set(data['words'])
        
    @staticmethod
    def check(word):
        pathFile = os.path.join(Dictionary.variant_live_full_path, word)
        if os.path.exists(pathFile):
            variant = pickle.load( open(  pathFile, "rb" ) )
            return {'exist': True, 'variant': variant, 'word': word}
        else:
            return {'exist': False, 'word': word}
  
    @staticmethod
    def add(word, variants, forceUpdateDictionary = False):
        checkResult = {}
        if forceUpdateDictionary == False:
            checkResult = Dictionary.check(word)
        else:
            checkResult['word'] = word
        if forceUpdateDictionary or ( checkResult and checkResult['exist'] == False):
            #variants có thể sẽ chứa rất nhiều biến thể không hợp lệ với tiếng Việt
            # .. ta sẽ lọc lại rồi mới lưu
            # filterVariants = set()
            # for va in variants:
            #     if va in Dictionary.valid_words:
            #         filterVariants.add(va)
          
            os.makedirs(Dictionary.variant_live_full_path, exist_ok=True)
            with open(os.path.join(Dictionary.variant_live_full_path, checkResult["word"]), 'wb') as variant_live_full:
                pickle.dump(variants, variant_live_full)
class Variant:
    
    MAX_CHAR = 7 # Từ trong tiếng việt chỉ có tối đa 7 kí tự
    cumPhuAm = set(['ng', 'th', 'ph', 'ch', 'kh', 'qu', 'tr', 'gi', 'nh'])
    letters_v_khongDau = set(['ă', 'ê', 'ô', 'ơ', 'ư'])
    letters_v_coDau = set(['ạ', 'ã', 'ả', 'á', 'à', 'ặ', 'ẵ', 'ẳ', 'ắ', 'ằ', 'ậ', 'ẫ', 'ẩ', 'ấ', 'ầ', 'â', 'ẹ', 'ẽ', 'ẻ', 'é', 'è', 'ệ', 'ễ', 'ể', 'ế', 'ề', 'ị', 'ĩ', 'ỉ', 'í', 'ì', 'ọ', 'õ', 'ỏ', 'ó', 'ò', 'ộ', 'ỗ', 'ổ', 'ố', 'ồ', 'ợ', 'ỡ', 'ở', 'ớ', 'ờ', 'ụ', 'ũ', 'ủ', 'ú', 'ù', 'ự', 'ữ', 'ử', 'ứ', 'ừ', 'ỵ', 'ỹ', 'ỷ', 'ý', 'ỳ'])
    letter_v = letters_v_khongDau.union(letters_v_coDau)
    letter_v_normal = set(['q','e','r','t','y','u','i','o','p','a','s','d','g','h','k','l','x','c','v','b','n','m'])
    letter_e = set(['w','f','j','z'])
    letters = letter_v_normal.union(letter_v) # All kí tự tiếng việt có dấu và không dấu và latin Việt
    nguyenAm = set(['o','a','e','u','i']) 
    neverInLast = set(['b','d','q','r','k','e','x','v', 'l','ă','ầ', 'ẵ','ẳ','ẫ']) # Những từ không bao giờ nằm ở cuối từ trong tiếng Việt
    arrFirstCharSpecial = [
                    {
                        'd': ['đ']
                    },
                    {
                        'u': ['ư', 'ứ']
                    },
                    {
                        'o': ['ó', 'ố','ọ','ồ','ổ']
                    },
                    {
                        'a': ['á', 'ả','ạ','ả','â','ấ', 'ă']
                    }
                    ]
    @staticmethod
    def split(word):
        return [(word[:i].lstrip(), word[i:].rstrip()) for i in range(len(word) + 1)]
    @staticmethod
    def replace(word):
        if word == '':
            return []
        # Xử lí các biến thể có các từ mà có kí tự đầu tiên có thể chứa các biến thể khác như 'dat', 'đat', 'ong', 'óng', 'ống',...
        arr = set([l + c + r[1:] for l, r in Variant.split(word) if r for c in Variant.letters])
        for char_dict in Variant.arrFirstCharSpecial:
            for key, values in char_dict.items():
                if word[0] == key:
                    for v in values:
                        newWord = v + word[1:]
                        arr.update([newWord])
                        arr.update([l + c + r[1:] for l, r in Variant.split(newWord) if r for c in Variant.letters])
        
        return arr
    def generate_deletes(splits):
        result = set()

        for l, r in splits:
            soTuMuonCat = len(l) + 1
            if ' ' in l:
                arr = l.split()
                if len(arr) == 1:
                    continue
                firstWordInPharse = arr[0]
                aPartSecondWordInPharse = arr[1]
                secondWordInPharse = aPartSecondWordInPharse + r
                if len(firstWordInPharse) > soTuMuonCat:
                    result.add(firstWordInPharse[soTuMuonCat:] + ' ' + secondWordInPharse)
                    
                if len(secondWordInPharse) > soTuMuonCat:
                    result.add(firstWordInPharse + ' ' + secondWordInPharse[soTuMuonCat:])
            if ' ' in r:
                arr = r.split()
                if len(arr) == 1:
                    continue
                secondWordInPharse = arr[1]
                aPartFirstWordInPharse = arr[0]
                firstWordInPharse = l + aPartFirstWordInPharse
                if len(firstWordInPharse) > soTuMuonCat:
                    result.add(firstWordInPharse[soTuMuonCat:] + ' ' + secondWordInPharse)
                    
                if len(secondWordInPharse) > soTuMuonCat:
                    result.add(firstWordInPharse + ' ' + secondWordInPharse[soTuMuonCat:])

        return result
    @staticmethod
    def insertCharToWord(char, word):
        """
        `Variant.insertCharToWord('1', 'hello')`
        
        ['1hello', 'h1ello', 'he1llo', 'hel1lo', 'hell1o', 'hello1']

        `Variant.insertCharToWord('2', 'Xin chào')`
        
        ['2Xin chào', 'X2in chào', 'Xi2n chào', 'Xin2 chào', 'Xin 2chào', 'Xin c2hào', 'Xin ch2ào', 'Xin chà2o', 'Xin chào2']

        `Variant.insertCharToWord('2', 'Nghiêng ngã')`

        ['Nghiêng 2ngã', 'Nghiêng n2gã', 'Nghiêng ng2ã', 'Nghiêng ngã2']

        `Variant.insertCharToWord('2', 'Ngã Nghiêng')`

        ['2Ngã Nghiêng', 'N2gã Nghiêng', 'Ng2ã Nghiêng', 'Ngã2 Nghiêng']
        """
        # Tạo danh sách các vị trí từ 0 đến độ dài của chuỗi
        positions = list(range(len(word) + 1))

        # word có thể là từ đơn hoặc cụm từ - Mà ở tiếng Việt, 1 từ tối đa chỉ có 7 kí tự, vậy nên phải kiểm tra nếu từ nào 
        # .. có chiều dài không thể thêm được thì không cần thêm
        if Variant.isPhrase(word):
            arrWord = word.split()
            firstWord = arrWord[0]
            secondWord = arrWord[1]
            startRange = 0
            endRange = len(word) + 1
            if len(firstWord) + 1 > Variant.MAX_CHAR:
                startRange = len(firstWord) + 1
                
            if len(secondWord) + 1 > Variant.MAX_CHAR:
                endRange = len(word) - len(secondWord)
                
            positions = positions[startRange:endRange]

        # Chèn giá trị của c vào các vị trí
        variants = [word[:pos] + char + word[pos:] for pos in positions]

        return variants
    @staticmethod
    def isPhrase(word):
        if ' ' in word:
            return True
        else:
            return False
    @staticmethod
    def generate_inserts(word):
        result = set([])
        for c in Variant.letters:
            result.update(Variant.insertCharToWord(c, word))
        return result
    @staticmethod
    def countNguyenAm(word):
        demNguyenAm = 0
        for c in [char for char in word]:
            if unidecode(c) in Variant.nguyenAm:
                demNguyenAm +=1
        return demNguyenAm
    @staticmethod
    def isFirstWordOfPhrase(word_array, leftCut):
        """
        #### Hàm kiểm tra từ đang xét là từ thứ nhất hay thứ 2 nếu như đang làm việc với cụm từ
        `word_array`: các mảng chứa các từ của cụm từ
        `leftCut`: là chuỗi bên trái bị cắt
        """

        return len(leftCut) <= len(word_array[0]) # Nếu như chiều bên phải đang xét nhỏ hơn hoặc bằng chiều dài của từ đầu tiên trong cụm từ thì nó đang xét từ đầu tiên
    @staticmethod
    def CheckValid_CumPhuAm(wordArray, leftCut):
        # Kiểm tra nếu từ không hợp lệ sẽ bỏ qua (Tiệt kiệm thời gian)
        for w in wordArray:
            #Vì đây là hàm tạo biến thể tiếng việt, nên nếu từ có chứa kí tự tiếng anh và số, nên sẽ không cần phải tạo
            for c in w:
                if c in Variant.letter_e or c.isdigit():
                    return set()
            # Trong tiếng việt có những từ có 6 đến 7 kí tự, tất cả chúng đều có điểm chung là chứa các cụm phụ âm, nên nếu từ mà có 6-7 kí tự mà không chứa
            # .. cụm phụ âm ở phía đầu coi như là từ không hợp lệ
            lenWord = 0
            w = None

            if Variant.isFirstWordOfPhrase(wordArray, leftCut):
                w = wordArray[0]
            else:
                w = wordArray[1]
            lenWord = len(w)
            if lenWord >=8:
                return False
            if lenWord >= 6:
                if w[:2] not in Variant.cumPhuAm: # 2 kí tự đầu tiên không nằm trong cụm phụ âm
                    return False
        return True
    @staticmethod
    def getPositionOfSecondWordInPhrase(wordArray, leftCut):
        return len(leftCut) - len(wordArray[0])
    @staticmethod
    def solvePositionAndLength(wordArray, leftCut, word):
        #l ở đây sẽ có dạng:
        #v
        #vi
        #viê
        #viêz
        # Như vậy ta sẽ kiểm tra nếu như mà = 4 thì chỉ kiểm tra khi l có chiều dài == 3 hoặc == 2
        lenWord = 0
        position = 0
        if len(wordArray) >=2 :
            if Variant.isFirstWordOfPhrase(wordArray, leftCut):
                lenWord = len(wordArray[0])
                position = len(leftCut) + 1
            else:
                lenWord = len(wordArray[1])
                """
                Giả sử: "đất nước"
                - Chiều dài của từ sắp gắn dấu được tính `len(l) + 1` . Nhưng mà điều này không đúng với từ thứ 2 trong cụm từ
                -> `len(l) - len(wordArray[0]) + 2`
                """
            
                position = Variant.getPositionOfSecondWordInPhrase(wordArray, leftCut)
        else:
            lenWord = len(word)
            position = len(leftCut) + 1
        return lenWord, position

    @staticmethod
    def replacer_do(result_letters_v, word):
       
        demNguyenAm = Variant.countNguyenAm(word)
        # Kiểm tra nếu từ không hợp lệ sẽ bỏ qua (Tiệt kiệm thời gian)
        splitChar = ' '
        if '_' in word:
            splitChar = '_'
        wordArray = word.split(splitChar)
        isPhrase = len(wordArray) >= 2
        
        # Kiểm tra xem từ / cụm từ có kí tự cuối cùng hợp lệ trong tiếng việt không.
        for w in wordArray:
            if w == '' or w[-1] in Variant.neverInLast:
                return set()
        #
        for idx, (l, r) in enumerate(Variant.split(word)):
            
            if isPhrase:
                if 1 - Variant.getPositionOfSecondWordInPhrase(wordArray, l) == 0:
                    if Variant.CheckValid_CumPhuAm(wordArray, l) == False:
                        return set()
            else:
                if idx == 0:
                    if Variant.CheckValid_CumPhuAm(wordArray, l) == False:
                        return set()

            nextL = ''
            nextL_unaccent = ''
            currentL = ''
            lenWord, position = Variant.solvePositionAndLength(wordArray, l, word)
            if position == 1:
                for char_dict in Variant.arrFirstCharSpecial:
                    for key, values in char_dict.items():
                        if word[idx] == key and idx+1 < len(word):
                            result_letters_v_two = []
                            
                        
                            for v in values:
                                if Variant.isFirstWordOfPhrase(wordArray, l):
                                    newWord = v + r[1:]
                                else:
                                    newWord = wordArray[0] + '_' + v + r[1:]
                                newWord = newWord.replace(' ', '_')
                                result_letters_v.add(newWord)
    
                            for c in Variant.letters_v_coDau:
                                nextL = word[idx+1]
                                nextL_unaccent = unidecode(nextL) 
                                if idx + 2 < len(word):
                                    # Giả sử trường hợp mà xuối thì:
                                    # currentL = x
                                    # nextL = u
                                    # next_nextL = ố
                                    # thì trong lần chạy lặp này nó sẽ gán nhãn cho nextL, mà rõ ràng ở tiếng việt không có trường hợp
                                    # .. từ có 2 dấu ví dụ như "xúối" nên không cần xử lí cho trường hợp này
                                    next_nextL = word[idx + 2]
                                    if next_nextL in Variant.letters_v_coDau:
                                        break
                                if unidecode(c) == nextL_unaccent:
                                    right = r[2:]
                                    for v in values:
                                        if Variant.isFirstWordOfPhrase(wordArray, l):
                                            newWord = v + c + right
                                            newWord = newWord.replace(' ', '_')
                                        else:
                                            newWord = wordArray[0] + '_' + v + c + right
                                        
                                        result_letters_v.add(newWord)
                                    # result_lan2 = replacer_do(result_letters_v.copy(), lenWord, newWord)  # Tạo bản sao của tập hợp
                                    # result_letters_v_two.extend(result_lan2)
                            for item in result_letters_v_two:
                                result_letters_v.add(item)
                continue
            if unidecode(l[0]) != unidecode(word[0]):
                continue
            if len(l) >= len(word):
                continue
            currentL = word[len(l) - 1]
            nextL = word[len(l)]
            # Nếu từ kí tự tiếp theo muốn thêm dấu mà nó đã có dấu rồi thì không cần thêm dấu
            if currentL == 'đ':
                pass
            if nextL in Variant.letters_v_khongDau:
                continue
            elif nextL in Variant.letters_v_coDau:
                if isPhrase: 
                    # Nếu như là cụm từ mà hiện tại đang xét ở từ đầu tiên, thì sẽ không break ngay chuyển sang kiểm tra 
                    # .. từ thứ 2 của cụm từ
                    if Variant.isFirstWordOfPhrase(wordArray, l):
                        continue
                break
            nextL_unaccent = unidecode(nextL)
            next_nextL = None
            if len(l) + 1 < len(word):
                # Giả sử trường hợp mà xuối thì:
                # currentL = x
                # nextL = u
                # next_nextL = ố
                # thì trong lần chạy lặp này nó sẽ gán nhãn cho nextL, mà rõ ràng ở tiếng việt không có trường hợp
                # .. từ có 2 dấu ví dụ như "xúối" nên không cần xử lí cho trường hợp này
                next_nextL = word[len(l) + 1]
                if next_nextL in Variant.letters_v_coDau:
                    break

            
            
            
            

            if  lenWord == 4 and position != 3 and position != 2: # tại sao lại là len(l) + 1 -- Bởi vì khi len(l) == 2 thì chạy đoạn code phía dưới (l + c) thì nó sẽ là 3
                continue
            if nextL_unaccent not in Variant.nguyenAm: # Nếu không phải là nguyên âm thì không cần phải thêm dấu
                continue
            # Với đoạn if phía trên lúc này nó đã giới hạn lại các biến thể với từ "viêz"
            # .. ban đầu là 27560 sau đó chỉ còn lại => 6968
            # Tương tự như vậy với các trường hợp mà từ word là 3 kí tự thì thông thường
            # .. dấu câu sẽ đặt ở 3 kí tự luôn như "ủng" hộ, "cũng", "nhỉ"
            # .. nên trường hợp có 3 kí tự sẽ không cần làm gì mà lấy hết tất cả các biến thể của nó
            # Với trường hợp có 2 kí tự như "Uỷ" ban, "Êm" đềm thì cũng tương tự nên cũng sẽ bỏ qua
            # Với trường hợp có 1 kí tự vẫn tương tự
            # Với trường hợp có 5 kí tự như "nguyễn", "quyết", "chính". Thì dấu câu sẽ rơi vào
            # .. vị trí kí tự thứ 3 hoăc 4 hoặc thứ 2 (dưỡng)
            # .. giả sử lấy ví dụ word="quyêz" thì len của myResult sẽ là 43030 biến thể
            if lenWord == 5 and (len(l) + 1 != 2 and len(l) + 1 != 3 and len(l) + 1 != 4): # tại sao lại là len(l) + 1 -- Bởi vì khi len(l) == 2 thì chạy đoạn code phía dưới (l + c) thì nó sẽ là 3
                continue
            # .. Sau khi có sự ràng buộc của if phía trên cho kết quả len của myResult sẽ là 17290 biến thể
        

            if r:
                for c in Variant.letter_v:
                    if unidecode(c) == nextL_unaccent:
                        # Nếu như kí tự cuối cùng hiện tại đã là 1 nguyên âm có dấu, 
                        # .. thì sẽ không có trường hợp kí tự tiếp theo lại là có dấu nữa
                        # .. ví dụ không có trường hợp thôí
                        # .. nhưng mà chữ 'thôí' phía trên có 3 kí tự, nếu như 1 từ mà có 3
                        # .. nguyên âm như 'bướu' thì rõ ràng chữ 'ư' vẫn có khả năng có chữ ớ là nguyên âm có dấu
                        
                        if demNguyenAm < 3:
                            if currentL in Variant.letters_v_coDau and nextL in Variant.letters_v_coDau: # ô not in [o,a,e,u,i]
                                continue
                        else:
                            if len(l) >= 3 and len(word) < 5: # len(word) < 5 là bởi bì ví dụ như từ "người" có 3 nguyên âm nhưng mà nó tới 5 kí tự nên nó vẫn có khả năng có từ nguyên âm có dấu cho từ trước
                                beforeL = word[len(l) - 1]
                                if unidecode(beforeL) in Variant.nguyenAm: # ô in [o,a,e,u,i]
                                    continue
                        # Trong tiếng việt chữ 'q' thì đi sau nó chỉ có chữ 'u' thôi và nó luôn luôn nằm ở vị trí kí tự đầu tiên
                        if l[-1] == 'q' and c != 'u':
                            continue
                        
                        newWord = l + c + r[1:]
                        newWord = newWord.replace(' ', '_')
                        result_letters_v.add(newWord)
                        if isPhrase:
                            # Thêm dấu cho next_nextL (kí tự kế tiếp của kí tự kế tiếp) nếu có thể
                            # Vì có trường hợp như "phưong an" nó chỉ tạo ra được "phương an"
                            # Thông thường đi sau ư có thể là ơ, nên là kiểm tra nếu từ kế tiếp là o thì sẽ thực hiện thêm 1 trường hợp ơ cho biến thể này
                            # Nên ta sẽ lợi dụng nếu như biến thể "thưong an" sẽ cho nó chạy 2 lần hàm này để gắn dấu cho từ thứ 2 trong cụm từ 
                            if next_nextL is not None and c == 'ư' and next_nextL == 'o' and Variant.countNguyenAm(wordArray[1]) >=1: 
                                newWord = l + c + 'ơ' + r[2:]
                                Variant.replacer_do(result_letters_v, newWord)
        return result_letters_v
    @staticmethod
    def create(w, run2Times = True):
        """
        #### Hàm tạo các biến thể - Quy định số lần tạo biến thể
        run2Times - Tham số này dùng trong 2 trường hợp sau:
        + Nếu như gọi trực tiếp hàm này sử dụng mà từ truyền vào là 1 từ tiếng Việt không dấu ví dụ như "buou" thì nó bắt buộc phải chạy 2 lần hàm replacer_do thì mới có thể thêm dấu cho cả chữ `u` và `o`
        + Nếu như gọi hàm này từ hàm `editAndCreate` thì chỉ cần chạy 1 lần, vì ở hàm `editAndCreate` đã có phần xử lí `Variant.replace(word)` nên là nó đã tạo ra các biến thể có sẵn 1 dấu, chẳng hạn như nó đã tạo ta được 1 biến là chữ 'bưou' trước khi chạy vào hàm `create` này nên là nó sẽ tạo ra được chữ `bươu` dù chỉ chạy 1 lần
        """
        # Nếu là tiếng ảnh thì ở chỗ dòng code trên đã có thể return ra result_letters rồi
        # .. nhưng mà đây là tiếng việt nên phải thêm một lần replace cho trường hợp các kí tự có dấu nữa
        # .. ví dụ từ word là "viêz", thì ở trên chỉ có thể sửa thành "viêt" mà không có trường hợp cho "việt"
        # .. chính vì thế nên phải thêm 1 bước thêm dấu nữa
        # giả sử với word="viêz" thì ở đây chiều dài là 104 biến thể được tạo ra
                                # nhưng sau đó chạy thêm đoạn code dưới sẽ tạo ra tổng là 27560 biến thể
                                # nó quá lớn nên phải phân tích 1 chút để giới hạn điều này lại
                                # giả sử với các từ tiếng việt có 4 kí tự thì thông thường thì dấu câu
                                # .. sẽ nằm ở kí tự thứ 3
        myResult = []
        result_letters_v = set()
    
        result = [w]
        result += Variant.replacer_do(result_letters_v, w)
        myResult.extend(result)
        if run2Times:
            # Với những từ có 3 nguyên âm như "buou" thì phải chạy 2 lần. Vì ví dụ như lần thứ nhất "bưou" => chưa có nghĩa
            # .. phải chạy thêm lần 2 thì mới có trường hợp là "bướu"
            # --------------
            # Sau nhiều lần thử nghiệm thì cuối cùng phát hiện có từ 2 nguyên âm vẫn phải chạy lần như chữ 'được'
            demNguyenAm = Variant.countNguyenAm(w)
            # if demNguyenAm == 3 or (demNguyenAm == 2 and len(w) == 5):
            if demNguyenAm >=2:
                for my_w in result_letters_v.copy():  # Tạo bản sao của tập hợp
                    
                    result_lan2 = Variant.replacer_do(result_letters_v.copy(), my_w)  # Tạo bản sao của tập hợp
                    myResult.extend(result_lan2)
    
        return set(myResult)
    def editAndCreate(word, debug = False, forceUpdateDictionary = False):
        
        result = set()
        rootWord = word
        word = word.lower().strip()
        word = unidecode(word)
        rootWordToLowerAndUnidecode = word
        isPharse = Variant.isPhrase(rootWord)
         # Xoá bỏ số và các ký tự [w, f, j, z]
        word = re.sub(r'[\dwfjz]', '', word)
        word = word.strip() # Sau khi xoá kí tự ở trên xong phải strip() lại
        # Giả sử word = 'Điều 6' sau khi thực thực hiện đoạn code xoá trên từ cụm từ sẽ trở thành đơn từ 'Điều' => Không phải cụm từ
        if isPharse and Variant.isPhrase(word) == False:
            return set([])
        # Giả sử word = '2' thì ở đoạn code trên sau khi chạy xong word sẽ = rỗng
        if word == '':
            return set([])
        result.update([rootWordToLowerAndUnidecode]) # Thêm từ muốn sửa vào luôn, vì đôi khi từ gốc đưa vào là tiếng anh, mà hàm tạo biến thể chỉ tạo tiếng việt nên đôi khi nó đã sửa từ tiếng anh đúng thành từ khác
        if debug == False and forceUpdateDictionary == False:
            resultCheckDictionary = Dictionary.check(word)
            if resultCheckDictionary['exist'] == True:
                return resultCheckDictionary['variant']
            

        splits = Variant.split(word)
        deletes = []
        inserts = []
        
        if len(word) > 1:
            if isPharse:

                deletes = Variant.generate_deletes(splits)

            else:
                deletes = set([(l + r[1:]).strip() for l,r in splits if r])
        if isPharse:
            inserts = Variant.generate_inserts(word)
        else:
            if len(word) + 1 <= Variant.MAX_CHAR:
                inserts = set([l + c + r for l, r in splits for c in Variant.letters])
            if len(word) == 1 and len(word) + 2 <= Variant.MAX_CHAR: # Nếu từ có 1 kí tự thì sẽ lấy ra biến thể có 3 kí tự
                inserts = inserts.union(set([l + c + r + c2 for l, r in splits for c in Variant.letters for c2 in Variant.letters]))
 
        swaps = set([(l + r[1] + r[0] + r[2:]).strip() for l, r in splits if len(r)>1])
        replaces = Variant.replace(word)


        for w in deletes:
            result.update(Variant.create(w, run2Times=False))
        for w in inserts:
            result.update(Variant.create(w, run2Times=False))
        for w in swaps:
            result.update(Variant.create(w, run2Times=False))
        for w in replaces:
            result.update(Variant.create(w, run2Times=False))
        if debug and forceUpdateDictionary == False:
            # Mở file để ghi
            with open('./output_editAndCreate' , "w", encoding="utf-8") as file:
                # Ghi từng phần tử trong mảng vào file
                for candidate in result:
                    file.write(candidate + "\n")
        else:
            Dictionary.add(word, result, forceUpdateDictionary)
        return result
    @staticmethod
    def updateAllVariantsLive():
        folder_path = Dictionary.variant_live_full_path 
        file_names = os.listdir(folder_path)
        file_names = [file for file in file_names if os.path.isfile(os.path.join(folder_path, file))]

        # Tạo thanh tiến trình với tổng số lượng tệp
        progress_bar = tqdm(file_names, desc="Processing files", unit="file")

        for word in progress_bar:
            word = word.replace('_', ' ')
            Variant.editAndCreate(word, forceUpdateDictionary=True)
            
            # Cập nhật thanh tiến trình
            progress_bar.update(1)

        # Đóng thanh tiến trình khi hoàn thành
        progress_bar.close()

        print("Processing completed.")