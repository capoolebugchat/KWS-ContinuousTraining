import pyrclone as rclone


configs = open("rclone.conf", 'r').read()
rclone.with_config(configs).run_cmd(
    command="mount", 
    extra_args=[
    "kf_minio:mlpipeline/pipeline", "blank2",
    "--daemon", "--log-file", "rclone.log",
    "-vv"])