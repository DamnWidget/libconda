import sublime

PREFERENCES_BUCKET = 'Preferences.sublime-settings'


def get(key, default=None):
    """Get the value specified by key from PREFERENCES_BUCKET
    """

    return sublime.load_settings(PREFERENCES_BUCKET).get(key, default)


def set(key, value):
    """Set the value specified by value into the key specified by key
    """

    settings = sublime.load_settings(PREFERENCES_BUCKET)
    settings[key] = value
    sublime.save_settings(PREFERENCES_BUCKET)
