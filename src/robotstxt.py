
import re
from io import TextIOBase, StringIO
from typing import Self
from collections import UserDict
from dataclasses import dataclass, field

def _match (pattern:str, source:str) -> bool:

  """文字列が指定されたパターンと一致するかを判定します。

  Parameters
  ----------
  pattern : str
    判定に使用されるパターン文字列です。
    この文字列には次の特殊文字を使用することができます。

    | 特殊文字 | 概要 |
    | --- | --- |
    | `*` | 0文字以上の任意の文字列に一致します。 |
    | `$` | 文字列の末尾に一致する。この文字が含まれていなければ先頭からの部分一致のみが行われます。 |

  source :str
    判定対象となる文字列です。

  Returns
  -------
  bool
    一致の成否を表す真偽値です。
  """

  if pattern:
    match pattern[0]:
      case "*":
        return any((_match(pattern[1:], source[i:]) for i in range(len(source) +1)))
      case "$":
        return not source
      case _:
        if source:
          return pattern[0] == source[0] and _match(pattern[1:], source[1:])
        else:
          return False
  else:
    return True

@dataclass
class Permissions:

  """参照が許可・禁止されているパスの集合を管理します。

  Attributes
  ----------
  allows : set[str]
    参照が許可されているパスの集合です。
  disallows : set[str]
    参照が禁止されているパスの集合です。
  """

  allows:set[str] = field(default_factory=set)
  disallows:set[str] = field(default_factory=set)

  def is_accessable (self, path:str) -> bool:

    """指定されたパスへの参照が可能かどうかを判定します。
  
    Notes
    -----
    属性 `allows` `disallows` に同じパスが設定されていた場合 `allows` の設定が優先されます。
    
    Parameters
    ----------
    path : str
      判定対象となるパスです。

    Returns
    -------
    bool
      参照の可否を表す真偽値です。
    """

    return (
      any((_match(p, path) for p in self.allows)) or
      not any((_match(p, path) for p in self.disallows)))

class UserAgentPermissions (UserDict):

  """ユーザーエージェント毎に設定された参照権限を保持する専用の辞書型です。"""

  def is_accessable (self, path:str, *, user_agent:str="*") -> bool:

    """指定されたパスへの参照が可能かどうかを判定します。

    Notes
    -----
    追加の引数 `user_agent` を要求する以外は `Permissions.is_accessable` と同じ振る舞いをします。

    Parameters
    ----------
    path : str
      判定対象となるパスです。
    user_agent : str
      検証時に指定されるユーザーエージェントです。
      未指定ならば "*" が使用されます。

    Returns
    -------
    bool
      参照の可否を表す真偽値です。
    """

    if user_agent in self.data:
      permissions = self.data[user_agent]
    elif "*" in self.data:
      permissions = self.data["*"]
    else:
      permissions = Permissions()
    return permissions.is_accessable(path)

@dataclass
class RobotsTxt:

  """UserAgentPermissions とサイトマップの集合をまとめたクラスです。

  Attributes
  ----------
  permissions : UserAgentPermissions
    ユーザーエージェント毎に設定された参照権限を保持する専用の辞書型です。
  sitemaps : set[str]
    robots.txt に記載されたサイトマップ URL の集合です。
  """

  permissions:UserAgentPermissions
  sitemaps:set[str]

  def dump (self, stream:TextIOBase):

    """...

    Parameters
    ----------
    stream : TextIOBase
      ...
    """

    for user_agent, permissions in sorted(self.permissions.items()):
      if permissions.allows or permissions.disallows:
        print("User-Agent: {:s}".format(user_agent), file=stream)
        for allow in permissions.allows:
          print("Allow: {:s}".format(allow), file=stream)
        for disallow in permissions.disallows:
          print("Disallow: {:s}".format(disallow), file=stream)
        print("", file=stream)
    for sitemap in self.sitemaps:
      print("Sitemap: {:s}".format(sitemap), file=stream)

  def dumps (self) -> str:

    """...

    Returns
    -------
    str
      ...
    """

    with StringIO() as stream:
      self.dump(stream)
      return stream.getvalue()

class ParseError (Exception):

  @classmethod
  def at (cls, message:str, line_and_linum:tuple[str, int]) -> Self:
    line, linum = line_and_linum
    return cls("{:s}: Line of {:d}, {:s}".format(message, linum, repr(line)))

