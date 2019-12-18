# Build and release instructions

The process is a bit manual at the moment.  The intention is to automate the push to pyPI

1. Create dev branch and make fixes.  
2. When happy, create a version tag locally and push to GitHub:
   ```
   git tag -a v0.2.1 -m "#75 fix for bug when downloading from github on windows"
   git push --tags
   ```
3. Make sure all tests pass and install the new version correctly:
   ```
   make test TARBALL=true TESTALL=true
   ```
4. Upload to the testpypi
   ```
   make upload
   ```
5. Raise PR and merge to master

6. Upload to the live pypi
   ```
   make upload LIVE=true
   ```