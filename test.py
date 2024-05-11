import tensorflow as tf


# Получаем список доступных физических устройств
physical_devices = tf.config.list_physical_devices()

print("Доступные физические устройства:")
for device in physical_devices:
    print(device)

print(tf.test.is_built_with_cuda())