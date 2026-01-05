
import pytest
import robotstxt

def test_match ():

  #空文字列に対する一致の動作確認

  assert robotstxt._match("", "") == True
  assert robotstxt._match("", "a") == True
  assert robotstxt._match("", "ab") == True
  assert robotstxt._match("", "abc") == True

  #単純な一致の動作確認

  assert robotstxt._match("ab", "a") == False
  assert robotstxt._match("ab", "ab") == True
  assert robotstxt._match("ab", "abc") == True

  #末尾一致の動作確認

  assert robotstxt._match("ab$", "a") == False
  assert robotstxt._match("ab$", "ab") == True
  assert robotstxt._match("ab$", "abc") == False

  #任意の文字列に対する一致の動作確認

  assert robotstxt._match("a*c", "ac") == True
  assert robotstxt._match("a*c", "abc") == True
  assert robotstxt._match("a*c", "abbc") == True
