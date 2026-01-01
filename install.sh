#!/usr/bin/env bash
set -e

TOOL_NAME="PDF_highlight_extractor"
TOOL_FILE="app.py"
INSTALL_DIR="."
#INSTALL_DIR="$HOME/.local/$TOOL_NAME"
BIN_DIR="$HOME/.local/bin"

# by default this installer installs a command line tool and creates an installable app
# if you prefer to only install the command line program, use --cli or -c
# if you prefer to only build the installable app,        use --app or -a

show_help() {
  cat <<EOF
Usage: $(basename "$0") [options]

Options:
  --cli, -c    Create the command-line app and install it for your terminal
  --app, -a    Create an installable app that you can drag and drop to /Applications
  --help, -h   Show this help message and exit
EOF
}

# No args → show help
for arg in "$@"; do
  if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
    show_help
    exit 0
  fi
done

if [[ $# -eq 0 ]]; then
  echo -e "No arguments were passed, will:\n  1. Install the command line tool.\n  2. Build an installable app."
  APP=true
  CLI=true
else
  echo "Arguments provided, will parse arguments to check what to build (--app and/or --cli)"	
  APP=false
  CLI=false
fi


# Ensure directories exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# check arguments
for arg in "$@"; do
  if [[ "$arg" == "--cli" || "$arg" == "-c" ]]; then
    CLI=true
    echo -e "  Will install the command line tool."
  fi
  if [[ "$arg" == "--app" || "$arg" == "-a" ]]; then
    APP=true
    echo -e "  Will build an installable app."
  fi
  if [[ "$arg" == "--clean" ]]; then
    APP=true
    read -p "Confirm deletion of your virtual environment ("$INSTALL_DIR/venv") and temp files from .app (build, dist, app.spec)? [y/N] " answer
    [[ "$answer" != "y" ]] && exit 0
    rm -rf "$INSTALL_DIR/venv";
    rm -rf build dist app.spec;
    echo "virtual environment ("$INSTALL_DIR/venv") and temp files from .app deleted. Exiting."
    exit 0
  fi

done

# Create virtual environment
python3 -m venv "$INSTALL_DIR/venv"

# Activate and install deps
source "$INSTALL_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

if $CLI; then
   echo -e "Installing $TOOL_NAME as a command-line tool, which you can invoke from your terminal using\n $TOOL_NAME"

  # Copy script
  cp "$TOOL_FILE" "$INSTALL_DIR/$TOOL_NAME"

  # Create launcher
cat > "$BIN_DIR/$TOOL_NAME" <<EOF
  #!/usr/bin/env bash
  source "$INSTALL_DIR/venv/bin/activate"
  exec python "$INSTALL_DIR/$TOOL_NAME" "\$@"
EOF

  chmod +x "$BIN_DIR/$TOOL_NAME"

  read -p "Add ~/.local/bin to your PATH? [y/N] " answer
  [[ "$answer" != "y" ]] && exit 0

  SHELL_NAME=$(basename "$SHELL")

  case "$SHELL_NAME" in
    bash)
      PROFILE="$HOME/.bashrc"
      ;;
    zsh)
      PROFILE="$HOME/.zshrc"
      ;;
    *)
      echo "Unknown shell. Please add ~/.local/bin to PATH manually."
      exit 0
      ;;
  esac

  LINE='export PATH="$HOME/.local/bin:$PATH"'

  grep -qxF "$LINE" "$PROFILE" || echo "$LINE" >> "$PROFILE"

  echo "Added to $PROFILE. Restart your shell."

  echo "Installed successfully as command line tool (you will need to restart your shell to run)."

fi


if $APP; then

  echo "Next, we will produce a .app file that you can drag-and-drop to your /Applications folder to install"
  rm -rf build dist app.spec;


  pip install pyinstaller;
  #pyinstaller --windowed --onefile app.py;
  pyinstaller --windowed --onefile --clean --noconfirm app.py;
  DIST_DIR="$(pwd)/dist"
  sleep 2;
  echo "$DIST_DIR/"$TOOL_NAME".app";
  mv $DIST_DIR/app.app $DIST_DIR/"$TOOL_NAME".app;

  echo -e "Completed, just drag and drop the $TOOL_NAME.app icon to /Applications folder.\n(remember: to run the command line tool, you might need to restart your shell)"

  open $DIST_DIR;
  open /Applications;
fi
