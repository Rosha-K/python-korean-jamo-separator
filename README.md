# python korean jamo separator
입력한 한글의 자모를 분리해서 엑셀에 저장시키는 파이썬 코드입니다.

python korean handler를 수정해서 작성했습니다.

원본 코드는 아래 링크에 있습니다.

https://github.com/neotune/python-korean-handler/

## infomation

한글이 아닌 영문, 특수문자 사용시 작동하지 않습니다.
또한, 초성, 중성이 하나라도 없다면 작동하지 않습니다.

ex)ㅏ ㅑㅑ -> 작동안함

ex)ㅎㅎㅎㅎ ㅏㅏㅏ -> 작동안함

ex)ㅎ하ㅏㅏ이 -> 작동안함

ex)안녕하세요 -> 작동함


* `python3.5.X`

## example

input(python) : 테스트

output(xlsx) : ㅌ	ㅓ	ㅣ	ㅅ	ㅡ	ㅌ	ㅡ

![image](https://user-images.githubusercontent.com/65499218/221481224-ab7abece-690d-4731-a527-dab1cde08d91.png)


#### RUN

```console
python korean_jamo_separator.py
```

## Licence

[MIT](http://opensource.org/licenses/MIT)
