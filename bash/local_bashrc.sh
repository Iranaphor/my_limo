alias t='tmux'

function gs () { git status . ; }
function vm () { tmule -c /workspaces/limo_ros2/src/custom_packages/verbaliser/new_tmule/chat.tmule.yaml $1 ; }
function tm () { tmule -c /workspaces/limo_ros2/src/custom_packages/my_limo/tmule/talky.tmule.yaml $1 ; }
function mu () { tmule -c /workspaces/limo_ros2/src/custom_packages/my_limo/tmule/$1.tmule.yaml $2 ; }
