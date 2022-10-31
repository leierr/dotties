####################################################################
export ZSH="$HOME/.oh-my-zsh"

plugins=(
	git
	history-substring-search
	colored-man-pages
	zsh-autosuggestions
	zsh-syntax-highlighting
)
####################################################################
alias ls='ls --color=auto -lah'
alias update='sudo pacman -Syu --noconfirm'
alias upgrade='yay -Syu --answerclean All --answerdiff None'
alias search='pacman -Ss'
alias remove='sudo pacman -Rns'
alias install='sudo pacman -S'
alias s='systemctl'
alias j='journalctl'
alias tripwire="~/.tripwire/tripwire.py --delete"
alias password="sleep 3 ; xdotool type 'WcAOV3Ygce'"
alias bsped="vim $HOME/.config/bspwm/bspwmrc"
alias cc="xclip -selection c -o | openssl x509 -noout -text | less"
####################################################################

export EDITOR="vim"
source $ZSH/oh-my-zsh.sh

bindkey '^ ' autosuggest-execute
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=247"

eval "$(starship init zsh)"
