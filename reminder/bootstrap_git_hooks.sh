#!/bin/bash
cd ../
echo "Configuring pre-commit hook..."

# make a symbolic link with the pre-commit hook
if [ ! -f ./git/hooks/pre-commit ]; then
  ln reminder/git_hooks/pre-commit .git/hooks/pre-commit
  echo "Done"
else
  cat <<EOF
A pre-commit hook exists already.
EOF
fi