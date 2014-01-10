scripts
=======

Scripts for managing Computer Science Foundations stuff.

notes:
---

names.txt
 - source for access to student email/ID, name, and github username; useful for writing scripts of various sorts
 - I'll try to keep this up-to-date as the class continues

pygithub
 - this is the package I'm using for access to the github api through python. docs at http://jacquev6.github.io/PyGithub/
 - install with

    pip install pygithub
    
 - import with 

    import github
    
pygithub_scraps.py
 - the file containing all my work to automate github administration using pygithub.
 - WIP, so bear with me. If you think something should be in there that isn't, feel free to add it
 - if you feel something should be changed or removed, ask me about it first--in case I've written something somewhere that depends on it.
 - upon importing, will ask for your github username and password. These are used to authenticate ensuing api calls, and are not stored.


__See individual files for more detail__


If there's something that you think isn't obvious or is badly explained, let me (Colin) know
