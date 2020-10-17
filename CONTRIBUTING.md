# Contributing to Sanctuary Zero

## Thanks for taking the time to contribute
The following is a set of guidelines for contributing to Sanctuary Zero, which are maintained by the AstroSonic community on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct for Contributors
This project and everyone participating in it is governed by the code of conduct for contributors which you can find [here](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [socials@astrosonic.tech](mailto:socials@astrosonic.tech).

## What should I know before getting started?
1. Sanctuary Zero is an open-source project targeting to facilitate messaging in a secure and synchronous manner.
2. The transience of messages and anonymity of the users conveying them are the most important things to consider.
3. In no circumstances can the project replace existing technologies due to its experimental nature of implementation.
4. The project aims to be secure and ways of achieving it but it is yet to be audited on the basis of security.
5. The major dependencies that the project makes use of are `websockets`, `python-prompt-toolkit`, `click` and `cryptography`.
6. The project is purely written in `Python` so an experience in the language and the aforesaid dependencies can be helpful.

## How can I contribute?
1. You can report bugs/glitches/faults that you are likely to come across when using the project server and client apps.
2. You can suggest enhancements that you would want to see implemented on the project - which gets voted in the roadmap.
3. You can address a wide variety of open issues if you wish to contribute using your code and make a pull request.

## Steps to contribute

* Comment on the issue you want to work on. Make sure it's not assigned to someone else.

* If you think you encounter a bug or have a suggestion for improvement of code or to add a feature, then create a issue with proper title and tags but first make sure it's not already present. And if you want to work on that, then comment on that issue and wait for the owner to assign that work to you.

### Making a PR

> - Make sure you have been assigned the issue to which you are making a PR.
> - If you make PR before being assigned, It will be labeled `invalid` and closed without merging.

* Fork the repo. This will create a copy of the current repository that you can edit and make changes to.

* Clone it on your machine. But first navigate to your forked repo and then, there you will find link provided by github to clone.

* Add a upstream link to main branch in your cloned repo
    ```
    git remote add upstream https://github.com/t0xic0der/sanctuary-zero.git
    ```
* Keep your cloned repo upto date by pulling from upstream (this will also avoid any merge conflicts while committing new changes)
    ```
    git pull upstream main https://github.com/t0xic0der/sanctuary-zero.git 
    ```
* Create your feature branch
    ```
    git checkout -b <feature-name>
    ```
* Commit all the changes
    ```
    git commit -m "Meaningful commit message"
    ```
* Push the changes for review
    ```
    git push origin <branch-name>
    ```
* Create a PR from your repo on Github. Give proper title and description of the changes you made.

* If all goes well, your request will be approved and will be merged.
