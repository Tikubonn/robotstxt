
import pytest
from io import StringIO
from robotstxt import RobotsTxt, UserAgentPermissions, Permissions

def test_robots_txt_dump ():

  #...

  robots_txt = RobotsTxt(
    permissions=UserAgentPermissions({
      "*": Permissions(
        disallows={"/"}
      ),
      "TestBot": Permissions(
        disallows={"/"},
        allows={"/public/"}
      )
    }),
    sitemaps={"http://www.example.com/sitemap.xml"}
  )
  with StringIO() as stream:
    robots_txt.dump(stream)
    assert stream.getvalue() == """User-Agent: *
Disallow: /

User-Agent: TestBot
Allow: /public/
Disallow: /

Sitemap: http://www.example.com/sitemap.xml
"""

def test_robots_txt_dumps ():

  #...

  robots_txt = RobotsTxt(
    permissions=UserAgentPermissions({
      "*": Permissions(
        disallows={"/"}
      ),
      "TestBot": Permissions(
        disallows={"/"},
        allows={"/public/"}
      )
    }),
    sitemaps={"http://www.example.com/sitemap.xml"}
  )
  assert robots_txt.dumps() == """User-Agent: *
Disallow: /

User-Agent: TestBot
Allow: /public/
Disallow: /

Sitemap: http://www.example.com/sitemap.xml
"""