_REGEXP_COMMENT:re.Pattern = re.compile(r"#.*$")
_REGEXP_USER_AGENT:re.Pattern = re.compile(r"^user-agent:\s*(\S.*)\s*$", re.I)
_REGEXP_ALLOW:re.Pattern = re.compile(r"^allow:\s*(\S.*)\s*$", re.I)
_REGEXP_DISALLOW:re.Pattern = re.compile(r"^disallow:\s*(\S.*)\s*$", re.I)
_REGEXP_SITEMAP:re.Pattern = re.compile(r"^sitemap:\s*(\S.*)\s*$", re.I)
_REGEXP_WHITESPACES:re.Pattern = re.compile(r"^\s*$")

def load (file:TextIOBase, *, ignore_error:bool=False) -> RobotsTxt:

  """robots.txt 形式のファイルを読み込み専用のオブジェクトを作成します。

  Examples
  --------
  >>> import robotstxt
  >>> from io import StringIO
  >>> with StringIO("User-Agent: *\\nDisallow: /\\nAllow: /public/\\n") as file:
  >>>   loaded = robotstxt.load(file)
  >>>   loaded.permissions.is_accessable("/")
  False
  >>>   loaded.permissions.is_accessable("/public/")
  True

  Raises
  ------
  ValueError
    引数 `file` が `TextIOBase` クラスを継承していない場合に送出されます。
  ParseError
    非対応の行が読み込まれた時に送出されます。

  Parameters
  ----------
  file : TextIOBase
    入力元となる file-like オブジェクトです。
  ignore_error : bool
    非対応の行が読み込まれた時に例外を送出するか無視するかを指定します。
    未指定ならば `False` が設定され、専用の例外が送出されます。

  Returns
  -------
  RobotsTxt
    robots.txt を読み込んで作成されたオブジェクトです。
  """

  if not isinstance(file, TextIOBase):
    raise ValueError("Argument `file` must be {:s} instance: {:s}".format(repr(TextIOBase), repr(file)))

  user_agent_permissions = UserAgentPermissions()
  cur_permissions = None
  read_user_agent = False
  sitemaps = set()
  for linum, line in enumerate(file):
    ln = _REGEXP_COMMENT.sub("", line)
    match = _REGEXP_USER_AGENT.match(ln)
    if match:
      user_agent, = match.groups()
      if read_user_agent:
        permissions = cur_permissions
      else:
        permissions = Permissions()
      user_agent_permissions[user_agent] = permissions
      cur_permissions = permissions
      read_user_agent = True
      continue
    match = _REGEXP_ALLOW.match(ln)
    if match:
      allow, = match.groups()
      cur_permissions.allows.add(allow)
      read_user_agent = False
      continue
    match = _REGEXP_DISALLOW.match(ln)
    if match:
      disallow, = match.groups()
      cur_permissions.disallows.add(disallow)
      read_user_agent = False
      continue
    match = _REGEXP_SITEMAP.match(ln)
    if match:
      sitemap, = match.groups()
      sitemaps.add(sitemap)
      continue
    match = _REGEXP_WHITESPACES.match(ln)
    if match:
      continue
    if not ignore_error:
      raise ParseError.at("Unsupported line was detected", (line, linum))
  return RobotsTxt(user_agent_permissions, sitemaps)

def loads (source:str, *, ignore_error:bool=False) -> RobotsTxt:

  """robots.txt 形式の文字列を読み込み専用オブジェクトを作成します。

  Examples
  --------
  >>> import robotstxt
  >>> loaded = robotstxt.loads("User-Agent: *\\nDisallow: /\\nAllow: /public/\\n")
  >>> loaded.permissions.is_accessable("/")
  False
  >>> loaded.permissions.is_accessable("/public/")
  True
  
  Notes
  -----
  送出される例外に関しては `load` 関数と同様です。

  Parameters
  ----------
  source : str
    入力元となる robots.txt 形式の文字列です。
  ignore_error : bool
    非対応の行が読み込まれた時に例外を送出するか無視するかを指定します。
    未指定ならば `False` が設定され、専用の例外が送出されます。

  Returns
  -------
  RobotsTxt
    robots.txt を読み込んで作成されたオブジェクトです。
  """

  if not isinstance(source, str):
    raise ValueError("Argument `source` must be {:s} instance: {:s}".format(repr(str), repr(source)))

  with StringIO(source) as stream:
    return load(stream, ignore_error=ignore_error)
