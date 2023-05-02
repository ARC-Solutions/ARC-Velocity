import tensorflow as tf

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))




# Set the GPU memory growth to avoid allocating all GPU memory at once
gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
