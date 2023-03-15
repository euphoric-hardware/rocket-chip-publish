import pytest

from helpers import mill_sc_version, get_new_version, replace_version_rc, replace_version_libs

class Test:
    sc_snippet = """
  def publishVersion = T {
    "1.6.0"
  }
""".split('\n')
    bad_snippet = """
    override def publishVersion = T {
      m.publishVersion()
    }
""".split('\n')
    snapshot_snippet = """
  def publishVersion = T {
    "1.2.0-SNAPSHOT"
  }
""".split('\n')

    patched_sc_snippet = """
  def publishVersion = T {
"1.8.0-ff-SNAPSHOT"
  }
""".split('\n')

    lib_snippet = """
  other_line
  def publishVersion = "1.2.0-SNAPSHOT"
  def publishVersion = de.tobiasroeser.mill.vcs.version.VcsVersion.vcsState().format()
""".split('\n')
    patched_lib_snippet = """
  other_line
def publishVersion = "1.8.0-ff-SNAPSHOT"
def publishVersion = "1.8.0-ff-SNAPSHOT"
""".split('\n')

    def test_mill_sc_version(self) -> None:
        version = mill_sc_version(self.sc_snippet)
        assert version == "1.6.0"

        with pytest.raises(ValueError):
            mill_sc_version(self.bad_snippet)

        with pytest.raises(ValueError):
            mill_sc_version(self.snapshot_snippet)

    def test_new_version(self) -> None:
        assert get_new_version("32e2bfcce", "1.6.0") == "1.6.0-32e2bfcce-SNAPSHOT"

    def test_replace_version_rc(self) -> None:
        assert replace_version_rc(self.sc_snippet, "1.8.0-ff-SNAPSHOT") == \
            self.patched_sc_snippet

    def test_replace_version_libs(self) -> None:
        assert replace_version_libs(self.lib_snippet, "1.8.0-ff-SNAPSHOT") == \
            self.patched_lib_snippet
