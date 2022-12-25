# quicksnap

The app is designed to be extremely simple for end users. To that end, it consists of an installation script, which should be run by you. It stores credentials, ensures dependencies are installed, and 

The client script itself then can be run with only one click. No authentication, preferences, or prompts. This is essential to prevent getting help from being just as difficult as a problem a tech-illiterate end-user is facing.

## GA blockers
* **No Row-Level-Security setup in Supabase yet**
* Credentials stored in plaintext, not Freedesktop Secret Store

## Roadmap
* Use screenshot portal if possible, falling back to scrot (fixes Wayland)

## Design limitations
* Screenshots, not screencasts
* No remote control
* Linux only
* Scrot only works on X :(


## Design discussion
### Why not use the Freedeskrop screenshot portal? 
The person this program was originally developed to help uses Solus, which, AFAIK, doesn't support it. 
### Why share credentials between end users and screenshot recipients?
This is easier for everyone. And given that you shouldn't be reusing your passwords, the consequences of a breach are minimal. Further, it is not expected that end users of this tool will try to manage their own account, or even know that credentials exist. Thus, it makes sense to only have one account.
### Why not use AppImage/Flatpak/Snap?
Given the utter simplicity of this tool, and the assumption that the installer has the skills requisite to run a simple installation script, at this point running any sort of CI or build process is overkill.

## Credits
Icon created by Dall-e
