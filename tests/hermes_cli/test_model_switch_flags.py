from hermes_cli.model_switch import parse_model_flags


def test_parse_model_flags_basic_model():
    assert parse_model_flags("sonnet") == ("sonnet", "", False, False)


def test_parse_model_flags_provider_and_global():
    assert parse_model_flags("sonnet --provider anthropic --global") == (
        "sonnet",
        "anthropic",
        True,
        False,
    )


def test_parse_model_flags_refresh_only():
    assert parse_model_flags("--refresh") == ("", "", False, True)


def test_parse_model_flags_unicode_dash_refresh():
    # Telegram / mobile keyboards sometimes convert '--refresh' into an em dash form.
    assert parse_model_flags("sonnet —refresh") == ("sonnet", "", False, True)
