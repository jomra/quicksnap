⚠️⚠️⚠️ This is pre-alpha software. It's insecure, ugly, and unreliable. ⚠️⚠️⚠️

# quicksnap

The app is designed to be extremely simple for end users. To that end, it consists of an installation script, which should be run by you. It stores credentials, ensures dependencies are installed, and sets up the `.desktop` file.

The client script itself then can be run with only one click. No authentication, preferences, or prompts. This makes it much easier for tech-illiterate end users to get help.

## Setup
*Only works on Linux computers.*
1. Make an account at [quicksn.app](https://quicksn.app)
2. Ensure `nodejs`, `npm`, & (`flameshot` or `scrot`)* are installed. If you are using Ubuntu, you'll also need to install `python-is-python3`
3. [Download](https://raw.githubusercontent.com/jomra/quicksnap/main/quicksnap-quickstart.py) and run `quicksnap-quickstart.py`
4. [Optional] Pin Quicksn.app to the launcher for easy usage
* Flameshot is prefered and supports Wayland. Scrot is more likely to be preinstalled and can capture the user's cursor.

## Design discussion

### Limitations
* Screenshots, not screencasts
* No remote control
* Linux only

### Why share credentials between end users and screenshot recipients?
This is easier for everyone. And given that you shouldn't be reusing your passwords, the consequences of a breach are minimal. It is not expected that end users of this tool will try to manage their own account, or even know that one exists. Thus, it makes sense to only have one account.

### Why not use AppImage/Flatpak/Snap?
Given the utter simplicity of this tool, and the assumption that the installer has the skills requisite to run a simple installation script, at this point running any sort of CI or build process is overkill.

## Credits
Icon created by Dall-e
