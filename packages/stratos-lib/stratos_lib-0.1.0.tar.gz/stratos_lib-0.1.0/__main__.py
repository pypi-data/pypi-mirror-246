from stratos_lib.components.vpc import VpcComponent
from stratos_lib import configs as confs

config = confs.VpcConfig()

component = VpcComponent(config=config)
