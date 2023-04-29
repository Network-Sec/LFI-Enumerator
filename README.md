# Warning
This project is in early development and may not work yet as expected

# LFI-Enumerator
CTF LFI Enumerator that looks for interesting files, which aren't present on a default ubuntu server

Will create output files containing the enumerated filesystem as well as other interesting info, instead of outputting to stdout.
##  Example Usage
```bash
usage: lfi_enum.py [-h] url basename wordlist structure   

Webserver enumeration and deviation finder

positional arguments:
  url         URL to send GET requests
  basename    Basename for the output files
  wordlist    Wordlist file containing default Linux files and directories (single words, not pathes. E.g. user\n bin\n bash\n)
  structure   Wordlist containing the file & directory structure of a Linux file system (pathes. E.g. /usr/bin/bash)
  
options:
  -h, --help  show this help message and exit

$ ./lfi_enum.py "http://example-ctf.box:8080/file?img=../../../../../../" example_ctf lfi_wordlist.txt structure.txt
```


# Create your own wordlist from a Linux filesystem
```bash
root$ find / -iname "*" 2>/dev/null | sed 's/\//\n/g' > /tmp/wordlist.txt
root$ cat /tmp/wordlist.txt | sort | uniq > /tmp/lfi_wordlist.txt
```
