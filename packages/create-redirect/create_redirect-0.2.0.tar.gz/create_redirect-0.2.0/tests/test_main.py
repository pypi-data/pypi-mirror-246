# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus, in_directory

# this package
from create_redirect.__main__ import main


@pytest.mark.parametrize(
		"url",
		[
				pytest.param("bbc.co.uk", id="domain_no_scheme"),
				pytest.param("http://bbc.co.uk", id="domain_http"),
				pytest.param("https://bbc.co.uk", id="domain_https"),
				pytest.param("bbc.co.uk/news", id="path_no_scheme"),
				pytest.param("http://bbc.co.uk/news", id="path_http"),
				pytest.param("https://bbc.co.uk/news", id="path_https"),
				pytest.param("bbc.co.uk/news/", id="path_trailing_slash_no_scheme"),
				pytest.param("http://bbc.co.uk/news/", id="path_trailing_slash_http"),
				pytest.param("https://bbc.co.uk/news/", id="path_trailing_slash_https"),
				]
		)
def test_main(url: str, monkeypatch, capsys, advanced_file_regression: AdvancedFileRegressionFixture):
	monkeypatch.setattr("sys.argv", ["create_redirect.py", url, '-'])

	main()

	out, err = capsys.readouterr()

	advanced_file_regression.check(out, extension=".html")


@pytest.mark.parametrize(
		"url",
		[
				pytest.param("bbc.co.uk", id="domain_no_scheme"),
				pytest.param("http://bbc.co.uk", id="domain_http"),
				pytest.param("https://bbc.co.uk", id="domain_https"),
				pytest.param("bbc.co.uk/news", id="path_no_scheme"),
				pytest.param("http://bbc.co.uk/news", id="path_http"),
				pytest.param("https://bbc.co.uk/news", id="path_https"),
				pytest.param("bbc.co.uk/news/", id="path_trailing_slash_no_scheme"),
				pytest.param("http://bbc.co.uk/news/", id="path_trailing_slash_http"),
				pytest.param("https://bbc.co.uk/news/", id="path_trailing_slash_https"),
				]
		)
def test_main_to_file(
		tmp_pathplus: PathPlus, url: str, monkeypatch, advanced_file_regression: AdvancedFileRegressionFixture
		):
	with in_directory(tmp_pathplus):
		monkeypatch.setattr("sys.argv", ["create_redirect.py", url, "index.html"])
		main()
		advanced_file_regression.check_file("index.html")


@pytest.mark.parametrize(
		"url",
		[
				pytest.param("bbc.co.uk", id="domain_no_scheme"),
				pytest.param("http://bbc.co.uk", id="domain_http"),
				pytest.param("https://bbc.co.uk", id="domain_https"),
				pytest.param("bbc.co.uk/news", id="path_no_scheme"),
				pytest.param("http://bbc.co.uk/news", id="path_http"),
				pytest.param("https://bbc.co.uk/news", id="path_https"),
				pytest.param("bbc.co.uk/news/", id="path_trailing_slash_no_scheme"),
				pytest.param("http://bbc.co.uk/news/", id="path_trailing_slash_http"),
				pytest.param("https://bbc.co.uk/news/", id="path_trailing_slash_https"),
				]
		)
def test_main_to_file_default(
		tmp_pathplus: PathPlus, url: str, monkeypatch, advanced_file_regression: AdvancedFileRegressionFixture
		):
	with in_directory(tmp_pathplus):
		monkeypatch.setattr("sys.argv", ["create_redirect.py", url])
		main()
		advanced_file_regression.check_file("redirect.html")
