
import pytest
import robotstxt

def test_permissions ():
  permissions = robotstxt.Permissions(
    allows={"/a/"},
    disallows={"/"}
  )
  assert permissions.is_accessable("/") == False
  assert permissions.is_accessable("/a/") == True
  assert permissions.is_accessable("/a/b/") == True
  assert permissions.is_accessable("/a/b/c/") == True
  assert permissions.is_accessable("/b/") == False
  assert permissions.is_accessable("/c/") == False

def test_permissions_empty ():
  permissions = robotstxt.Permissions()
  assert permissions.is_accessable("/") == True
  assert permissions.is_accessable("/a/") == True
  assert permissions.is_accessable("/a/b/") == True
  assert permissions.is_accessable("/a/b/c/") == True

def test_permissions_allows_only ():
  permissions = robotstxt.Permissions(
    allows={"/a/"}
  )
  assert permissions.is_accessable("/") == True
  assert permissions.is_accessable("/a/") == True
  assert permissions.is_accessable("/a/b/") == True
  assert permissions.is_accessable("/a/b/c/") == True

def test_permissions_disallows_only ():
  permissions = robotstxt.Permissions(
    disallows={"/a/"}
  )
  assert permissions.is_accessable("/") == True
  assert permissions.is_accessable("/a/") == False
  assert permissions.is_accessable("/a/b/") == False
  assert permissions.is_accessable("/a/b/c/") == False
  assert permissions.is_accessable("/b/") == True
  assert permissions.is_accessable("/c/") == True
