# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture

# this package
from create_redirect import create_redirect


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
def test_create_redirect(url: str, advanced_file_regression: AdvancedFileRegressionFixture):
	out = create_redirect(url)
	advanced_file_regression.check(out, extension=".html")
