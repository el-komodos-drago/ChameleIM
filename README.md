What is ChameleIM?
==================
ChameleIM is an unfinished innovative private messenger with advanced protections from metadata collection.

Will it work?
=============
No of course it won't, I have basically no experience with cryptography and have been instructed to impliment the RSA algorithm myself. Get ready for some basic mistakes.

Why are you doing this?
=======================
ChameleIM started without any idea to build an E2EE messenger. The concept has been mine for a while: to create a piece of software where you can only talk to someone if you have physically met them. From there is spiralled into the fact that key verification remains the largest flaw in encrypted messaging (and with voice and video synthasisation technology getting better far faster than quality on voice and video calls is improving the old trick of reading a public PGP key down a telephone isn't going to work anymore). So if people are going to meet in person, why not use that to transfer public keys.

Then I started thinking about long running complaints about Signal: telephone numbers, lack of data at rest encryption, vulnderability to metadata collection both by Signal and by Amazon (the server hosts). Ideally a new E2EE messenger would not be vulnderable to any of those things. So I designed one that only used public keys to identify users to the server, encrypted data at rest with support for a duress password, and rapidly changed public keys making metadata collection potentially impossible.

I am also going to impliment steganography by hiding the encrypted data in the least significant bit of a PNG file. Mainly just for fun but also to potentially extend the tool into an e-mail utility (Chamele-mail - yes I know).

What's the roadmap?
===================

Chamele-mail - a encryption tool that takes the message, applies encryption and steganography, and then provides an output file to be sent by e-mail (or a similar tool). It is  much the same as the long term goal (ChameleIM) but doesn't actually send the message itself. To be delivered in early summer.
ChamelIM - a complete instant messenger with a central server that allows messages to be delivered to users. To be delivered in late summer.
ChameleTor - a far future goal with federated servers and an inbuilt tor connection. To be delivered whenever I get round to it.
