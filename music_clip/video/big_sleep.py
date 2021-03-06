from big_sleep import Imagine


class BigSleepImagine(Imagine):
    def __init__(
        self,
        *,
        text=None,
        img=None,
        encoding=None,
        text_min="",
        lr=0.07,
        image_size=512,
        gradient_accumulate_every=1,
        save_every=50,
        epochs=20,
        iterations=1050,
        save_progress=False,
        bilinear=False,
        open_folder=True,
        seed=None,
        append_seed=False,
        torch_deterministic=False,
        max_classes=None,
        class_temperature=2,
        save_date_time=False,
        save_best=False,
        experimental_resample=False,
        ema_decay=0.99,
        num_cutouts=128,
        center_bias=False
    ):
        super().__init__(
            text=text,
            img=img,
            encoding=encoding,
            text_min=text_min,
            lr=lr,
            image_size=image_size,
            gradient_accumulate_every=gradient_accumulate_every,
            save_every=save_every,
            epochs=epochs,
            iterations=iterations,
            save_progress=save_progress,
            bilinear=bilinear,
            open_folder=open_folder,
            seed=seed,
            append_seed=append_seed,
            torch_deterministic=torch_deterministic,
            max_classes=max_classes,
            class_temperature=class_temperature,
            save_date_time=save_date_time,
            save_best=save_best,
            experimental_resample=experimental_resample,
            ema_decay=ema_decay,
            num_cutouts=num_cutouts,
            center_bias=center_bias,
        )

