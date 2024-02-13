# A proof of concept workaround for the Palworld text broadcast bug

![Palworld_Encoding_bug](https://github.com/Darkhand81/Palworld_broadcast_encoding_bug/assets/1334381/25cadc75-7da5-4419-b73f-861d2f799ad7)

So for us dedicated server owners, it's been quite annoying to have a `broadcast` command, only to find that it doesn't quite work. Only the first word you send in the command is sent to the server.  So if you broadcast `Hello everyone!`, either over rcon or in-game, people only see `Hello`.

At first, I thought that maybe the server was interpreting each word as an argument of the command, and only reading the first one.  But after some experimentation, I found it to be a text encoding mismatch!

When I first tried working around this bug, I tried replacing regular spaces with the unicode non-breaking space character `\u00a0` (NBSP), to see if using an alternate space character might let us get around it.  But when I tried this, those spaces would get replaced with `Â ` (an 'A' with a circumflex accent followed by a space).

In UTF-8 encoding, `\u00a0` is represented by the bytes `C2 A0`. But in ISO-8859-1 and Windows-1252 encodings, `C2` is `Â`, and `00` is `SPACE`! Hmm! Those are our characters!

So Palworld is mixing up two different encodings when receiving vs sending text data!

I created this test script in Python to confirm things.  The script sends a raw rcon command to the server... It takes a test message, like "broadcast Hello world!", and splits it up. The "broadcast " (with the first space) part is sent with regular utf-8 encoding, but the rest of the spaces in the message are replaced with the raw binary-encoded A0 character to represent a space, instead of UTF-8.

And it works!! We have here the world's first Palworld broadcast message with spaces!
