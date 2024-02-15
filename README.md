# A proof of concept workaround for the Palworld text broadcast bug

![Palworld_Encoding_bug](https://github.com/Darkhand81/Palworld_broadcast_encoding_bug/assets/1334381/25cadc75-7da5-4419-b73f-861d2f799ad7)

So for us dedicated server owners, it's been quite annoying to have a `broadcast` command, only to find that it doesn't quite work. Only the first word you send in the command is sent to the server.  So if you broadcast `Hello everyone!`, either over rcon or in-game, people only see `Hello`.

It seems as though the server is interpreting each word after the `broadcast` message as an argument, and only interpreting the first one. But after some experimentation, I found a workaround!

When I first tried working around this bug, I tried replacing regular spaces with the unicode non-breaking space character `\u00a0` (NBSP), to see if using an alternate space character might let us get around it.  While this didn't work, it pointed me in the right direction... When I tried this, those spaces would get replaced with `Â ` (an 'A' with a circumflex accent followed by a space).

In UTF-8 encoding, `\u00a0` is represented by the bytes `C2 A0`. But in ASCII, `C2` is `Â`, and `A0` is a non-breaking space! Hmm! Those are the characters we see!  Palworld doesn't seem to want to accept Unicode (which is odd considering its native Japanese text), but it will take ASCII...  We can replace spaces with the ASCII NBSP code `A0`, but will those NBSP spaces render correctly?

I created this test script in Python to confirm things.  The script sends a raw rcon command to the server... It takes a test message, like `broadcast Hello world!`, and splits it up. The `broadcast ` (with the first space) part is sent with regular utf-8 encoding, but the rest of the spaces in the message are replaced with the raw hex `A0` character to force an ASCII non-breaking space to be sent instead of a regular space.

And it works!! We have here the world's first Palworld broadcast message with spaces! Technically we're only giving one long argument to the `broadcast` command, since it doesn't treat the NBSP spaces as actual spaces!
