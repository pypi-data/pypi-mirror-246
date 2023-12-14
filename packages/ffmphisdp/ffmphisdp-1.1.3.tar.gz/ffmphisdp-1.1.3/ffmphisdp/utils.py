"""This module contains utility methods to test a video readers output the expected frames"""
import signal

import ffmpeg  # type: ignore
import numpy as np  # type: ignore


def create_video(data: list, final_filename: str, size: int = 10, red_shift: int = 11, green_shift: int = 17):
    """Create a CFR or VFR video file whose frame index can be identified by the frame color
    Args:
        data (list): a list of tuple in the following format: [(filename, framerate, frame_count), ...]
        final_filename (str):  the name of the final video file (unused if len(data) == 1)
        size (int): width and height of the video
        red_shift (int): the amount of red that is added to each frame (loop at 256)
        green_shift (int): the amount of green that is added to each frame  (loop at 256)
    """
    total_frame_count = sum([frame_count for _, _, frame_count in data])
    # Create the frames
    frame_array: np.typing.NDArray = np.ndarray(shape=(total_frame_count, size, size, 3), dtype=np.uint8)
    for frame_idx in range(total_frame_count):
        frame_array[frame_idx, :, :, :] = np.full(
            (size, size, 3), (np.uint8(frame_idx * red_shift), np.uint8(frame_idx * green_shift), np.uint8(0))
        )

    used_frames = 0
    for filename, framerate, frame_count in data:
        # Create the video file for the framerate section:
        process = (
            ffmpeg.input('pipe:', format='rawvideo', r=framerate, pix_fmt='rgb24', s='{}x{}'.format(size, size))
            .output(filename, pix_fmt='yuv420p', vcodec='libx264', r=framerate)
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        for frame in frame_array[used_frames : used_frames + frame_count]:
            process.stdin.write(frame.astype(np.uint8).tobytes())
        process.stdin.close()
        process.wait()
        used_frames += frame_count

    if len(data) > 1:
        ffmpeg.concat(*[ffmpeg.input(filename, r=framerate) for filename, framerate, _ in data]).output(
            final_filename, vsync='vfr'
        ).overwrite_output().run()


def expected_frame_color(frame_index: int, red_shift: int = 11, green_shift: int = 17):
    """Return the expected frame color for the given frame index of a video created by the create_video method
    Args:
        frame_index (int): the frame index
        red_shift (int): the amount of red that is added to each frame (loop at 256)
        green_shift (int): the amount of green that is added to each frame  (loop at 256)
    Returns:
        tuple: the expected frame color (red, green, blue)
    """
    return np.uint8(frame_index * red_shift), np.uint8(frame_index * green_shift), np.uint8(0)


def is_almost_same_color(color1: np.uint8, color2: np.uint8):
    """This method normalize color comparisons of a frame encoded using the create_video method
    It account for the fact that encoding will slightly degrade colors
    Args:
        color1 (np.uint8): the color to compare
        color2 (np.uint8): the expected color
    Returns:
        bool: True if the color is close enough to the expected color
    """
    return abs(int(color1) - int(color2)) < 4


class Timeout:
    """
    This class is used to run a block of code with a timeout.
    It is meant to be used as a context manager, for example:
    ```
        with Timeout(5):
            do_something()
    ```
    """

    class TimeoutException(Exception):
        pass

    def __init__(self, timeout: float):
        """Create a Timeout object
        Args:
            timeout (float): the timeout in seconds
        """
        self.timeout = timeout

    @staticmethod
    def handler(signum, frame):
        raise Timeout.TimeoutException()

    def __enter__(self):
        signal.signal(signal.SIGALRM, Timeout.handler)
        signal.setitimer(signal.ITIMER_REAL, 0.001)

    def __exit__(self, exc_type, value, traceback):
        if exc_type == Timeout.TimeoutException:
            return True
