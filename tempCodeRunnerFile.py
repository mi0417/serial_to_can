
    config, result = ConfigParams.from_toml_data('tool-config.toml')
    print(config)
    print(result)
    print(ConfigParams.to_config_str(config.data))