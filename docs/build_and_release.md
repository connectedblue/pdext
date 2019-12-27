# Dev and git branches

There are two main branches:

 * `master` this syncronises with the latest version released onto pyPI.  The version number tags
    should be of the format X.Y.Z and tagged against commits in the master branch.  Commits can
    only be made via PRs.  There may also be documentation releases in between pyPI releases, but
    these are not tagged on master.

 * `develop` this contains all merged tickets beyond master.  Ideally all commits should be via
    PRs, but not enforced.  All tests should pass before committing anything to this branch.

Bug and feature development is done under branches of the form `iss-N` where `N` is
the github issue number.  Tests don't necessarily have to pass for every commit, although it's 
useful if they do.  Once a ticket is complete, raise a PR to merge into `develop` and delete the
`iss-` branch.

On GitHub the list of tickets merged into develop but not yet on pyPI/master is maintained.

# Prepare releases

Create a new branch called `vX.Y.Z-rc` from `develop` and use `git rebase -i HEAD~N` if
necessary to cherry pick commits to place into the release.

Update the version number in `symbols.py` and test everything in the branch. Version
numbers are `vX.Y.Z-rcN`

When happy,make the final version `vX.Y.Z` but don't version bump in this branch.
Raise a PR to merge that branch into master.

NOTE:  Still to figure out -- How to progess with develop if certain
       commits are excluded from a release candidate:
         * After merge, do a `git rebase master` on the develop branch?
         * Create a new `develop`??
         * How are the already merged commits on `develop` handled after this?

 

# Release to pyPI

The process is a bit manual at the moment.  The intention is to automate the push to pyPI

1. Checkout master
2. Version bump on master using `make bump`
3. Make sure all tests pass and install the new version correctly:
   ```
   make test TARBALL=true TESTALL=true
   ```
4. Upload to the testpypi
   ```
   make upload
   ```

5. Upload to the live pypi
   ```
   make upload LIVE=true
   ```