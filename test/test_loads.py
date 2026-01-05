
import pytest
import robotstxt

def test_loads ():
  loaded = robotstxt.loads("""
#This is comment.

User-Agent: *
Disallow: /

Sitemap: https://www.example.com/sitemap.xml

User-Agent: TestBot
User-Agent: TestBot2
User-Agent: TestBot3
Disallow: /
Allow: /a/
""")
  assert len(loaded.permissions) == 4
  assert "*" in loaded.permissions
  assert loaded.permissions["*"].allows == set()
  assert loaded.permissions["*"].disallows == {"/"}
  assert "TestBot" in loaded.permissions
  assert loaded.permissions["TestBot"].allows == {"/a/"}
  assert loaded.permissions["TestBot"].disallows == {"/"}
  assert "TestBot2" in loaded.permissions
  assert loaded.permissions["TestBot2"].allows == {"/a/"}
  assert loaded.permissions["TestBot2"].disallows == {"/"}
  assert "TestBot3" in loaded.permissions
  assert loaded.permissions["TestBot3"].allows == {"/a/"}
  assert loaded.permissions["TestBot3"].disallows == {"/"}
  assert loaded.sitemaps == {"https://www.example.com/sitemap.xml"}

TEST_CODE_ERROR = """
#This is comment.

User-Agent: *
Disallow: /

Sitemap: https://www.example.com/sitemap.xml

UNSUPPORTED_LINE!

User-Agent: TestBot
User-Agent: TestBot2
User-Agent: TestBot3
Disallow: /
Allow: /a/
"""

def test_load_error ():
  with pytest.raises(robotstxt.ParseError):
    loaded = robotstxt.loads(TEST_CODE_ERROR, ignore_error=False)

def test_load_ignore_error ():
  loaded = robotstxt.loads(TEST_CODE_ERROR, ignore_error=True)
  assert len(loaded.permissions) == 4
  assert "*" in loaded.permissions
  assert loaded.permissions["*"].allows == set()
  assert loaded.permissions["*"].disallows == {"/"}
  assert "TestBot" in loaded.permissions
  assert loaded.permissions["TestBot"].allows == {"/a/"}
  assert loaded.permissions["TestBot"].disallows == {"/"}
  assert "TestBot2" in loaded.permissions
  assert loaded.permissions["TestBot2"].allows == {"/a/"}
  assert loaded.permissions["TestBot2"].disallows == {"/"}
  assert "TestBot3" in loaded.permissions
  assert loaded.permissions["TestBot3"].allows == {"/a/"}
  assert loaded.permissions["TestBot3"].disallows == {"/"}
  assert loaded.sitemaps == {"https://www.example.com/sitemap.xml"}
