export ROBOT_NAME=$(hostname)

export MQTT_BROKER_IP=''
export MQTT_BROKER_PORT=''
export MQTT_ENCODING='json'

export ALSA_INPUT="hw:3,0"
export ALSA_OUTPUT="hw:2,0"
export DOCKER_ESPEAK=True

export JOY_DEV='/dev/input/js0'
export JOY_CONFIG=$MY_LIMO/config/logitech.yaml

export ENVIRONMENT_TEMPLATE='/workspaces/limo_ros2/src/custom_packages/environment_template'
source $ENVIRONMENT_TEMPLATE/config/environment.sh
export TMAP_FILE_WRITE=$ENVIRONMENT_TEMPLATE/config/topological/network.tmap2.yaml

source $MY_LIMO/bash/secrets.sh