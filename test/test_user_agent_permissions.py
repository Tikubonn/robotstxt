
import pytest
import robotstxt

def test_user_agent_permissions ():

  #基本機能の動作確認です

  permissions = robotstxt.UserAgentPermissions({
    "*": robotstxt.Permissions(
      disallows={"/"}
    ),
    "TestBot": robotstxt.Permissions(
      disallows={"/"},
      allows={"/a/"}
    ),
  })

  #user_agent="*" の動作確認です

  assert permissions.is_accessable("/", user_agent="*") == False
  assert permissions.is_accessable("/a/", user_agent="*") == False
  assert permissions.is_accessable("/a/b/", user_agent="*") == False
  assert permissions.is_accessable("/a/b/c/", user_agent="*") == False
  assert permissions.is_accessable("/b/", user_agent="*") == False
  assert permissions.is_accessable("/c/", user_agent="*") == False

  #user_agent が未指定ならば "*" が設定されます

  assert permissions.is_accessable("/") == False
  assert permissions.is_accessable("/a/") == False
  assert permissions.is_accessable("/a/b/") == False
  assert permissions.is_accessable("/a/b/c/") == False
  assert permissions.is_accessable("/b/") == False
  assert permissions.is_accessable("/c/") == False

  #user_agent="TestBot" の動作確認です

  assert permissions.is_accessable("/", user_agent="TestBot") == False
  assert permissions.is_accessable("/a/", user_agent="TestBot") == True
  assert permissions.is_accessable("/a/b/", user_agent="TestBot") == True
  assert permissions.is_accessable("/a/b/c/", user_agent="TestBot") == True
  assert permissions.is_accessable("/b/", user_agent="TestBot") == False
  assert permissions.is_accessable("/c/", user_agent="TestBot") == False
